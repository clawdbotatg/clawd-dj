#!/usr/bin/env python3
"""Analyze rendered audio, optionally against a reference — the sandbox's judgment.

Usage:
  python3 sandbox/analyze.py mine.wav
  python3 sandbox/analyze.py mine.wav ref.m4a --start-b 150 --dur-b 30

Any ffmpeg-decodable input works. With two files, prints side-by-side metrics
and deltas so a rendition can be compared to the YouTube reference:
BPM (onset autocorrelation), onset density, band energy profile, spectral
centroid, RMS/crest. Only needs numpy + ffmpeg.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

SR = 22050
BANDS = [("sub", 20, 60), ("kick", 60, 120), ("bass", 120, 250), ("lowmid", 250, 800),
         ("mid", 800, 2500), ("high", 2500, 8000), ("air", 8000, 11000)]


def load(path, start=0.0, dur=None):
    with tempfile.NamedTemporaryFile(suffix=".f32", delete=False) as f:
        tmp = f.name
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-i", str(path)]
    if dur:
        cmd += ["-t", str(dur)]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", tmp]
    subprocess.run(cmd, check=True)
    x = np.fromfile(tmp, dtype=np.float32)
    Path(tmp).unlink()
    return x


def onset_envelope(x, hop=256, win=1024):
    frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]
    spec = np.abs(np.fft.rfft(frames * np.hanning(win), axis=1))
    flux = np.maximum(spec[1:] - spec[:-1], 0).sum(axis=1)
    return flux / (flux.max() + 1e-9), SR / hop


def bpm_estimate(env, fps):
    env = env - env.mean()
    ac = np.correlate(env, env, "full")[len(env) - 1:]
    best_bpm, best_v = 0.0, -1.0
    for lag in range(int(fps * 60 / 200), int(fps * 60 / 60)):  # 60..200 bpm
        if lag < len(ac) and ac[lag] > best_v:
            best_v, best_bpm = ac[lag], 60.0 * fps / lag
    return best_bpm


def metrics(x):
    if len(x) < SR:
        return {"error": "audio too short"}
    rms = float(np.sqrt((x ** 2).mean()))
    peak = float(np.abs(x).max())
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    total = (spec ** 2).sum() + 1e-12
    bands = {n: round(float((spec[(freqs >= lo) & (freqs < hi)] ** 2).sum() / total), 4)
             for n, lo, hi in BANDS}
    centroid = float((freqs * spec).sum() / (spec.sum() + 1e-12))
    env, fps = onset_envelope(x)
    thresh = env.mean() + env.std()
    onsets = int(((env[1:] > thresh) & (env[:-1] <= thresh)).sum())
    return {
        "seconds": round(len(x) / SR, 2),
        "rms_db": round(20 * np.log10(rms + 1e-12), 1),
        "crest_db": round(20 * np.log10(peak / (rms + 1e-12)), 1),
        "bpm": round(bpm_estimate(env, fps), 1),
        "onsets_per_sec": round(onsets / (len(x) / SR), 2),
        "centroid_hz": round(centroid),
        "bands": bands,
    }


def main():
    args = sys.argv[1:]
    opts = {"start-a": 0.0, "dur-a": None, "start-b": 0.0, "dur-b": None}
    files = []
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            opts[args[i][2:]] = float(args[i + 1])
            i += 2
        else:
            files.append(args[i])
            i += 1
    if not files:
        sys.exit(__doc__)

    a = metrics(load(files[0], opts["start-a"], opts["dur-a"]))
    out = {"a": {"file": files[0], **a}}
    if len(files) > 1:
        b = metrics(load(files[1], opts["start-b"], opts["dur-b"]))
        out["b"] = {"file": files[1], **b}
        out["delta"] = {
            "bpm": round(a["bpm"] - b["bpm"], 1),
            "onsets_per_sec": round(a["onsets_per_sec"] - b["onsets_per_sec"], 2),
            "centroid_hz": a["centroid_hz"] - b["centroid_hz"],
            "rms_db": round(a["rms_db"] - b["rms_db"], 1),
            "bands": {k: round(a["bands"][k] - b["bands"][k], 4) for k in a["bands"]},
        }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
