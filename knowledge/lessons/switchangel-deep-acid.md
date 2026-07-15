---
source: https://www.youtube.com/watch?v=HkgV_-nJOuE
creator: Switch Angel
genre: acid techno
software: strudel
---

# 2 Minute Deep Acid in Strudel (from scratch)

## Final code

```js
setCps(140/60/4)

// LETS MAKE ACIDDDDD with SWITCH ANGEL

$: s("sbd!4").distort()._scope()   // .distort was still being typed in the last frame that shows this line; its argument was never visible on screen
.duck("2:3:4").duckattack(.2).duckdepth(.8)

$bass: n(irand(10).sub(7).seg(16)).scale("c:minor")
.rib(46,1)
  .distort("2.2:.3")
.s("sawtooth").lpf(200).lpenv(slider(2.28,0,8))

  .lpq(12).orbit(2)._pianoroll()

$: s("supersaw").detune(1).rel(5).beat(2, 32).slow(2).orbit(3)
.fm("2").fmh(2.04).room(1).roomsize(6)

$: s("pulse").orbit(4).seg(16).dec(.1).fm(time).fmh(time)
```

Notes on fidelity:
- The kick's `.distort` (added at 3:12, narrated "store" = distort) is the one uncertainty: the last frame showing line 6 (t192) captures it mid-typing as `$: s("sbd!4").distort|._scope()` with no argument yet, and the final two frames are scrolled past that line. Everything after `.distort` on the kick is unverified.
- `.lpenv(slider(2.28,0,8))` — the slider widget's displayed value drifted while she swept it (3.04 → 2.36 → 2.28); 2.28 is the last visible value.
- Line 16 is clipped by the webcam overlay in the final frames, but an earlier full view (t168, ~2:48) shows it ends `.orbit(3)`.
- `"sbd"`, `"2:3:4"`, `"c:minor"`, `"2.2:.3"`, `"sawtooth"`, `"pulse"` render as boxed widget chips in the REPL; the underlying text is as transcribed.

## Build timeline

