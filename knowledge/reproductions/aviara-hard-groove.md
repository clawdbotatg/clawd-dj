---
lesson: knowledge/lessons/aviara-hard-groove-techno.md
code: sandbox/repro/aviara-hard-groove.strudel
reference: learn/corpus/vAPX6g2eHgA/audio.m4a @ 555s–585s (9:15 full-groove section)
date: 2026-07-15
verdict: rhythm locked (tempo exact, kick band within 1%); tonal balance off where the frames were unreadable
---

# Reproduction: Aviara "Hard Groove Techno"

Second closed loop, first from an **unnarrated** video (build recipe inferred
from frames alone — no transcript existed).

## Adaptations from the lesson's final code

- Reconstructed the 9:12–9:48 full-groove layer set (bass + both kicks + both
  hat layers; toms out) from the timeline — the on-screen final state is the
  stripped outro.
- Sliders → ridden values from the timeline (`lpq 8.8`); `lpenv` guessed at 4
  (peaked at 8.9 only later, at 10:12); hats `lpf(2000)` (last readable value,
  final retype unreadable); boogie lpf guessed 1500 (was being swept 960→1590).
- `_scope()` stripped; outro-only `.fm(time)` excluded.
- `.bank("tr808")` needs `samples('https://strudel.b-cdn.net/tidal-drum-machines.json')`
  in @strudel/web (strudel.cc prebakes it; `github:ritchse/...` has no
  strudel.json at the repo root — the b-cdn manifest is the working URL).

## Measured (30s render vs 30s reference)

| metric | ours | YouTube | delta |
|---|---|---|---|
| BPM (est) | 74.9 | 74.9 | **0.0** (both half-time readings of 150) |
| onsets/sec | 3.26 | 3.73 | −0.47 |
| centroid | 959 Hz | 1804 Hz | −845 |
| RMS | −11.8 dB | −4.3 dB | −7.5 |
| sub / kick / bass | .22 / .34 / .32 | .39 / .35 / .18 | −.16 / **−.01** / +.15 |

## Interpretation

- Tempo locks exactly and the kick band matches within 1% — the groove is the
  groove.
- The misses map 1:1 onto the *known unreadable spots*: our −845Hz centroid and
  quiet high end = the hats/boogie filter values I had to guess (too dark);
  their +.16 sub = the 808 sub_kick sitting much hotter in their gain staging
  (and possibly a sidechain we didn't see). Our supersaw bass band is +.15 hot
  for the same reason in reverse.
- Same −7dB RMS mastering gap as the first reproduction — expected, not a code
  issue (their crest 7.9dB says heavy limiting).

## Loose ends

- Try hats/boogie lpf up around 4–6k and sub_kick postgain ~1.5, re-measure.
- The BPM estimator half-times fast four-on-the-floor; fine for comparison
  (consistent on both sides) but worth a doubling heuristic in analyze.py.
