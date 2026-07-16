#!/usr/bin/env python3
"""clawd-dj practice room — watch/listen to the AI rehearse a reproduction.

Runs an iterate loop: render candidate headless -> measure vs the YouTube
reference -> ask the brain (claude -p, heuristic fallback) for an adjusted
candidate -> repeat. Every step is broadcast over SSE to practice/index.html,
which plays the current candidate aloud in the viewer's browser.

Usage:
  python3 practice/server.py                      # default: Aviara hard groove session
  python3 practice/server.py <code.strudel> <reference-audio> <ref-start> <ref-dur> [iters]

Then open http://<lan-ip>:8940/ and click once to join the audio.
Pure stdlib. Shells out to sandbox/render.mjs + sandbox/analyze.py.
"""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PORT = 8940
RENDER_SECS = 30
WARMUP = 5

# ---------- SSE hub ----------
CLIENTS = []          # list of queue-like lists guarded by LOCK
HISTORY = []          # every event ever sent, replayed to late joiners
LOCK = threading.Lock()


def broadcast(kind, **data):
    evt = {"kind": kind, "t": time.strftime("%H:%M:%S"), **data}
    line = f"data: {json.dumps(evt)}\n\n".encode()
    with LOCK:
        HISTORY.append(line)
        for q in CLIENTS:
            q.append(line)
    print(f"[{evt['t']}] {kind}: {data.get('msg', '')[:100]}", flush=True)


# ---------- practice loop ----------
def run(cmd, timeout=180):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)


def render_and_measure(code, ref, ref_start, ref_dur, tag):
    work = HERE / "work"
    work.mkdir(exist_ok=True)
    cf = work / f"{tag}.strudel"
    wav = work / f"{tag}.wav"
    cf.write_text(code)
    r = run(["node", "sandbox/render.mjs", str(cf), str(wav), str(RENDER_SECS), str(WARMUP)])
    if r.returncode != 0:
        try:
            msg = json.loads(r.stderr.strip().splitlines()[-1]).get("msg", r.stderr)
        except Exception:
            msg = (r.stderr or r.stdout)[-300:]
        return None, f"render failed: {msg}"
    a = run(["python3", "sandbox/analyze.py", str(wav), str(ref),
             "--start-b", str(ref_start), "--dur-b", str(ref_dur)])
    if a.returncode != 0:
        return None, f"analyze failed: {a.stderr[-300:]}"
    return json.loads(a.stdout), None


def score(delta):
    """Lower = closer to the reference. Loudness excluded (mastering, not code)."""
    return round(
        sum(abs(v) for v in delta["bands"].values())
        + abs(delta["centroid_hz"]) / 2000
        + abs(delta["onsets_per_sec"]) / 4, 4)


SCRUB = ("CLAUDECODE", "ANTHROPIC_API_KEY")


def brain_adjust(code, comparison, goal_note):
    """Ask claude -p for the next candidate. Returns (new_code, commentary) or (None, why)."""
    if not shutil.which("claude"):
        return None, "claude CLI not found"
    env = {k: v for k, v in os.environ.items()
           if k not in SCRUB and not k.startswith("CLAUDE_CODE_")}
    prompt = f"""You are a livecoding DJ rehearsing a Strudel reproduction of a YouTube track.
Current candidate code:
```
{code}
```
Measured against the reference recording (a = mine, b = reference, delta = a-b):
{json.dumps(comparison, indent=1)}
Session notes: {goal_note}

Adjust ONLY mix/filter/gain-ish parameters (lpf, hpf, postgain, gain, decay, lpenv, lpq, shape, velocity ranges) to shrink the deltas: negative band delta = that band is too quiet in mine; negative centroid = mine is too dark. Do not restructure patterns or change the tempo. Reply with exactly two parts separated by a line containing only ---:
1. One sentence saying what you changed and why (plain language, for a listener watching the rehearsal).
2. The COMPLETE adjusted Strudel code, no fences, no commentary."""
    if os.environ.get("DJ_BRAIN_CONFIG_DIR"):
        env["CLAUDE_CONFIG_DIR"] = os.environ["DJ_BRAIN_CONFIG_DIR"]
    try:
        # trusted-workspace cwd — see ask_brain
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                           timeout=180, env=env, cwd=os.environ.get("HOME", "/"))
    except subprocess.TimeoutExpired:
        return None, "brain timed out"
    if r.returncode != 0:
        return None, f"brain error: {(r.stderr or r.stdout)[-200:]}"
    out = r.stdout.strip()
    if "---" not in out:
        return None, f"brain reply unparseable: {out[:200]}"
    commentary, _, new_code = out.partition("---")
    new_code = new_code.strip().strip("`")
    if new_code.startswith("js\n"):
        new_code = new_code[3:]
    if len(new_code) < 40:
        return None, "brain returned no code"
    return new_code, commentary.strip()


