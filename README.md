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

## Status

- [x] fetch pipeline proven (transcript + frames legible, code recoverable verbatim)
- [ ] first lessons in `knowledge/lessons/`
- [ ] `dj/` Strudel harness page
- [ ] DJ brain loop (LLM writes/revises the pattern on a schedule)
- [ ] the event

Needs `yt-dlp` + `ffmpeg` (`brew install yt-dlp ffmpeg`).
