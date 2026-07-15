#!/usr/bin/env python3
"""Fetch a livecoding YouTube video into a study corpus.

Usage: python3 learn/fetch.py <youtube-url-or-id> [--interval SECS]

Produces learn/corpus/<video-id>/
  meta.json        title/channel/duration/url
  captions.vtt     raw auto-captions (if available)
  transcript.txt   deduped plain-text transcript with [mm:ss] timestamps
  frames/tNNNN.png one frame every --interval seconds (default 8), near-dup frames dropped

The corpus is what the study step reads: a vision-capable agent walks frames/ in
order (code state over time) alongside transcript.txt (the DJ narrating why) and
writes a lesson into knowledge/.

Needs: yt-dlp, ffmpeg on PATH.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
    if m:
        return m.group(1)
    if re.fullmatch(r"[\w-]{11}", url):
        return url
    sys.exit(f"can't parse a video id out of {url!r}")


def dedupe_vtt(vtt_path: Path) -> str:
    """YouTube auto-captions repeat each line across rolling cues; keep first sightings, stamped."""
    lines, seen = [], set()
    stamp = "0:00"
    for raw in vtt_path.read_text(errors="replace").splitlines():
        m = re.match(r"(\d+):(\d+):(\d+)\.\d+ --> ", raw)
        if m:
            h, mnt, s = int(m[1]), int(m[2]), int(m[3])
            stamp = f"{h * 60 + mnt}:{s:02d}"
            continue
        text = re.sub(r"<[^>]+>", "", raw).strip()
        if not text or text in ("WEBVTT",) or text.startswith(("Kind:", "Language:")):
            continue
        if text in seen:
            continue
        seen.add(text)
        lines.append(f"[{stamp}] {text}")
    return "\n".join(lines) + "\n"


def main():
    args = sys.argv[1:]
    interval = 8
    if "--interval" in args:
        i = args.index("--interval")
        interval = int(args[i + 1])
        del args[i : i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    vid = video_id(args[0])
    url = f"https://www.youtube.com/watch?v={vid}"
    out = CORPUS / vid
    frames = out / "frames"
    frames.mkdir(parents=True, exist_ok=True)

    print(f"[{vid}] metadata + captions ...")
    meta_raw = run(["yt-dlp", url, "--no-download", "--print",
                    "%(.{id,title,channel,duration,upload_date,view_count})j"]).stdout.strip()
    (out / "meta.json").write_text(json.dumps({**json.loads(meta_raw), "url": url}, indent=2) + "\n")

    subprocess.run(["yt-dlp", url, "--write-auto-subs", "--write-subs", "--sub-langs", "en",
                    "--skip-download", "-o", str(out / "captions")],
                   check=True, capture_output=True)
    vtts = sorted(out.glob("captions*.vtt"))
    if vtts:
        vtts[0].rename(out / "captions.vtt")
        for extra in vtts[1:]:
            extra.unlink()
        (out / "transcript.txt").write_text(dedupe_vtt(out / "captions.vtt"))
        print(f"[{vid}] transcript: {len((out / 'transcript.txt').read_text().splitlines())} lines")
    else:
        print(f"[{vid}] no captions available")

    print(f"[{vid}] video ...")
    mp4 = out / "video.mp4"
    if not mp4.exists():
        subprocess.run(["yt-dlp", url, "-f", "bv*[height<=720]/bv*", "-o", str(mp4)],
                       check=True, capture_output=True)

    print(f"[{vid}] frames every {interval}s ...")
    for old in frames.glob("*.png"):
        old.unlink()
    # one frame per interval, named by its timestamp so it aligns with the transcript
    dur = int(float(json.loads((out / "meta.json").read_text()).get("duration") or 0))
    for t in range(0, max(dur, interval), interval):
        run(["ffmpeg", "-y", "-ss", str(t), "-i", str(mp4), "-frames:v", "1",
             str(frames / f"t{t:05d}.png")])

    # drop near-duplicate consecutive frames (idle stretches) by size-similarity heuristic
    prev = None
    kept = dropped = 0
    for f in sorted(frames.glob("*.png")):
        size = f.stat().st_size
        if prev is not None and abs(size - prev) < prev * 0.005:
            f.unlink()
            dropped += 1
            continue
        prev = size
        kept += 1
    mp4.unlink()  # keep the corpus light; refetch if ever needed
    print(f"[{vid}] done: {kept} frames kept, {dropped} near-dups dropped -> {out}")


if __name__ == "__main__":
    main()
