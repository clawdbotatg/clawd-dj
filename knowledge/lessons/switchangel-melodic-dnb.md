---
source: https://www.youtube.com/watch?v=aPsq5nqvhxg
creator: Switch Angel
genre: melodic dnb
software: strudel
---

# Livecoding melodic DNB in Strudel

## Final code

```js
register('rlpf', (x,pat) => {return pat.lpf(pure(x).mul(12).pow(4))})
setGainCurve(x => Math.pow(x,2))
setCpm(170/4)
// LETS F*#*ING MAKE DRUM AND BASS W/ Switch Angel

$drums: stack(
  s("bd:1")  .beat("0,7?,10",16).duck("3:4:5"),
  s("sd:2").beat("4,12",16),
  s("hh:4!8")
)
  .rib(0,1/4)
  .orbit(2)._scope()

$bass: s("supersaw!8")
  .note("<c# f d# [d# a#2]>/2".sub("[12 0]".fast(4))).orbit(3)
  .rlpf(slider(0.989)).lpenv("2")

$riser: s("pulse!16").dec(.1).fm(time).fmh(time).orbit(5)

$vox: s("jt:3").scrub(berlin.fast(2).seg(8)
                .rib(13,2)
                )
.delay(.6).delaytime(rand).room(1).roomsize(7).dry(3)
.orbit(4)
```

Notes on fidelity:
- `.dry(3)` is the one real uncertainty: for most of the outro the line reads `.dry(0)` ("reverb only" at 3:49). The very last frame (t264, 4:24 — 4s before the video ends) shows `.dry(3` with the cursor still inside the parens, i.e. an edit caught mid-typing. Take `.dry(0)` as the last *stable* value; `3` may be an incomplete `.3` or a final tweak that was never heard.
- `.rlpf(slider(0.989))` — the slider widget's displayed value drifted as she rode it live: 0.552 → 0.664 → 0.699 → 0.774 → 0.934 → **0.989** last visible.
- Line 1 (`register('rlpf', …)`) is scrolled off-screen in the final frames but is verbatim from many earlier full views (t0–t112); it never changed.
- `.rib(0,1/4)` on the drums and the kick line both toggled via comments during the arrangement; the final frame shows both **uncommented** (active).
- `"bd:1"`, `"hh:4"`, `"0"`, `"3:4:5"`, `"supersaw"`, `"c#"`, `"d#"`, `"a#2"`, `"2"`, `"jt:3"`, `"pulse"` etc. render as boxed widget chips in the REPL; underlying text is as transcribed.
- The `$vox` chain's odd indentation (the lone `)` on its own line, effects on unindented lines) is how it actually sat in the editor.

## Build timeline

