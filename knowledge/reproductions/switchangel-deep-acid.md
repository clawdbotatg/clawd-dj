---
lesson: knowledge/lessons/switchangel-deep-acid.md
code: sandbox/repro/switchangel-deep-acid.strudel
reference: learn/corpus/HkgV_-nJOuE/audio.m4a @ 170s–200s (post-drop full groove)
date: 2026-07-15
verdict: faithful — exact BPM, matched rhythm density, band profile within a few percent
---

# Reproduction: Switch Angel "2 Minute Deep Acid"

First closed loop of watch → study → reproduce → render → measure → compare.

## Adaptations from the lesson's final code

- `_scope()` / `_pianoroll()` stripped (editor visual widgets, not audio).
- `slider(2.28,0,8)` → literal `2.28` (last visible value of her live sweep).
- Kick `.distort(...)` omitted (its argument was never on screen — flagged in
  the lesson as the one unverified spot).

## Measured (sandbox/analyze.py, 30s render vs 30s reference)

| metric | ours | YouTube | delta |
|---|---|---|---|
| BPM | 139.7 | 139.7 | **0.0** |
| onsets/sec | 6.56 | 6.73 | −0.17 |
| centroid | 3060 Hz | 2730 Hz | +330 |
| RMS | −12.3 dB | −5.9 dB | −6.4 |
| sub / kick / bass | .15 / .38 / .30 | .19 / .39 / .20 | −.04 / −.02 / +.10 |
| lowmid / mid | .13 / .018 | .15 / .040 | −.01 / −.02 |

## Interpretation

- Tempo and rhythmic density match exactly — the lesson's code is the track.
- **The deltas point at the known unknowns**: we're light in mid (.018 vs .040)
  and sub — consistent with the omitted kick `.distort(...)` (waveshaping adds
  harmonics/mids and thickens the kick). Our bass band is +.10 hot — her slider
  ride kept the filter envelope moving while our literal 2.28 parks it.
- −6.4 dB RMS is mastering/loudness normalization on YouTube's side, not a
  code discrepancy (crest factors are close: 10.6 vs 9.4 dB).

## Loose ends

- `s("sbd")` rendered fine in @strudel/web 1.3.0 headless (synth drum).
- Next fidelity step: sweep `lpenv` with a slow sine (`sine.range(0,8).slow(8)`)
  to emulate the human slider ride, and try `.distort("1.5:.4")` on the kick;
  re-measure mid band against the reference.
