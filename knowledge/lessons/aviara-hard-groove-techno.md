---
source: https://www.youtube.com/watch?v=vAPX6g2eHgA
creator: Aviara
genre: hard groove techno
software: strudel
---

# Livecoding Hard Groove Techno in Strudel from Scratch

**No narration:** this video is music-only livecoding (verified by transcribing the audio locally — whisper finds zero speech). All reasoning in the timeline below is inferred from what the code does, not from spoken explanation. The corpus also had no transcript.txt.

## Final code

State at the last frame (11:24) — the video ends in a stripped-down outro with most layers commented out; the commented lines are exactly as they appear on screen.

```js
setCps(150/60/4)
samples('github:tidalcycles/dirt-samples')

const bass_pattern = "e2 f2 ~ g#1 ~ a1 f2 ~"

let main_bass =
  // note(bass_pattern)
  note("e1(5,8)")
  .sound("supersaw")
  .sustain(0.3)
  .release(0.1)
  .shape(0.3)
  .lpf(perlin.range(200, 1000).slow(4))
  .lpq(slider(8.831, 3, 10))
  .lpenv(slider(1, 1, 12))
  .room(.1)
  .jux(rev)
  .postgain(1)
  .fm(time)
  ._scope()

let sub_kick = s("bd:3!4").bank("tr808")
  .shape(.6)
  .sustain(.8)
  .hpf(80)
  .postgain(1)
  ._scope()

let main_kick = s("<[sbd!3 [sbd sbd]] [sbd!2 [sbd sbd] sbd]>").lpf(742)
  ._scope()

let hats = s("white!8").decay(.07).lpf(2000).delay(.2)
  .sometimesBy(".3", x=>x.s("oh | hh"))
  .velocity(perlin.range(.5, 1.7))
  ._scope()

const low_tom = s("~ ~ lt ~ lt ~ ~ ~")
  .lpf(1000)
  .pan(.6)
  .postgain(1)

const mid_tom = s("~ ~ ~ mt  ~ ~ mt [~ mt]")
  .lpf(2500)
  .pan(.3)
  .postgain(.9)

const high_tom = s("ht ht ~ ~ ht ~ [ht ht] ~ ")
  .hpf(300)
  .pan(.8)
  .postgain(.8)

let toms = stack(
  low_tom,
  mid_tom,
  high_tom
).delay(.3)

let boogie_woogie = s("hh:1 * 8, oh:4 * 4").decay(.05)
  .delay(.2)
  .speed(perlin.range(1, 2).slow(8))
  .velocity(perlin.range(.5, 1.5)).postgain(1)
  .lpf(slider(0, 0, 10000))

track: stack(
  main_bass,
  sub_kick,
  // main_kick,
  // hats,
  // boogie_woogie,
  // toms
)
  // .hpf(slider(852, 0, 3000))
```

Notes on fidelity:
- **hats `.lpf(2000)` is the one real uncertainty.** At 9:48 (the last frame that shows the hats line) the value is mid-retype — the screen reads `lpf(000)` with the cursor before the zeros, i.e. the leading digit(s) were being typed and are unreadable. 2000 is the last fully-visible value (9:24); the final value may be different. A `.postgain(1.2)` that briefly existed on hats (9:24) is deleted by 9:48.
- Slider last-visible values: bass `lpq` = **8.831** (range 3–10), bass `lpenv` = **1** (dragged back down from a peak of 8.931 at 10:48; range 1–12), boogie_woogie `lpf` = **0** (range 0–10000), master `.hpf` comment preserves **852** (range 0–3000). Sliders are performance controls — these are end-of-video positions, not "the" values.
- At 4:48 the master hpf slider briefly displays `153302` — almost certainly a display artifact for ~1533.02; flagged verbatim.
- toms/boogie_woogie/track sections were last verified in full at 10:24–11:00; the very last two frames only show the top of the file (main_bass edits). Everything below main_bass is reconstructed from those 10:24–11:00 views.
- `bd:3`, `tr808`, `white`, `oh`, `hh`, `sbd`, `e1(5,8)`, `.3`, `hh:1`, `oh:4`, `8`, `4`, `supersaw`, `g#1` render as boxed widget chips in the REPL; underlying text is as transcribed.
- The mid_tom pattern really has a double space (`"~ ~ ~ mt  ~ ~ mt [~ mt]"`) and high_tom has a trailing space — transcribed verbatim.