1. [0:00] Pre-existing scaffold: `setCps(140/60/4)` (140 BPM, 4 beats/cycle) and a comment header. "Let's make some fast acid."
2. [0:03] Kick first: `$: s("sbd!4")._scope()` — a synthesized 909-style kick, four to the floor (`!4` = repeat 4x per cycle), with an oscilloscope visual ("kick with the scope").
3. [0:11–0:20] Bass melody as pure randomness quantized to a scale: `$bass: n(irand(10).sub(7).seg(16)).scale("c:minor")` — "random notes", "subtract one octave" (`.sub(7)` = down 7 scale degrees), "16th notes in the scale of C minor" (`.seg(16)` samples the random signal 16x per cycle).
4. [0:25–0:35] Give the bass its acid voice: `.s("sawtooth").lpf(200).lpenv(2).lpq(12)` — "make the sound a sawtooth wave with a low pass filter of 200 hertz and an envelope of two", then "increase the resonance" with `.lpq(12)`.
5. [0:39–0:48] Sidechain pump: `.orbit(2)` on the bass, and on the kick line `.duck("2:3:4")` — "Let's duck it. Let's make it pump." The kick ducks orbits 2, 3, and 4 (pre-registering orbits for layers that don't exist yet).
6. [0:49–0:56] Shape the pump: `.duckattack(.2)` ("increase that duck attack to 200 milliseconds") and `.duckdepth(.8)` ("lower the depth to 08").
7. [1:01–1:06] Freeze the randomness into a loop: `.rib(46,1)` on the bass — "ribbon the seed of our bass so it repeats every cycle" (seed 46, 1 cycle).
8. [1:08–1:19] Performance control: "replace this envelope with a slider" — `.lpenv(2)` becomes `.lpenv(slider(3.04,0,8))`, then she sweeps it live (settles ~2.28). This is THE acid move: riding the filter-envelope depth by hand.
9. [1:19–1:31] Grit: `.distort("2.2:.3")` on the bass — "add some distortion" (pattern string: gain 2.2, post-gain/mix .3).
10. [1:31–1:47] New layer, the "fog horn": `$: s("supersaw").detune(1).rel(5).beat(2, 32)` — "It's got a fog horn sound. Super saw. the high detune, the high release, on beat two out of 32" (a single stab that fires once every 32 beats, on beat 2).
11. [1:47–1:51] `.slow(2)` — "slow the pattern by two", then `.orbit(3)` — "let's make it pump as well" (orbit 3 is already in the kick's duck list).
12. [1:56–2:04] `.fm("2").fmh(2.04)` on the supersaw — "we can FM our fog horn for more chaos" (FM index 2, harmonicity 2.04 — slightly detuned from harmonic for grind).
13. [~2:12] Mutes the kick (`$:` → `_$:`) to build the riser section — "what's making a vanilla building riser".
14. [2:23–2:36] Riser: `$: s("pulse").orbit(4).seg(16).dec(.1).fm(time).fmh(time)` — "16th notes with a short decay pulse wave, FM with time, FM harmonic with time" — both FM index and harmonicity are driven by the ever-growing `time` signal, so the timbre climbs forever = infinite riser. Orbit 4 so it pumps too.
15. [2:38] `._pianoroll()` appended to the bass chain — "add the piano to our base" (pianoroll visualization of the bass pattern).
16. [2:46] Unmutes the kick — "bring our kick back in" (`_$:` → `$:`) — the drop.
17. [2:54–3:06] Space on the fog horn: `.room(1).roomsize(6)` — "add some room reverb to our supersaw sound. Make it huge."
18. [3:09–3:12] Final punch: "Make it pop" — `.distort(…)` added to the kick line (argument off-camera).

## Techniques

- **Sidechain duck / pump** — the kick ducks every melodic layer for the classic pumping-techno feel — `.duck("2:3:4")` on the kick channel (mini-notation list of target orbits), shaped with `.duckattack(.2).duckdepth(.8)`; each pumped layer just needs `.orbit(2)` / `.orbit(3)` / `.orbit(4)`. She registers orbits 3 and 4 in the duck list before those layers even exist.
- **Random-but-looping acid line** — generate the melody from noise, quantize to a scale, then freeze the seed so it repeats as a riff — `n(irand(10).sub(7).seg(16)).scale("c:minor").rib(46,1)`. `irand(10)` = random scale degrees 0–9, `.sub(7)` drops an octave, `.seg(16)` = 16th-note steps, `.rib(46,1)` pins seed 46 over 1 cycle.
- **Acid filter voice** — sawtooth into a low-set lowpass with high resonance and a swept envelope — `.s("sawtooth").lpf(200).lpq(12).lpenv(…)`. Cutoff stays at 200 Hz; all movement comes from the envelope amount.
- **Slider as performance macro** — swap any literal for `slider(value,min,max)` to get an on-screen knob you ride live — `.lpenv(slider(2.28,0,8))` replacing `.lpenv(2)`. Sweeping lpenv depth is the acid "wub" move.
- **Patterned distortion** — distortion amount as a mini-notation pattern string with gain:mix — `.distort("2.2:.3")` on the bass (and a plain `.distort(…)` on the kick to "make it pop").
- **Fog-horn stab (sparse big-release hit)** — one huge detuned supersaw note that fires rarely and rings out — `s("supersaw").detune(1).rel(5).beat(2, 32).slow(2)`: fire on beat 2 of a 32-beat grid, halved again by `.slow(2)`, 5-unit release tail.
- **FM for chaos** — add FM to a pad/stab for grind, using a near-harmonic ratio — `.fm("2").fmh(2.04)` (harmonicity just off 2 gives slow beating/detune grind).
- **Infinite time-driven riser** — feed `time` into FM params so the timbre rises without ever resetting — `s("pulse").seg(16).dec(.1).fm(time).fmh(time)`: 16th-note short-decay pulse ticks that get progressively more metallic/bright forever.
- **Mute/unmute as arrangement** — prefix a pattern label with `_` to mute it (`_$:`), remove it to drop back in — she mutes the kick to build the riser section, then unmutes for the drop.
- **Inline visualizers as instrumentation** — `._scope()` on the kick (waveform) and `._pianoroll()` on the bass (note grid) render live inside the editor, doubling as performance visuals.

## Vocabulary

- `setCps(140/60/4)` — set global tempo in cycles per second; the 140/60/4 idiom reads as "140 BPM, 4 beats per cycle".
- `$:` — play an (anonymous) pattern; `$name:` (e.g. `$bass:`) labels it; prefixing `_` (`_$:`) mutes that line.
- `s("...")` — choose the sound/sample/synth: `"sbd"` (synthesized 909-ish kick sample), `"sawtooth"`, `"supersaw"`, `"pulse"`.
- `!4` — mini-notation repeat: `"sbd!4"` = four kicks per cycle.
- `n(...)` — pattern of note/scale-degree numbers fed to the synth.
- `irand(10)` — continuous stream of random integers 0–9.
- `.sub(7)` — subtract from each value (here: drop the random degrees one octave, 7 scale steps).
- `.seg(16)` — sample a continuous signal into N discrete events per cycle (16 = 16th notes).
- `.scale("c:minor")` — map numbers onto a scale (C minor) to get pitches.
- `.rib(46,1)` — "ribbon": freeze the random stream with seed 46 over a 1-cycle window so it loops identically.
- `.lpf(200)` — lowpass filter cutoff in Hz.
- `.lpenv(2)` — lowpass filter envelope depth (the swept acid parameter).
- `.lpq(12)` — lowpass filter resonance (Q).
- `slider(2.28,0,8)` — inline UI slider widget (value, min, max) usable anywhere a number goes.
- `.orbit(2)` — route the pattern to a numbered mixer bus (target for duck/effects).
- `.duck("2:3:4")` — sidechain: this pattern's hits duck the audio on orbits 2, 3, 4.
- `.duckattack(.2)` — recovery/attack time of the duck envelope (~200 ms).
- `.duckdepth(.8)` — how far the ducked signal is attenuated (0–1).
- `.distort("2.2:.3")` / `.distort()` — waveshaping distortion; the string form patterns amount:mix.
- `.detune(1)` — spread/detune amount of the supersaw's stacked oscillators.
- `.rel(5)` — envelope release time (long tail).
- `.dec(.1)` — envelope decay time (short, plucky).
- `.beat(2, 32)` — trigger only on the given beat number(s) out of N beats per cycle-group (beat 2 of 32).
- `.slow(2)` — stretch the pattern to half speed (twice as long).
- `.fm("2")` / `.fm(time)` — frequency-modulation index (brightness/grind); patternable, can take a signal.
- `.fmh(2.04)` / `.fmh(time)` — FM harmonicity ratio (modulator:carrier); non-integer = clangorous.
- `time` — continuous signal of elapsed time, monotonically rising — plug into params for endless risers.
- `.room(1)` — reverb send amount.
- `.roomsize(6)` — reverb room size ("make it huge").
- `._scope()` — inline oscilloscope visualization of the pattern's audio.
- `._pianoroll()` — inline pianoroll visualization of the pattern's notes.
