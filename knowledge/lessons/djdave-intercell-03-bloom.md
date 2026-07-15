---
source: https://www.youtube.com/watch?v=6--6xVkJINc
creator: DJ_Dave
genre: live-coded electronic / techno (with live vocals)
software: Sonic Pi (inferred — see note below; code never legible on screen)
---

# Intercell EP Live Coded: Part 03 - Bloom

## Final code

**NOT RECOVERABLE FROM THIS VIDEO.** This is a cinematically shot warehouse
performance film (Part 03 of DJ_Dave's "Intercell EP Live Coded" series), not a
screen capture. The code appears only two ways, both illegible:

1. **Wall projection** — the full editor is projected floor-to-ceiling behind
   her (visible ~0:08–0:56 and ~2:08 in wide shots): a dark-theme editor with a
   large stencil title reading "BL...M" (almost certainly **BLOOM**), two
   columns of code — indented blocks with bright/white highlighted lines on the
   left-center and a magenta/pink-highlighted block of ~10 lines lower right
   (the pink flash is consistent with Sonic Pi's run-highlight and her known
   Sonic Pi setup). Even at 3x upscale + contrast enhancement the projected
   glyphs blur into bars; not one token is readable.
2. **Laptop screen** — close-ups (~0:40, 2:16–2:32) show the same dark UI at a
   steep angle: a left buffer, a right-hand column of short indented code
   lines, and a bright white/pink panel below it. Layout matches Sonic Pi's
   dark mode (code buffer + log/scope panels), but again no readable text.

Software note: recorded as **Sonic Pi** on the strength of (a) DJ_Dave's
well-documented toolchain — she is one of the best-known Sonic Pi performers
and the Intercell EP was written/performed in Sonic Pi — and (b) the dark
editor with magenta run-flash visible in projection and laptop shots. Treat as
high-confidence inference, not on-screen verification.

The near-empty auto-captions confirm there is no tutorial narration: the only
caught words are sung lyrics ("I changed myself" ~0:28) and one stray "undo"
(~2:03).

## Build timeline

Timeline of the *performance* (what the camera shows), since the code build is
not observable:

1. [0:00] Wide shot of the warehouse (Intercell-branded show). The full code
   buffer for "Bloom" is already on the projection wall — the piece starts
   from substantially pre-written code, not a blank buffer.
2. [0:08–0:24] Projection shows the "BLOOM" title graphic + two columns of
   code; highlighted (executing) line-blocks are visible. Track is already
   grooving — she is triggering/mutating existing blocks rather than typing
   from scratch.
3. [0:24–0:40] Close-ups: she sings into a handheld mic ("I changed myself" —
   Bloom's vocal hook) while standing behind a Pioneer CDJ + DJM-style mixer
   rig with a laptop to the side. Live vocals over the live-coded backing.
4. [0:40–0:56] She works the mixer (EQ/filter/FX knobs) with one hand, mic in
   the other — hardware mixing layered on top of the code performance.
5. [1:04–1:28] Peak section: the projection switches from code to full-wall
   generative strobing visuals (purple/pink grid patterns) synced to the music;
   audience seated on the floor watching.
6. [1:36–1:56] More vocal close-ups; she alternates mic and mixer.
7. [2:00–2:32] Back to the laptop: dark editor visible on screen and wall
   (auto-caption catches "undo" here — plausibly a live code revert). She
   leans into the laptop/mixer for a transition.
8. [2:40–3:04] Projection becomes organic fiery "bloom" imagery (flowering,
   molten textures) for the final section — visuals track the arc of the song.
9. [3:04–3:19] Outro: she rides the mixer as the track winds down; end card
   with the DAVE logo at 3:20.

## Techniques

Code-level techniques are not extractable; performance-architecture techniques
are:

- **Pre-written buffer, live execution** — for a produced EP track performed
  live, the whole code sits in the editor before the set; performance = firing,
  muting, and editing blocks (the moving highlight bars in projection), not
  live-typing from zero. The opposite end of the spectrum from a from-scratch
  build like Switch Angel's.
- **Hybrid rig: live code + DJ hardware** — Sonic Pi laptop feeds a Pioneer
  mixer (CDJ + DJM on a road case); broad strokes come from code, continuous
  gestures (EQ sweeps, filter, FX, level rides) come from hardware knobs. This
  gets around live coding's weakness at smooth parameter rides.
- **Live vocals over live code** — handheld mic, sung hooks on top of the
  generated track; the code carries the instrumental so both hands/voice are
  free between edits.
- **Code as stage design** — the editor is the backdrop: full-wall projection
  of the running buffer with a giant track-title header ("BLOOM") typed into
  the buffer as display text, alternating with generative visuals for peaks
  and outros. Audience-facing code is part of the show even when nobody can
  read every token.
- **Undo as performance move** — the one non-lyric word captioned is "undo"
  (~2:03): reverting an edit is a legitimate live transition tool.

## Vocabulary

No API vocabulary recoverable (no legible code). Contextual vocabulary:

- **Sonic Pi** — Ruby-based live-coding environment (`live_loop`s, samples,
  synths) that DJ_Dave performs in; dark-mode editor flashes the executed
  block, which is the highlight seen in projection.
- **Intercell EP** — the DJ_Dave release this series performs track-by-track;
  "Bloom" is Part 03.
- **Buffer** — a Sonic Pi editor tab holding the track's code; here fully
  pre-written and mutated live.
- **CDJ / DJM (Pioneer)** — DJ deck + mixer hardware used downstream of the
  laptop for EQ/FX/level performance.