## Build timeline

All reasoning inferred (no narration).

1. [0:00] Pre-existing scaffold before play is pressed: `setCps(150/60/4)` (150 BPM, 4 beats/cycle), `samples('github:tidalcycles/dirt-samples')`, a written bassline `const bass_pattern = "e2 f2 ~ g#1 ~ a1 f2 ~"`, and `main_bass` = `note(bass_pattern).sound("supersaw").sustain(0.3).release(0.1).shape(0.3).lpf(perlin.range(200,1000).slow(4)).lpq(slider(9.02,3,10)).lpenv(slider(1,1,12)).room(.1).postgain(1)._scope()`, played via `track: stack(main_bass)`. Bass-first: the groove is built on top of a moving supersaw bass whose cutoff drifts by perlin noise.
2. [0:12–0:36] Sub kick: `let sub_kick = s("bd:3!4").bank("tr808").shape(.6).sustain(.8).hpf(80).postgain(1)._scope()` — an 808 kick four-to-the-floor, driven into `.shape` for saturation, high-passed at 80 Hz so it's a mid-punch layer, not sub mud. Added to the `track: stack(...)`.
3. [0:48–1:12] Main kick as a two-bar alternation: `let main_kick = s("<[sbd!3 [sbd sbd]] [sbd!2 [sbd sbd] sbd]>").lpf(742)` — the hard-groove signature: a syncopated, shuffling kick pattern built from `sbd` (synth kick) with `<>` alternating two different bar-long groupings. Low-passed at 742 Hz to sit under the 808.
4. [1:24–2:00] Hats from noise: `let hats = s("white!8").decay(.07).lpf(2000).delay(.2)` — eight white-noise ticks per cycle with a tiny decay = synthesized closed hats, then `.sometimesBy(".3", x=>x.s("oh | hh"))` — 30% of events are randomly swapped to a real open-hat or closed-hat sample (`|` = random choice).
5. [2:12] Scrolls to top and rides the bass sliders (`lpq` 9.02→6.8, `lpenv` 1→3.4) — filter-envelope performance on the bass while the beat runs.
6. [2:24] Humanize the hats: `.velocity(perlin.range(.5, 1.7))` — continuous perlin wobble of hit loudness.
7. [2:24–4:00] Tom section, one voice at a time, each EQ'd and panned to its own spot in the stereo field:
   - `const low_tom = s("~ ~ lt ~ lt ~ ~ ~").lpf(1000).pan(.6).postgain(1)`
   - `const mid_tom = s("~ ~ ~ mt  ~ ~ mt [~ mt]").lpf(2500).pan(.3).postgain(.9)`
   - `const high_tom = s("ht ht ~ ~ ht ~ [ht ht] ~ ").hpf(300).pan(.8).postgain(.8)`
   Interlocking 8-step rest-heavy patterns — the percussive "groove" conversation over the kick.