1. [0:00] Pre-existing scaffold: `register('rlpf', (x,pat) => {return pat.lpf(pure(x).mul(12).pow(4))})` (a custom curved lowpass helper), `setGainCurve(x => Math.pow(x,2))`, `setCpm(170/4)` (170 BPM, 4 beats/cycle — DNB tempo), comment header, and an empty `$drums: stack( ).orbit(2)`.
2. [0:00–0:10] Kick: `s("bd:1").beat("0,7?,10",16)` — "kick drum on beats zero, seven, sometimes 10 out of 16 steps" (the `?` makes a step probabilistic; per the code it sits on the 7). `._scope()` appended to the drum bus — "with the scope."
3. [0:13–0:22] Snare: `s("sd:2").beat("4,12",16)` — "snare on beats 4, 12 out of 16 steps" — the classic 2-and-4 DNB backbeat.
4. [0:23–0:29] Hats: `s("hh:4!8")` — "more groove with high hats. Number four, eighth notes" (sample `hh:4`, replicated 8 per cycle).
5. [0:29–0:37] Bass shell: `$bass: s("supersaw!8").note(…)` — "the base of our bass is a super saw. Eighth notes."
6. [0:38–0:48] Melody: `.note("<c# f d# [d# a#2]>/2")` — "key of F minor. First note C sharp, then F, D sharp, D sharp, A sharp 2" (`<…>` steps one entry per cycle, `/2` halves the rate, `[d# a#2]` packs two notes into one slot).
7. [0:49] `.sub(12)` on the note pattern — "subtract one octave" (12 semitones down).
8. [0:56–1:03] Pump: `.duck("3:4:5")` on the kick and `.orbit(3)` on the bass — "let's make a pump. Let's duck it with our kick" (kick ducks orbits 3, 4, 5 — vox orbit 4 and riser orbit 5 are pre-registered before those layers exist).
9. [1:07–1:23] Filter: `.rlpf(slider(0.552)).lpenv("2")` — "control our bass with our filter lowpass slider, and then envelope to make it bounce. Increase the slider to increase the power." `rlpf` is her registered helper: the 0–1 slider is mapped through `.mul(12).pow(4)` to a musically-curved cutoff.
10. [1:28–1:40] Vocal chops: `$vox: s("jt:3")` — "I recorded my voice. It sounds like this" — first scrubbed with a literal pattern (`.scrub("0!…")`).
11. [1:41–1:50] `.scrub(berlin.fast(2).seg(8))` — "scrub it with Berlin noise instead at double speed. Eighth note segments" (the `berlin` smooth-noise signal drives the playhead position; `.seg(8)` chops it into 8 slices/cycle). `.orbit(4)` routes it into the pump.
12. [1:52–2:02] `.rib(13,2)` inside the scrub — "we can control the RNG of the chops with ribbon. Ribbon from cycle 13, two cycles long" (freezes the noise into a repeating 2-cycle phrase).
13. [2:04–2:15] `.delay(.6).delaytime(rand)` on vox — "make it even cooler by adding delay. Modulate delay time random value."
14. [2:17–2:22] Build: mutes the kick by commenting its line (`// s("bd:1")…`) — "let's make a build. Mute our kick."
15. [2:23–2:52] Riser: `$riser: s("pulse").dec(.1)` → `.fm(time).fmh(t)` — "bring infinite riser sound. Pulse wave decay short. FM time FM harmonic time." Console errors "T is not defined" [2:43] — she fixes `t` → `time`. `.orbit(5)` so it pumps too.
16. [2:54] `s("pulse!16")` — "hey, let's do 16 notes instead" (8ths → 16ths).
17. [2:59–3:07] Drum rhythm control: `.rib(0,1/4)` appended to the whole drum stack — "we can control the rhythm of our drums. Cycle zero quarter notes" (loop the first quarter-cycle: only the beat-0 kick + hats survive, repeating 4x = four-on-the-floor).
18. [3:12–3:20] The drop: kick line uncommented, and `.rib(0,1/4)` commented back out (`// .rib(0,1/4)`) — full break returns ("breaking").
19. [3:27] "Increase filter for more power" — rides the `rlpf` slider up (0.699 → 0.774 → 0.934 → 0.989).
20. [3:33–3:46] Vox space: `.room(1).roomsize(6)` → `roomsize(7)` — "add reverb to vocals. Increase size."
21. [3:49] `.dry(0)` — "reverb only" (kill the dry signal, leaving a ghost-vocal wash).
22. [3:58–4:08] Bass bounce: `.sub(12)` becomes `.sub("[12 0]".fast(4))` — "we can modulate the bounce of our base by changing the notes" — the subtracted amount alternates 12/0 semitones 4x faster, so the bassline leaps octaves ("[12 0]… got fast too").
23. [4:15] Outro: `.rib(0,1/4)` uncommented again — "quarter note kick" — drums collapse back to the pounding quarter pulse. (Final seconds: `.dry(3` mid-edit, see fidelity note.)

## Techniques