def heuristic_adjust(code, comparison):
    """Dumb fallback: nudge every lpf literal toward the centroid delta."""
    import re
    d = comparison["delta"]["centroid_hz"]
    factor = 1.3 if d < -200 else (0.77 if d > 200 else 1.0)
    if factor == 1.0:
        return None, "heuristic: centroid close, nothing to nudge"
    def bump(m):
        return f"lpf({round(float(m.group(1)) * factor)})"
    new = re.sub(r"lpf\((\d+(?:\.\d+)?)\)", bump, code)
    return (new, f"heuristic: scaled fixed lpf values by {factor} (centroid delta {d}Hz)") \
        if new != code else (None, "heuristic: no fixed lpf literals to nudge")


def practice_session(code_path, ref, ref_start, ref_dur, max_iters):
    code = Path(code_path).read_text()
    goal_note = ("Rehearsing toward the reference groove. Loudness (rms_db) difference is "
                 "YouTube mastering - ignore it; match the band profile, centroid and onset density.")
    best = (None, float("inf"), 0)  # code, score, iteration
    broadcast("session", msg=f"practice session: {Path(code_path).name} vs {Path(ref).name} "
                             f"@{ref_start}s+{ref_dur}s, {max_iters} iterations max",
              code=code, iteration=0)
    for i in range(1, max_iters + 1):
        if STOP.is_set():
            broadcast("done", msg="rehearsal stopped from the booth")
            break
        broadcast("render", msg=f"iteration {i}: rendering {RENDER_SECS}s headless...", iteration=i)
        comparison, err = render_and_measure(code, ref, ref_start, ref_dur, f"iter{i}")
        if err:
            broadcast("error", msg=f"iteration {i}: {err}", iteration=i)
            if best[0] is None:
                break
            code = best[0]  # revert to best-known and let the brain try again
            continue
        s = score(comparison["delta"])
        broadcast("measure", msg=f"iteration {i}: score {s} (lower is closer)",
                  iteration=i, comparison=comparison, score=s, code=code)
        if s < best[1]:
            best = (code, s, i)
            broadcast("best", msg=f"iteration {i} is the closest match yet (score {s})",
                      iteration=i, score=s)
        if s < 0.15:
            broadcast("done", msg=f"converged at iteration {i} (score {s})", iteration=i)
            break
        if i == max_iters:
            break
        broadcast("think", msg=f"iteration {i}: asking the brain for an adjustment...", iteration=i)
        new_code, note = brain_adjust(code, comparison, goal_note)
        if new_code is None:
            broadcast("think", msg=f"brain unavailable ({note}); trying heuristic", iteration=i)
            new_code, note = heuristic_adjust(code, comparison)
        if new_code is None:
            broadcast("done", msg=f"no further adjustment available ({note})", iteration=i)
            break
        code = new_code
        broadcast("adjust", msg=note, iteration=i, code=code)
    if best[0]:
        out = HERE / "work" / "best.strudel"
        out.write_text(best[0])
        broadcast("done", msg=f"session over — best was iteration {best[2]} (score {best[1]}), "
                              f"saved to practice/work/best.strudel",
                  code=best[0], score=best[1])


# ---------- set mode: the brain crafts songs one layer at a time ----------
DIGEST = (ROOT / "knowledge/DIGEST.md")
VALIDATE_SECS = 6       # quick audition render per candidate

# The song-craft script: how the studied artists actually work — open sparse,
# add ONE layer at a time, let the full groove ride, break it down, drop it,
# then tear down into the next palette. (directive, hold_seconds_after_airing)
RIDE = ("The record rides. Make ONE subtle performance tweak in the spirit of the "
        "record — nudge a filter, vary one pattern slightly, swap one drum variant. "
        "Everything else stays byte-identical. Do NOT add or remove layers, and do "
        "NOT unmute any _$-muted line.")


