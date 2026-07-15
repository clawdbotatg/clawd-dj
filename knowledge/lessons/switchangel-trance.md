---
source: https://www.youtube.com/watch?v=GWXCCBsOMSg
creator: Switch Angel
genre: trance
software: strudel
---

# Coding Trance Music (Full Narrated)

## Final code

```js
samples('http://localhost:5432')
setCpm(140/4)
// LET US TRANCE W/SWITCH ANGEL
_$: s("tbd:2!4").beat("0,4,8,11,14",16)._scope()

_$: n("<3@3 4 5 @3 6>*2".add("-14,-21")).scale("g:minor")
  .s("supersaw")
  // .trancegate(1.5,45,1).o(2)
  .seg(16)
  .rlpf(slider(0.877)).lpenv(2)

$: s("jcp:2!4").o(5).beat("0,4,8,11,14",16)

$: n("0@2 <-7 [-5 -2]>@3 <0 -3 2 1>@3".add(7)
    .add("<5 4 0 <0 2>>")
  )
  .scale("g:minor")
  .s("supersaw").trancegate(1.5,45,1).o(3)
  .delay(.7).pan(rand)
  .fm(.5).fmwave("brown")
  .rlpf(slider(0.88)).lpenv(2)._pianoroll()

$: s("pulse!16").dec(.1).fm(time).fmh(time).o(4)

$: s("jt:6").note("e2".add("<0 0 7 12 0>*8"))
  .scrub(rand.seg(16).rib(46,2))
  .delay(.8)
  .o(5)
```

Notes on fidelity:
- The video ends on a wind-down: in the final frame (t376, ~6:16) the kick and bass lines are muted (`_$:`) and the bass's `.trancegate(1.5,45,1).o(2)` is re-commented. The "full drop" state 16 seconds earlier (t360, ~6:00) had both unmuted and the trancegate active, with the kick still plain `$: s("tbd:2!4")._scope()` (no `.beat`) — the `.beat(...)` appears on the kick only in the final two frames.
- Line 1 of the file is never visible on screen (every frame starts at line 2, `samples(...)`); unknown whether anything is on it.
- The last line, `.o(5)`, is clipped at the bottom edge of the final frame; it is confirmed complete from t360/t368.
- `.rlpf(...)` is transcribed exactly as displayed on every frame that shows it. It is not a documented core Strudel name (docs use `lpf`); she loads a custom sample server (`samples('http://localhost:5432')`) and this may be a custom/renamed helper — but the screen consistently reads `rlpf`.
- Slider widget values are the last displayed: bass `slider(0.877)` (drifted .5 → 0.418 → 0.462 → 0.669 → 0.877 as she swept it), lead `slider(0.88)` (.5 → 0.593 → 0.723 → 0.828 → 0.88). The literal originally typed was `slider(.5)` in both.
- `"tbd:2!4"`, `"supersaw"`, `"g:minor"`, `"-14,-21"`, `"jcp:2!4"`, `"jt:6"`, `"e2"`, `"brown"`, `"pulse!16"` and several pattern numbers render as boxed widget chips in the REPL; underlying text is as transcribed.
- In the bass pattern `"<3@3 4 5 @3 6>*2"` there is a visible space between `5` and `@3` in every frame that shows it (t136 → t376); transcribed verbatim (narration says "three at three, four; five at three, six").
- Frames are missing for ~2:00–2:08, ~3:12, ~4:16–4:32, ~5:20 and ~5:36–5:44; changes in those windows are bracketed by the surrounding frames and narration.

## Build timeline