8. [4:00–4:12] Group them: `let toms = stack(low_tom, mid_tom, high_tom).delay(.2)` — one shared delay send on the whole tom bus. Added to the track (initially commented, then in at 4:48).
9. [4:12–4:36] Master filter as a performance macro: the track's closing `)` gets `.hpf(slider(0, 0, 3000))` — a high-pass over the ENTIRE mix, then it's swept (4:48 shows it mid-sweep) for a DJ-style filter build; commented back out at 5:12 when done.
10. [5:12–6:24] Second hat layer: `let boogie_woogie = s("hh:1 * 8, oh:4 * 4").decay(.05)` — closed hats at 8/cycle stacked (comma) with open hats at 4/cycle — then `.delay(.2)`, `.speed(perlin.range(1, 2).slow(8))` (slow perlin pitch/rate drift), `.velocity(perlin.range(.5, 1.5)).postgain(1)`, and its own `.lpf(slider(10000, 0, 10000))` filter macro.
11. [6:24–7:00] Rides the boogie_woogie lpf slider down 10000→6350→0 — filtering the new layer out as a transition move.
12. [7:12–7:24] Bass rewrite mid-set: comments out `note(bass_pattern)` and replaces it with `note("e1(5,8)")` — a Euclidean bassline, 5 hits over 8 steps on a single low E — and adds `.jux(rev)` (left channel forward, right channel reversed = instant stereo width). The written melody is abandoned for a tighter, more driving pattern.
13. [7:36–8:36] Arrangement by comment-toggling: layers flip in and out of the `track: stack(...)` (hats/boogie out at 7:48; main_kick out, toms `.delay` bumped to `.3`, master hpf parked as `// .hpf(slider(852, 0, 3000))` at 8:12; main_kick back at 8:24; everything but kicks out at 8:36) — a breakdown/build cycle done purely with `//`.
14. [9:00, 10:00] Select-all + re-evaluate (whole file flashes highlighted, "loading..."), applying the batch of comment changes at once.
15. [9:12–9:48] Full-groove section: main_bass, sub_kick, main_kick, hats, boogie_woogie all in; hats get a brief `.postgain(1.2)` boost (then removed); hats lpf retyped (final value unreadable); boogie lpf swept 960→1590.
16. [10:12–10:48] Peak ride: bass `lpq` slider up to 8.8, `lpenv` up to 8.9 — maximum filter-envelope aggression on the supersaw bass.
17. [10:36–11:24] Outro strip-down: main_kick, hats, boogie_woogie, toms all commented out — only main_bass + sub_kick remain — then `.fm(time)` is added to the bass (ever-rising FM brightness) and `lpenv` is dragged back down to 1. The track ends as a dissolving bass drone over the 808 pulse.

## Techniques

- **Two-kick architecture** — split the kick's jobs: a plain four-to-the-floor 808 (`s("bd:3!4").bank("tr808").shape(.6).hpf(80)`) carries the pulse, while a separate syncopated synth-kick pattern carries the groove. Because they're separate voices they can be EQ'd (`hpf(80)` vs `lpf(742)`) and muted independently.
- **Alternating syncopated kick bar** — `s("<[sbd!3 [sbd sbd]] [sbd!2 [sbd sbd] sbd]>")` — `<>` alternates two bracketed bar-groupings each cycle, so the shuffling hard-groove kick figure is two bars long, not one. This one line is the genre's engine.
- **Noise hats with sampled ghosts** — synthesize the hat bed from white noise (`s("white!8").decay(.07).lpf(2000)`) and then randomly substitute real hat samples into it: `.sometimesBy(".3", x=>x.s("oh | hh"))` — 30% of hits become an open or closed hat (`|` picks randomly). Texture stays tight, variation is free.
- **Perlin everything** — `perlin.range(a, b)` as continuous LFO for organic drift: bass cutoff `lpf(perlin.range(200,1000).slow(4))`, hat velocity `.velocity(perlin.range(.5,1.7))`, hat speed `.speed(perlin.range(1,2).slow(8))`. Nothing static, nothing stepped.
- **Panned tom choir** — three tom voices with interlocking rest-heavy patterns, each filtered into its own band and panned to its own spot (`.lpf(1000).pan(.6)` / `.lpf(2500).pan(.3)` / `.hpf(300).pan(.8)`), grouped with `stack(...)` so one `.delay(.3)` treats them as a single bus.
- **Bus grouping via stack + variables** — every layer is a named `let`/`const` chain; `stack()` combines them both for sub-buses (`toms`) and the master (`track: stack(...)`). Effects appended after a `stack()`'s closing paren apply to the whole group.
- **Master-bus filter sweep** — hang `.hpf(slider(0, 0, 3000))` off the final `stack(...)` and drag it live for the classic whole-mix high-pass build, then comment it out when done. Same trick per-layer: `boogie_woogie`'s `.lpf(slider(…, 0, 10000))` fades that layer in/out by cutoff instead of volume.
- **Slider as performance macro** — every parameter that gets ridden live is wrapped in `slider(value, min, max)`: bass `lpq`/`lpenv`, layer lpf, master hpf. The set is "played" by dragging these, not by retyping numbers.
- **Comment-toggle arrangement** — sections are built by `//`-ing layers inside the `track: stack(...)` list and re-evaluating (select-all + eval shows as a full-file flash). Breakdowns, drops and the outro are all comment edits.
- **Euclidean bass swap** — mid-set, the written melody `"e2 f2 ~ g#1 ~ a1 f2 ~"` is commented out for `note("e1(5,8)")` — 5 hits spread over 8 steps on one note. Groove over melody; the old line is kept as a comment for instant rollback.
- **jux(rev) width** — `.jux(rev)` on the bass plays the pattern normally left and reversed right for cheap huge stereo.
- **time-driven outro** — `.fm(time)` on the bass in the final minute: FM index climbs forever, so the sound continuously brightens/degrades as the track dissolves — an ending you don't have to perform.