def render_only(code, tag):
    """Fast validation render; returns (metrics|None, err)."""
    work = HERE / "work"
    work.mkdir(exist_ok=True)
    cf, wav = work / f"{tag}.strudel", work / f"{tag}.wav"
    cf.write_text(code)
    r = run(["node", "sandbox/render.mjs", str(cf), str(wav), str(VALIDATE_SECS), "2"])
    if r.returncode != 0:
        try:
            msg = json.loads(r.stderr.strip().splitlines()[-1]).get("msg", r.stderr)
        except Exception:
            msg = (r.stderr or r.stdout)[-300:]
        return None, msg
    a = run(["python3", "sandbox/analyze.py", str(wav)])
    if a.returncode != 0:
        return None, f"analyze failed: {a.stderr[-200:]}"
    return json.loads(a.stdout)["a"], None


def ask_brain(prompt, timeout=240):
    if not shutil.which("claude"):
        return None, "claude CLI not found"
    env = {k: v for k, v in os.environ.items()
           if k not in SCRUB and not k.startswith("CLAUDE_CODE_")}
    # brain calls can ride a different (cooler) subscription pool than the harness
    if os.environ.get("DJ_BRAIN_CONFIG_DIR"):
        env["CLAUDE_CONFIG_DIR"] = os.environ["DJ_BRAIN_CONFIG_DIR"]
    try:
        # cwd MUST be a trusted workspace: claude -p stalls on the trust gate in
        # untrusted dirs (practice/work froze every brain call under the daemon).
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                           timeout=timeout, env=env, cwd=os.environ.get("HOME", "/"))
    except subprocess.TimeoutExpired:
        return None, "brain timed out"
    if r.returncode != 0:
        return None, f"brain error: {(r.stderr or r.stdout)[-200:]}"
    return r.stdout.strip(), None


PERF = ROOT / "knowledge/crate/perf"
RISER_LINE = ('$riser: s("pulse*16").dec(.08).gain(saw.slow(8).range(.15,.5))'
              '.hpf(saw.slow(8).range(300,3000)).orbit(6)')


def load_perf_records():
    """Performance-form records: header `// title | genres: a,b | bpm: N | layers: l1 l2`,
    body has one $name: line per layer (verified against the original by render)."""
    recs = []
    for f in sorted(PERF.glob("*.strudel")):
        text = f.read_text()
        m = re.match(r"//\s*(.+?)\s*\|\s*genres:\s*([\w,\- ]+)\s*\|\s*bpm:\s*(\d+)\s*\|\s*layers:\s*(.+)",
                     text.splitlines()[0])
        if not m:
            continue
        recs.append({"file": f.name, "title": m.group(1),
                     "genres": [g.strip() for g in m.group(2).split(",")],
                     "bpm": int(m.group(3)), "layers": m.group(4).split(),
                     "code": text})
    return recs


def pick_record(records, genre, played):
    words = set(re.findall(r"[a-z]+", genre.lower()))
    fresh = [r for r in records if r["file"] not in played] or records
    scored = sorted(fresh, key=lambda r: -len(words & set(r["genres"])))
    top = len(words & set(scored[0]["genres"]))
    pool = [r for r in scored if len(words & set(r["genres"])) == top]
    import random
    return random.choice(pool)


def set_layers(code, active, riser=False):
    """The whole record stays in the program; exactly `active` layers are unmuted.
    Deterministic string surgery on verified code — the brain can't touch the floor."""
    out = []
    for line in code.splitlines():
        m = re.match(r"_?\$(\w+):", line)
        if m:
            bare = line[1:] if line.startswith("_") else line
            out.append(bare if m.group(1) in active else "_" + bare)
        else:
            out.append(line)
    if riser:
        out.append(RISER_LINE)
    return "\n".join(out)


