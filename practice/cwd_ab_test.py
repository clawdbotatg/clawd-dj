import os, subprocess, time
from pathlib import Path
digest = Path("knowledge/DIGEST.md").read_text()
prompt = f"""You are a livecoding DJ planning song #1 of an original melodic house set in Strudel.

{digest}

Previous songs in this set (avoid repeating their palettes/keys):
(none — this is the opener)

Write a SONG PLAN, max 10 lines of plain text: a name; the BPM; the key/scale;
the palette (which whitelisted sounds you'll use for kick/bass/hats/melodic/texture);
and the layer order you'll build in (first layer -> last). Make it a DIFFERENT
palette and key than the previous songs. No code yet. Reply with only the plan."""
env = {"HOME": os.environ["HOME"], "USER": os.environ["USER"],
       "PATH": "/Users/austingriffith/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin",
       "CLAUDE_CONFIG_DIR": os.environ["HOME"] + "/.clawd-accounts/slop"}
for cwd, label in [("practice/work", "A: cwd=practice/work"), (os.environ["HOME"], "B: cwd=$HOME")]:
    t = time.time()
    try:
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True,
                           timeout=90, env=env, cwd=cwd)
        print(f"{label}: {time.time()-t:.1f}s rc={r.returncode} out={r.stdout[:80]!r} err={r.stderr[:120]!r}")
    except subprocess.TimeoutExpired:
        print(f"{label}: TIMEOUT at {time.time()-t:.0f}s")
