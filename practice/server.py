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
    try:
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                           timeout=180, env=env, cwd=str(HERE / "work"))
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


# ---------- set mode: the brain plays an original set ----------
DIGEST = (ROOT / "knowledge/DIGEST.md")
MOVE_SECS = 75          # target seconds between moves (validation time counts)
VALIDATE_SECS = 8       # quick audition render per candidate


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


def phase_for(elapsed, total):
    k = elapsed / total
    if k < .12: return "intro — start sparse (kick, or kick+bass), leave headroom"
    if k < .35: return "build — layer one element in, raise energy a notch"
    if k < .5: return "peak — full groove, maximum filter aggression"
    if k < .62: return "breakdown — mute the kick, pads/riser carry it, tease the return"
    if k < .85: return "second peak — drop the kick back, everything in, biggest moment"
    return "outro — strip layers one per move, end on bass or kick alone"


def brain_move(genre, phase, code, history, feedback):
    if not shutil.which("claude"):
        return None, None, "claude CLI not found"
    env = {k: v for k, v in os.environ.items()
           if k not in SCRUB and not k.startswith("CLAUDE_CODE_")}
    digest = DIGEST.read_text() if DIGEST.exists() else ""
    prompt = f"""You are a livecoding DJ playing an original {genre} set in Strudel, live, right now.

{digest}

SET STATE — phase: {phase}
Moves so far (oldest first): {json.dumps(history[-6:], indent=0)}
Currently playing:
```
{code if code else '(nothing yet — this is your opening move)'}
```
{feedback}

Make ONE DJ move: evolve the current program (add/remove/mutate a layer or two,
tweak filters/energy) to fit the phase. Stay in genre and tempo; keep it groovy,
not busy. Respect every hard rule in the digest. Reply with exactly two parts
separated by a line containing only ---:
1. One short sentence, MC-style, telling the crowd what you're doing.
2. The COMPLETE new Strudel program (the whole track, all layers), no fences."""
    try:
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                           timeout=240, env=env, cwd=str(HERE / "work"))
    except subprocess.TimeoutExpired:
        return None, None, "brain timed out"
    if r.returncode != 0:
        return None, None, f"brain error: {(r.stderr or r.stdout)[-200:]}"
    out = r.stdout.strip()
    if "---" not in out:
        return None, None, f"unparseable reply: {out[:150]}"
    mc, _, new_code = out.partition("---")
    new_code = new_code.strip().strip("`")
    if new_code.startswith("js\n"):
        new_code = new_code[3:]
    if len(new_code) < 30:
        return None, None, "no code in reply"
    return new_code, mc.strip(), None


def set_session(genre, minutes):
    total = minutes * 60
    t0 = time.time()
    code, history, move_n = None, [], 0
    broadcast("session", msg=f"SET MODE: {genre}, {minutes} minutes. The AI is on the decks.")
    while time.time() - t0 < total:
        move_n += 1
        phase = phase_for(time.time() - t0, total)
        broadcast("think", msg=f"move {move_n}: composing ({phase.split(' — ')[0]})...", iteration=move_n)
        feedback = ""
        candidate = None
        for attempt in range(3):
            new_code, mc, err = brain_move(genre, phase, code, history, feedback)
            if new_code is None:
                broadcast("error", msg=f"move {move_n}: {err}", iteration=move_n)
                break
            metrics, verr = render_only(new_code, f"set{move_n}")
            if verr:
                feedback = f"Your previous attempt FAILED validation: {verr}. Fix it."
                broadcast("think", msg=f"move {move_n}: candidate failed audition "
                                       f"({verr[:80]}), retrying...", iteration=move_n)
                continue
            if metrics.get("rms_db", -99) < -35:
                feedback = ("Your previous attempt rendered near-silence "
                            f"({metrics.get('rms_db')}dB RMS). Check labels ($:) and gains.")
                broadcast("think", msg=f"move {move_n}: candidate was silent, retrying...",
                          iteration=move_n)
                continue
            candidate = (new_code, mc, metrics)
            break
        if candidate is None:
            if code is None:
                broadcast("error", msg="couldn't produce an opening move; set aborted")
                return
            broadcast("think", msg=f"move {move_n}: keeping the current groove running",
                      iteration=move_n)
        else:
            code, mc, metrics = candidate
            history.append(mc)
            broadcast("adjust", msg=f"🎧 {mc}", iteration=move_n, code=code,
                      comparison=None, score=None)
            broadcast("measure", msg=f"move {move_n} on air — {metrics['bpm']}bpm-ish, "
                                     f"{metrics['rms_db']}dB, centroid {metrics['centroid_hz']}Hz",
                      iteration=move_n)
        # hold the groove until the next move slot
        elapsed_this = 0  # brain+validation already burned real time; top up to MOVE_SECS
        remaining = MOVE_SECS - (time.time() - t0) % MOVE_SECS
        time.sleep(max(10, min(remaining, MOVE_SECS)))
    broadcast("done", msg=f"set over — {move_n} moves, thank you and goodnight 🙏",
              code=code or "")
    if code:
        (HERE / "work" / "last-set-final.strudel").write_text(code)


# ---------- session runner (one at a time, startable over HTTP) ----------
SESSION_BUSY = threading.Lock()


def start_set(genre, minutes):
    if not SESSION_BUSY.acquire(blocking=False):
        return False

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