def brain_craft_move(genre, record, plan, directive, code, feedback, recent):
    digest = DIGEST.read_text() if DIGEST.exists() else ""
    out, err = ask_brain(f"""You are a livecoding DJ mid-set, performing a known record live in Strudel — the 808-set style: the whole record lives in your program as labeled layers, and you perform by muting/unmuting and riding parameters. An audience is listening RIGHT NOW; your edit swaps in beat-aligned.

{digest}

THE RECORD you are performing — "{record['title']}" — its original code (your ground truth; keep layer code verbatim unless a directive says otherwise):
```
{record['code']}
```

YOUR PERFORMANCE PLAN (layer order):
{plan}

Recent moves: {json.dumps(recent[-4:], indent=0)}

THE PROGRAM PLAYING RIGHT NOW:
```
{code if code else '(a lean drum skeleton from the previous record, or silence at set open)'}
```

YOUR DIRECTIVE FOR THIS MOVE (do exactly this, nothing more):
{directive}
{feedback}

Respect every hard rule in the digest. Reply with exactly two parts separated by
a line containing only ---:
1. One short sentence, MC-style, telling the crowd what you just did.
2. The COMPLETE new Strudel program, no fences.""")
    if out is None:
        return None, None, err
    if "---" not in out:
        return None, None, f"unparseable reply: {out[:150]}"
    mc, _, new_code = out.partition("---")
    new_code = new_code.strip().strip("`")
    if new_code.startswith("js\n"):
        new_code = new_code[3:]
    if len(new_code) < 20:
        return None, None, "no code in reply"
    return new_code, mc.strip(), None


def band_change(a, b):
    """How audibly different two renders are (sum of abs band-share deltas)."""
    if not a or not b:
        return 1.0
    return sum(abs(a["bands"][k] - b["bands"][k]) for k in a["bands"])


def set_session(genre, minutes):
    total = minutes * 60
    t0 = time.time()
    code, move_n, song_n = None, 0, 0
    recent, played = [], []
    records = load_perf_records()
    if not records:
        broadcast("error", msg="no performance records in knowledge/crate/perf/")
        return
    broadcast("session", msg=f"SET MODE: {genre}, {minutes} minutes. Performing "
                             f"verified records from the crate ({len(records)} in the bag): "
                             "layer-by-layer builds, rides, breakdowns, drops. "
                             "The AI is on the decks.")
    while time.time() - t0 < total and not STOP.is_set():
        song_n += 1
        rec = pick_record(records, genre, played)
        played.append(rec["file"])
        L = rec["layers"]
        broadcast("session", msg=f"🎼 song {song_n}: \"{rec['title']}\" (~{rec['bpm']}bpm) — "
                                 f"layers: {', '.join(L)}")
        # deterministic performance script: (kind, active_layers, riser, mc_line, hold)
        script = []
        for i in range(1, len(L) + 1):
            kind = "open" if i == 1 else ("full" if i == len(L) else "layer")
            mc = {"open": f'pulling up "{rec["title"]}" — just the {L[0]}, let it breathe',
                  "layer": f"bringing in the {L[i-1]}",
                  "full": f"the {L[i-1]} completes it — full record, wall to wall"}[kind]
            script.append((kind, L[:i], False, mc, 30 + i * 4))
        script += [
            ("ride", None, False, None, 85),
            ("breakdown", L[1:], True, f"the {L[0]} drops out — riser winding up, hold on", 40),
            ("drop", L, False, f"THE DROP — {L[0]} slams back, everything wide open", 90),
            ("ride", None, False, None, 70),
            ("teardown", L[:2], False, "stripping to the bones — next record loading", 22),
        ]
        for kind, active, riser, mc, hold in script:
            if time.time() - t0 >= total or STOP.is_set():
                break
            move_n += 1
            if kind == "ride":
                # the one brain move: a subtle audited performance tweak on verified code
                broadcast("think", msg=f"move {move_n} (ride): feeling the groove...",
                          iteration=move_n)
                new_code, bmc, err = brain_craft_move(genre, rec, "", RIDE, code, "", recent)
                if new_code:
                    metrics, verr = render_only(new_code, f"set{move_n}")
                    if not verr and metrics.get("rms_db", -99) > -35:
                        code = new_code
                        recent.append(f"[ride] {bmc}")
                        broadcast("adjust", msg=f"🎧 {bmc}", iteration=move_n,
                                  code=code, mode="inplace")
                        STOP.wait(hold)
                        continue
                broadcast("think", msg=f"move {move_n}: ride skipped ({err or 'audition failed'}), "
                                       "letting the record speak", iteration=move_n)
                STOP.wait(hold / 2)
                continue
            code = set_layers(rec["code"], set(active), riser=riser)
            recent.append(f"[{kind}] {mc}")
            broadcast("adjust", msg=f"🎧 {mc}", iteration=move_n, code=code, mode="inplace")
            STOP.wait(hold)
    broadcast("done", msg=f"set over — {song_n} records, {move_n} moves. "
                          "Thank you and goodnight 🙏", code=code or "", mode="inplace")
    if code:
        (HERE / "work" / "last-set-final.strudel").write_text(code)