## Vocabulary

- `setCps(150/60/4)` — global tempo in cycles per second; reads as "150 BPM, 4 beats per cycle".
- `samples('github:tidalcycles/dirt-samples')` — load the classic Dirt sample library from GitHub.
- `const x = …` / `let x = …` — plain JS variables holding pattern chains; the track only plays what's in the final `stack`.
- `track: stack(a, b, …)` — label + stack: play all listed patterns together; effects chained after the `)` hit the whole mix.
- `stack(…)` — combine patterns to play simultaneously (also used to make sub-buses like `toms`).
- `note("e1(5,8)")` — pitch pattern; `(5,8)` = Euclidean rhythm, 5 onsets over 8 steps.
- `s("…")` / `.sound("…")` — sample/synth choice: `bd:3` (4th bd sample), `sbd` (synth kick), `white` (white noise), `hh`/`oh`/`lt`/`mt`/`ht` (hats/toms), `supersaw`.
- `.bank("tr808")` — pick the drum machine bank for the sample name (bd → 808 kick).
- `!4` / `* 8` — mini-notation repeat (`bd:3!4` = four per cycle) and speed-up (`hh:1 * 8` = 8 per cycle).
- `~` — rest. `[a b]` — subdivide a step. `<a b>` — alternate per cycle. `a | b` — pick one at random. `a, b` inside one string — stack.
- `.shape(0.3)` — waveshaping saturation/distortion amount.
- `.sustain(.8)` / `.release(0.1)` / `.decay(.07)` — amplitude envelope segments (decay ≈ length of a tick).
- `.lpf(742)` / `.hpf(80)` — low-/high-pass cutoff in Hz.
- `.lpq(…)` — lowpass resonance (Q).
- `.lpenv(…)` — lowpass filter-envelope depth (the swept parameter).
- `slider(value, min, max)` — inline UI slider usable anywhere a number goes; the on-screen knob for live sweeps.
- `perlin` — smooth noise signal; `.range(a, b)` scales it, `.slow(n)` stretches it in time.
- `.velocity(…)` — per-hit loudness scaling (here fed by perlin for humanization).
- `.speed(…)` — sample playback rate (pitch/length).
- `.sometimesBy(".3", fn)` — apply `fn` to a random 30% of events (`x=>x.s("oh | hh")` re-voices them).
- `.delay(.2)` — echo send amount.
- `.room(.1)` — reverb send amount.
- `.pan(.3)` — stereo position (0 left, 1 right).
- `.postgain(1)` — output gain after effects; the per-layer mixer fader.
- `.jux(rev)` — run the pattern reversed in the right channel only for stereo width.
- `.fm(time)` — FM index driven by the ever-rising `time` signal: endless brightening.
- `time` — continuous elapsed-time signal, monotonically rising.
- `._scope()` — inline oscilloscope of the layer's audio, rendered under the code line.
- `// line` — comment; the arrangement tool — layers mute by commenting them out of the stack and re-evaluating.
