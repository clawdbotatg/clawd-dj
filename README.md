# clawd-dj

An AI DJ. Browser livecoding systems (Strudel — TidalCycles-in-JS at
[strudel.cc](https://strudel.cc)) have gotten good enough that a whole track is
just text: an LLM can write it, rewrite it live, and take a crowd through a set.
This repo is the work toward an AI that can DJ an event.

Two tracks of work:

## 1. `dj/` — play: full control + observability over live beats

A browser harness around Strudel where the AI has the same instrument a human
livecoder has: evaluate a pattern, layer it, sweep a filter, drop the kick,
bring it back. Requirements: programmatic evaluate/stop from JS, smooth
pattern-to-pattern transitions, and enough observability (current code, cycle
position, what's audible) that the DJ brain can reason about the set.

## 2. `learn/` + `knowledge/` — study the human DJs

The livecoding DJs on YouTube (Switch Angel, DJ_Dave, Dan Gorelick, ...) narrate
*how* they build tracks while the code is on screen. That's a complete lesson —
we just have to extract it:

- `learn/fetch.py <youtube-url>` → `learn/corpus/<id>/` with a timestamped
  `transcript.txt` (the *why*, from auto-captions) and `frames/tNNNNN.png`
  every 8s (the *what*: code state over time, read verbatim by a vision agent).
- A study agent walks the corpus and writes `knowledge/lessons/<slug>.md`:
  final code, build timeline, reusable techniques, vocabulary.
- The lessons become the DJ brain's style corpus: it doesn't imitate one
  pattern, it learns the *build-up recipes* (start with a kick + scope, layer a
  scale-locked bass, sweep `lpenv`, sidechain-`duck` everything, drop at 32).

`learn/corpus/` is gitignored (refetchable, heavy); `knowledge/` is committed —
it's the distilled asset.

## 3. `sandbox/` — reproduce and *hear* the difference

The feedback loop the DJ brain needs: render any Strudel code headless
(`sandbox/render.mjs code.strudel out.wav [secs]` — taps the real audio graph,
so the WAV is exactly what speakers would get) and measure it
(`sandbox/analyze.py mine.wav ref.m4a --start-b 170 --dur-b 30` — BPM via
onset autocorrelation, onset density, band energy profile, centroid, RMS).
`knowledge/reproductions/` holds the compare reports; first one matched the
studied track at **exactly 139.7 BPM with band profile within a few percent**,
and the deltas correctly fingered the one piece of code the frames never
showed.

## 4. `practice/` — the venue

`practice/server.py` serves the practice room on **:8940** (LAN): watch/listen
while the AI rehearses reproductions against references, or hit **play a set**
and it performs original music — every move composed by `claude -p` with the
`knowledge/DIGEST.md` cheat sheet, auditioned in the sandbox before airing, and
crossfaded between two Strudel decks in your browser. Runs as a launchd daemon
(`com.clawd.dj-practice`, logs at `/tmp/clawd-dj-practice.log`):

```
launchctl load ~/Library/LaunchAgents/com.clawd.dj-practice.plist   # install/start
launchctl list | grep clawd.dj                                      # status
```

## Status

- [x] fetch pipeline proven (transcript + frames legible, code recoverable verbatim)
- [x] first lessons in `knowledge/lessons/` (acid, trance, house, ...)
- [x] `dj/` deck page (`window.dj` API; `dj/probe.mjs` passes headless)
- [x] `sandbox/` render + analyze + first faithful reproduction
- [ ] DJ brain loop (LLM writes/revises the pattern on a schedule)
- [ ] the event

Needs `yt-dlp` + `ffmpeg` (`brew install yt-dlp ffmpeg`).