# ---------- session runner (one at a time, startable over HTTP) ----------
SESSION_BUSY = threading.Lock()
STOP = threading.Event()  # POST /stop -> current session winds down after its move


def start_set(genre, minutes):
    if not SESSION_BUSY.acquire(blocking=False):
        return False
    STOP.clear()

    def go():
        try:
            set_session(genre, minutes)
        except Exception as e:
            broadcast("error", msg=f"set crashed: {e}")
        finally:
            SESSION_BUSY.release()

    threading.Thread(target=go, daemon=True).start()
    return True


def start_session(code_path, ref, ref_start, ref_dur, iters):
    if not SESSION_BUSY.acquire(blocking=False):
        return False
    STOP.clear()

    def go():
        try:
            practice_session(code_path, ref, ref_start, ref_dur, iters)
        except Exception as e:  # a crashed session must not wedge the room
            broadcast("error", msg=f"session crashed: {e}")
        finally:
            SESSION_BUSY.release()

    threading.Thread(target=go, daemon=True).start()
    return True


def catalog():
    repros = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "sandbox/repro").glob("*.strudel"))
    refs = []
    for m in sorted((ROOT / "learn/corpus").glob("*/meta.json")):
        if not (m.parent / "audio.m4a").exists():
            continue
        meta = json.loads(m.read_text())
        refs.append({"path": str((m.parent / "audio.m4a").relative_to(ROOT)),
                     "title": meta.get("title", m.parent.name),
                     "duration": meta.get("duration")})
    return {"repros": repros, "refs": refs}


# ---------- HTTP ----------
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("cache-control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path == "/stop":
            if SESSION_BUSY.locked():
                STOP.set()
                broadcast("session", msg="🛑 stop requested — winding down after the current move")
                self._json({"ok": True})
            else:
                self._json({"ok": True, "note": "nothing running"})
            return
        if self.path == "/set":
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("content-length", 0))))
                genre = str(req.get("genre", "techno"))[:60]
                minutes = max(1, min(float(req.get("minutes", 15)), 120))
            except (ValueError, json.JSONDecodeError) as e:
                self._json({"error": str(e)}, 400)
                return
            if start_set(genre, minutes):
                self._json({"ok": True})
            else:
                self._json({"error": "a session is already running"}, 409)
            return
        if self.path != "/session":
            self.send_response(404)
            self.end_headers()
            return
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("content-length", 0))))
            code = (ROOT / req["code"]).resolve()
            ref = (ROOT / req["ref"]).resolve()
            if ROOT not in code.parents or ROOT not in ref.parents:
                raise ValueError("path outside project")
            if not code.exists() or not ref.exists():
                raise ValueError("no such file")
            args = (code, ref, float(req.get("start", 0)), float(req.get("dur", 30)),
                    max(1, min(int(req.get("iters", 6)), 20)))
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            self._json({"error": str(e)}, 400)
            return
        if start_session(*args):
            self._json({"ok": True})
        else:
            self._json({"error": "a session is already running"}, 409)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.send_header("cache-control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/player.html":
            body = (HERE / "player.html").read_bytes()
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.send_header("cache-control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/catalog":
            self._json(catalog())
        elif self.path == "/events":
            self.send_response(200)
            self.send_header("content-type", "text/event-stream")
            self.send_header("cache-control", "no-store")
            self.end_headers()
            q = []
            with LOCK:
                for line in HISTORY:
                    q.append(line)
                CLIENTS.append(q)
            try:
                while True:
                    while q:
                        self.wfile.write(q.pop(0))
                        self.wfile.flush()
                    time.sleep(0.3)
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                with LOCK:
                    if q in CLIENTS:
                        CLIENTS.remove(q)
        else:
            self.send_response(404)
            self.end_headers()


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def main():
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"practice room: http://{lan_ip()}:{PORT}/", flush=True)
    args = sys.argv[1:]
    if args:
        start_session(Path(args[0]), Path(args[1]), float(args[2]), float(args[3]),
                      int(args[4]) if len(args) > 4 else 6)
    else:
        broadcast("session", msg="room open — pick a track and reference above and start a session")
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