1. [0:00] Pre-existing scaffold: `samples('http://localhost:5432')` (custom local sample server), `setCpm(140/4)` (140 BPM, 4 beats/cycle), comment header `// LET US TRANCE W/SWITCH ANGEL`.
2. [0:00–0:09] "Fast trance kick drum, four on the floor, with scope" — `$: s("tbd:2!4")._scope()` (tbd sample #2, repeated 4x per cycle, oscilloscope inline).
3. [0:11–0:17] "Bass super saw controlled with trancegate. Cycle 45, one cycle long" — new line `$: n("0").s("supersaw").trancegate(1.5,45,1).o(2)` (by t32 split across two lines).
4. [0:21–0:27] "The key — it needs to be G minor" — `.scale("g:minor")` on the bass.
5. [0:33–0:37] "Drop one octave… two octaves" — `n("0".add(-14))` (7 scale degrees per octave; she lands on −14 = two octaves).
6. [0:40–0:48] "Filter controlled with a slider. An envelope of two" — `.rlpf(slider(.5)).lpenv(2)` appended to the bass.
7. [0:50–0:58] "A lead sound from our cloned bass. Instead of subtracting two, we'll add one octave" — the whole bass block is duplicated; the clone becomes the lead with `.add(7)` and `.o(3)`.
8. [1:04] "We need more power with delay" — `.delay(.7)` on the lead.
9. [1:08] "Make it swirl with random panning" — `.pan(rand)` on the lead.
10. [1:15–1:25] "Add more notes. Drop one octave for three eighth notes… go deeper by patterning inside of our pattern" — lead melody grows from `"0"` to `"0@2 -7@3 0@…"` (t80) to `"0@2 -7@3 <0 -3 2 1>@3"` (t88) to final `"0@2 <-7 [-5 -2]>@3 <0 -3 2 1>@3"` (t96) — an angle-bracket alternation nested inside the sequence.
11. [1:39–1:50] "Let's make a breakdown. First, visualize our lead with piano roll. Increase the power of our filter" — kick muted (`$:` → `_$:`), `._pianoroll()` appended to the lead, lead slider swept 0.5 → 0.593. Bass trancegate gets commented out (`// .trancegate(1.5,45,1).o(2)`) during the breakdown.
12. [1:54–2:04] "A percussion with our bass. Do half notes. Three at three, four; five at three, six" — bass note pattern replaced with `"<3@3 4 5 @3 6>*2"`.
13. [2:12–2:16] "Increase the power of our bass by layering one more octave below" — bass `.add("-14")` becomes `.add("-14,-21")` (stack: two octaves down + three octaves down).
14. [2:29–2:48] "We can make our lead follow our bass percussion" — a second transpose line added inside the lead's `n(...)`: `.add("<5 4 0 <2 -2>>")` (t160) revised to `<0 -2>` (t168) and finally `.add("<5 4 0 <0 2>>")` (t176).
15. [2:54–3:06] "An infinite riser. 16th-note pulse wave, decay short, FM with time, FM harmonics with time" — `$: s("pulse!16").dec(.1).fm(time).fmh(time).o(4)`.
16. [3:11–3:14] "Make our bass bounce in 16th-note segments" — `.seg(16)` inserted in the bass chain.
17. [3:21–3:32] "Add a vocal chop. Change the note to E. Scrub it randomly like a tape loop in 16th-note segments" — `$: s("jt:6").note("e2").scrub(rand.seg(16)).o(5)`.
18. [3:37–3:43] "Ribbon it and control the RNG of our chop. Two cycles long" — scrub becomes `.scrub(rand.seg(16).rib(46,2))`.
19. [3:49] "Add a delay" — `.delay(.7)` typed on the vocal, revised to `.delay(.8)` by t240.
20. [3:56] "Bring our kick back in" — kick unmuted (`_$:` → `$:`).
21. [4:04–4:08] "Let's do a clap to increase the harmonic cells" — `$: s("jcp:2!4").o(5)`.
22. [4:16–4:18] "Bring our trancegate back in on our bass for more power" — bass `.trancegate(1.5,45,1).o(2)` uncommented (visible active at t280).
23. [4:28–4:40] "We can FM our super saw with noise for more chaos. More chaos brings more power" — `.fm(.5).fmwave("brown")` added to the lead.
24. [4:54–5:04] "Change the beat of our kick to make it more exciting. Four eights. 11, 14 out of 16" — `.beat("0,4,8,11,14",16)` — typed onto the clap line (`$: s("jcp:2!4").o(5).beat("0,4,8,11,14",16)`); the same pattern lands on the kick line itself only at the very end (t368).
25. [5:28–5:52] "Add notes to our vocal pattern in a polymetric way" — vocal note becomes `.note("e2".add("<0 0 7 12 0>*8"))`: a 5-step transpose cycle running at 8 per cycle against the 16-segment scrub.
26. [6:00–6:16] Outro: the kick line gets `.beat("0,4,8,11,14",16)` inserted before `._scope()`, then kick and bass are muted (`_$:`) and the bass trancegate re-commented as the video ends.

## Techniques

- **Trance gate on a sustained supersaw** — the genre-defining rhythmic chopping of a held saw: `s("supersaw").trancegate(1.5,45,1)` (args narrated as gate speed/seed 45/one cycle long). She turns it off for the breakdown (comment the line) and back on for the drop — the trancegate itself is an arrangement switch.
- **Clone-the-bass lead** — duplicate the entire bass block and change only the transpose: bass `.add(-14)` → lead `.add(7)` ("instead of subtracting two, we'll add one octave"), plus its own orbit. Instant timbre-matched layer pair.
- **Patterning inside the pattern** — nest angle-bracket alternation inside a sequence for evolving melodies: `"0@2 <-7 [-5 -2]>@3 <0 -3 2 1>@3"` — each cycle picks the next option in each `<>` slot, so a one-bar riff mutates over 4 bars.
- **Stacked chord-tone transposes** — a second `.add("<5 4 0 <0 2>>")` inside `n(...)` re-roots the whole lead riff per cycle so the lead "follows" the bass progression; comma stacking in `.add("-14,-21")` plays the same line in parallel octaves for power.
- **Slider-ridden filter** — `.rlpf(slider(.5)).lpenv(2)` on both bass and lead: cutoff on an on-screen slider you sweep live (breakdown = close it, drop = open it; she parks bass at 0.877, lead at 0.88), with a fixed envelope of 2 for movement per note.
- **Bass-as-percussion** — during the breakdown the bassline is rewritten as sparse long notes (`"<3@3 4 5 @3 6>*2"`) then later chopped by `.seg(16)` to "bounce in 16th-note segments" — one voice serves as both riff and percussion depending on section.
- **Infinite time riser** — `s("pulse!16").dec(.1).fm(time).fmh(time)`: 16th-note pulse ticks whose FM index and harmonicity both ride the ever-increasing `time` signal, so it climbs forever without a reset point.
- **Tape-loop vocal chop** — `s("jt:6").note("e2").scrub(rand.seg(16).rib(46,2))`: scrub position driven by random values sampled 16x/cycle, frozen with `.rib(46,2)` (seed 46, 2-cycle loop) so the "random" chop repeats as a hook. `.delay(.8)` glues it.
- **Polymetric vocal melody** — `.note("e2".add("<0 0 7 12 0>*8"))`: a 5-element transpose cycle clocked at 8 steps/cycle over a 16-segment scrub — 5-against-8-against-16 keeps the chop evolving.
- **Noise-FM for chaos** — FM the supersaw lead with brown noise: `.fm(.5).fmwave("brown")` — "more chaos brings more power".
- **Beat-list groove** — `.beat("0,4,8,11,14",16)`: fire on beats 0, 4, 8, 11, 14 of a 16-grid — turns a straight `!4` clap/kick into a syncopated trance pattern ("four eights; 11, 14 out of 16").
- **Mute prefix as arrangement** — `_$:` mutes a line; she mutes the kick for the breakdown, unmutes for the drop, and mutes kick+bass for the outro.
- **Inline visualizers** — `._scope()` on the kick, `._pianoroll()` on the lead: live instrumentation inside the editor.

## Vocabulary

- `samples('http://localhost:5432')` — load a sample map from a (here: local/custom) server.
- `setCpm(140/4)` — set tempo in cycles per minute; 140/4 idiom = 140 BPM at 4 beats per cycle.
- `$:` / `_$:` — play an anonymous pattern line; leading `_` mutes it.
- `s("tbd:2!4")` — choose sound/sample: name:index, `!4` = repeat 4x per cycle (`"tbd"` kick, `"jcp"` clap, `"jt"` vocal, `"supersaw"`, `"pulse"` synths).
- `n("...")` — pattern of scale-degree numbers for the synth.
- `note("e2")` — pattern of absolute note names.
- `.add(7)` / `.add("-14,-21")` / `.add("<5 4 0 <0 2>>")` — transpose a number pattern; comma = stack (parallel layers), patternable per cycle.
- `.scale("g:minor")` — map degree numbers onto a scale (G minor — "the key").
- `.trancegate(1.5,45,1)` — rhythmic gate chopping a sustained sound (narrated: seed/"cycle 45", one cycle long).
- `.o(2)` — orbit: route to a numbered mixer bus (kick has no orbit; bass 2, lead 3, riser 4, clap+vocal 5).
- `.seg(16)` — sample a continuous/held value into N discrete events per cycle (16th notes).
- `.rlpf(slider(.5))` — lowpass-filter cutoff (as displayed on screen; see fidelity note) — here always fed by a slider.
- `slider(0.877)` — inline UI slider widget; the number is the current value, updated live as you drag.
- `.lpenv(2)` — lowpass filter envelope depth ("an envelope of two").
- `.delay(.7)` — echo/delay send ("more power with delay").
- `.pan(rand)` — stereo position from continuous random signal ("make it swirl").
- `rand` — continuous random signal 0–1.
- `.fm(.5)` / `.fm(time)` — FM index (brightness); patternable, accepts signals.
- `.fmh(time)` — FM harmonicity ratio; driven by `time` for the riser.
- `.fmwave("brown")` — FM modulator waveform; brown noise = chaos.
- `time` — monotonically rising elapsed-time signal — plug into params for infinite risers.
- `.dec(.1)` — envelope decay (short/plucky).
- `.scrub(...)` — playback-position scrubbing of a sample, "like a tape loop"; fed a signal for position.
- `.rib(46,2)` — "ribbon": freeze a random stream with seed 46 over a 2-cycle window so it loops.
- `.beat("0,4,8,11,14",16)` — trigger only on the listed beat numbers out of N per cycle.
- `!4` / `!16` — mini-notation repeat (4 or 16 events per cycle).
- `@3` — mini-notation duration weight (hold this step for 3 units — "three eighth notes").
- `<a b c>` — mini-notation alternation: one option per cycle; nestable ("patterning inside of our pattern").
- `[a b]` — mini-notation subgroup (fits multiple events into one step).
- `*2` / `*8` — mini-notation speed-up: run the bracketed cycle N times per cycle (source of the polymeter).
- `._scope()` — inline oscilloscope visual.
- `._pianoroll()` — inline pianoroll visual ("visualize our lead with piano roll").