- **DNB break via `.beat` step lists** — program the amen-feel kick/snare directly as step numbers out of 16 — `s("bd:1").beat("0,7?,10",16)` + `s("sd:2").beat("4,12",16)`: kick on 0/7/10, snare locked to 4 and 12 (the 2-and-4). `?` on a step makes it fire only sometimes, for a humanized break.
- **One drum bus, per-layer patterns** — wrap all drum voices in `stack(…)` and hang shared modifiers (`.rib`, `.orbit(2)`, `._scope()`) off the closing paren, while each `s(…)` keeps its own `.beat`.
- **Custom curved macro via `register`** — wrap an awkward parameter in your own named function with a perceptual curve — `register('rlpf', (x,pat) => {return pat.lpf(pure(x).mul(12).pow(4))})` so `.rlpf(slider(0.989))` maps a 0–1 slider onto cutoff as `(x*12)^4` Hz: fine control at the bottom, huge sweep at the top.
- **Slider as performance macro** — `.rlpf(slider(0.552))` gives an on-screen knob she rides for the whole set; "increase the slider to increase the power" is the drop-energy move (ends at 0.989 ≈ filter wide open).
- **Sidechain duck / pump** — `.duck("3:4:5")` on the kick ducks orbits 3, 4, 5, shaping bass, vox, and riser at once; orbits are registered in the duck list *before* those layers exist. Each pumped layer only needs `.orbit(n)`.
- **Bracket-melody bass** — a slow angle-bracket sequence on an 8th-note supersaw — `s("supersaw!8").note("<c# f d# [d# a#2]>/2")`: the notes change per cycle (halved by `/2`) while the rhythm stays 8ths, so one chord-tone per bar pulses underneath (F-minor: c#, f, d#, d#+a#2).
- **Octave-bounce via patterned `.sub`** — modulate the transposition itself — `.sub("[12 0]".fast(4))` alternates dropping 12 semitones and 0 four times per slot, so the same melody leaps octaves for bounce.
- **Berlin-noise vocal scrub** — treat a vocal recording as a wavetable and let smooth noise drive the playhead — `s("jt:3").scrub(berlin.fast(2).seg(8).rib(13,2))`: `berlin` = smooth random position, `.fast(2)` doubles the wander speed, `.seg(8)` chops into 8th-note slices, `.rib(13,2)` freezes cycles 13–15 of the randomness into a repeating 2-cycle chop pattern ("control the RNG with ribbon").
- **Randomized delay** — `.delay(.6).delaytime(rand)` — echo level fixed, but every echo lands at a random time = glitchy sprayed repeats on the chops.
- **Infinite time-driven riser** — `s("pulse!16").dec(.1).fm(time).fmh(time)` — short-decay pulse 16ths whose FM index and harmonicity both ride the ever-growing `time` signal, so the timbre climbs forever; mute the kick underneath it for the build.
- **`.rib` as arrangement/rhythm tool (not just RNG-freeze)** — `.rib(0,1/4)` on the whole drum stack loops just the first quarter-cycle: only the beat-0 kick and hats survive, giving a four-on-the-floor "quarter note kick" section from the same code; toggling the line's `//` switches break ↔ pulse.
- **Mute-by-comment arrangement** — `//` on the kick line for the build, remove it for the drop; same trick toggles the `.rib(0,1/4)` rhythm. In this video comments are the mute button (rather than the `_$:` label prefix).
- **Reverb-only ghost vocals** — `.room(1).roomsize(7).dry(0)` — full send into a huge room and kill the dry path, so only the wash remains.
- **Global gain curve** — `setGainCurve(x => Math.pow(x,2))` in the scaffold: gain values respond on a squared (perceptual) curve.

## Vocabulary

- `register('name', (x,pat) => …)` — define your own chainable pattern function; here it wraps `.lpf` with a curve.
- `pure(x)` — lift a plain value into a pattern (needed inside `register` to do `.mul/.pow` math on it).
- `setGainCurve(x => Math.pow(x,2))` — remap all gain values through a curve (squared ≈ perceptual loudness).
- `setCpm(170/4)` — tempo in cycles per minute; the `170/4` idiom reads "170 BPM, 4 beats per cycle."
- `$name:` — play a labeled pattern (`$drums:`, `$bass:`, `$riser:`, `$vox:`); commenting a line with `//` mutes it.
- `stack(a, b, c)` — layer patterns simultaneously in one channel.
- `s("bd:1")` — sound/sample choice; `:n` picks variant n from the bank (`bd:1`, `sd:2`, `hh:4`, `jt:3` — `jt` is her own recorded voice).
- `!8` — mini-notation replicate: `"hh:4!8"` = 8 hats per cycle; `"supersaw!8"` = 8th-note bass; `"pulse!16"` = 16ths.
- `.beat("0,7?,10", 16)` — trigger on the listed step numbers out of N steps per cycle; `?` makes that step probabilistic.
- `.duck("3:4:5")` — sidechain: this pattern's hits duck orbits 3, 4 and 5.
- `.orbit(n)` — route to a numbered mixer bus (duck target / effect isolation).
- `._scope()` — inline oscilloscope of the pattern's audio.
- `.note("<c# f d# [d# a#2]>/2")` — note names; `<…>` cycles one entry per cycle, `[…]` packs entries into one slot, `/2` plays the sequence at half speed.
- `.sub(12)` / `.sub("[12 0]".fast(4))` — subtract semitones from the notes; patternable, so the transposition itself can move.
- `.rlpf(…)` — her registered curved lowpass (slider 0–1 → `(x*12)^4` Hz cutoff).
- `slider(0.989)` — inline UI slider widget usable anywhere a number goes; shows the live value in code.
- `.lpenv("2")` — lowpass filter envelope depth ("envelope to make it bounce").
- `.scrub(sig)` — play a sample by scrubbing its playhead to the signal's value (0–1 position).
- `berlin` — smooth continuous noise signal (à la perlin; she narrates it "Berlin noise").
- `.fast(2)` — speed a pattern/signal up by a factor.
- `.seg(8)` — sample a continuous signal into N discrete events per cycle.
- `.rib(13,2)` — "ribbon": freeze a random/noise stream to the values it had from cycle 13, looping a 2-cycle window; `.rib(0,1/4)` on drums loops the first quarter-cycle as a rhythm edit.
- `.delay(.6)` — delay send level.
- `.delaytime(rand)` — delay time; `rand` = continuous random signal, so every echo lands differently.
- `rand` — uniform random signal 0–1.
- `.room(1)` / `.roomsize(7)` — reverb send and room size.
- `.dry(0)` — level of the unprocessed signal; 0 = "reverb only."
- `.dec(.1)` — envelope decay (short, plucky).
- `.fm(time)` / `.fmh(time)` — FM index / harmonicity ratio; feeding both the ever-rising `time` signal = infinite riser (note: `t` alone errors — "time, not t").
- `time` — continuous signal of elapsed time, monotonically rising.
