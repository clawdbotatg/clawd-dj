---
source: https://www.youtube.com/watch?v=m7Rp46AU8dw
creator: Glossing
genre: house
software: strudel
---

# STRUDEL FOR BEGINNERS (46-minute house track from scratch)

## Final code

```js
// bd, sd, cp, hh, pad, tops, vox
kick: s("bd*4").bank("tut").duck(5).duckattack(0.3)
$: s("[~ cp]*2").bank("tut").orbit(2).room(0.4).size(0.8).postgain(1.3)
closedhat: s("hh*16").bank("tut").decay(0.05)._spectrum()
openhat: s("[~ hh]*4").bank("tut")._spectrum()

// 027_a__Pad_Loop_110bpm_G#m_-_RETROWAVE_Zenhiser
pad: s("pad").bank("tut").clip(1).postgain(0.5)
  .note("C2").transpose(-8).room(0.3).delay(0.3)
  .orbit(5)

setDefaultJoin('mix')
vocal: s("vox").bank("tut").clip(1).note("C2".add("<4!3 [-8 -8] ~!4>")).n(5)
  .delay(0.3).postgain(0.7).compressor(-20)

tops: s("tops:4/4").fit().bank("tut").clip(1).postgain(0.7)
  ._pianoroll()

bass: s("saw").set(`<
  ~ 3
  4 3
  ~ 3
  ~ 3
  ~ 5
  4 5
  ~ 5
  ~ 5
  ~ 2
  4 2
  ~ 2
  ~ 2
  ~ 6
  4 6
  7 6
  ~ 6
>*8`.as("n")).scale("C1:minor").lpf(rand.range(50, 200)).lpq(8)
  .sometimesBy(0.125, x => x.ply("2")) // arrow notation
  .lpe(2).lpdecay(0.3)._spectrum().postgain(1.5)
  ._pianoroll({ labels: 1, width: 1000 })

pluck: s("saw").set(`<
  ~!3 0
  ~!3 3
  ~!3 5
  ~!3 4
>*8`.as("n")).scale("C4:minor")
  .add(note("0,0.3")).lpf("<200 2800>/4").sometimes(x => x.ply(2)).vib(0.3)
  ._pianoroll()
  .delay(0.6).delayfb(0.6)._spectrum()

all(x => x.mul(postgain(0.7)))
```

Notes on fidelity:
- Reconstructed by combining scrolled views: t02730 (lines 1–12), t02685 (12–27), t02670 (25–38), t02745/t02700/t02655 (38–50). All samples are her own uploads in bank `tut` (`tut_bd(9) tut_cp(12) tut_hh(10) tut_pad(22) tut_sd(10) tut_tops(14) tut_vox(17)` per the sounds panel at t02160).
- Bass tail (`.lpe(2)...` + `.postgain(1.5)`) is one logical line: the inline `_spectrum()` widget canvas wraps the editor line, so `.postgain(1.5)` renders on its own unnumbered row below the canvas. `.lpe(2)` verified via the pluck (a verbatim copy of the bass at 41:45, frame t02505) — she had lowered it from the `.lpe(4)` she narrated at 26:50 sometime before copying.
- Pluck line 46's `.sometimes(x => x.ply(2)).vib(0.3)` appears only in the very last frame (t02745, during the unnarrated outro playback); `.vib(0.3)` is my best reading of that frame and has no narration to confirm it.
- Clap line: narration mentions only "reverb", "size 0.8", "turned it up"; the frame reading `.orbit(2).room(0.4).size(0.8).postgain(1.3)` is consistent across t02460 and t02730. This whole line plus `.compressor(-20)` on the vocal were added during a jump cut (~40:08–41:04), so their reasoning is only summarized on screen.
- Pad `.postgain(0.5)`: she *says* 0.7 at 12:30 but every frame from t00810 on shows 0.5. Pad `.delay(0.3)`: she says 0.1 (then demos 1); frames settle at 0.3. Later frame wins in both cases.

## Build timeline

1. [0:46–2:05] Fresh browser, stock Strudel. Imports her own samples: hamburger menu → sounds → import-sounds; each subfolder name becomes a sound name you type into `s()`. Samples came from searching "pad", "bass drum" etc. on Splice and taking "the first 10" — "nothing fancy going on here."
2. [2:08–2:44] Replaces the default pattern with `$: s("tut_bd")`, then splits prefix from name: `s("bd").bank("tut")` — "if I don't want to have to type each time." [2:30] "If you're a super super beginner, S is just sound and it picks what sound is being played."
3. [3:06–4:23] Lane labels: `$:` is "an anonymous label, meaning that I don't care what it's named"; or name them (`bassdrum:`, `snaredrum:`). Writes the inventory comment `// bd, sd, cp, hh, pad, tops, vox`. Ctrl+Enter = start/update, Ctrl+. = stop. Alt+Shift+Down duplicates a line. `$bassdrum` (dollar+name) is for multiple lines with the same name; two plain `bassdrum:` labels → only the last one plays.
4. [4:26–5:22] Settings tour: highlight active line, highlight events in code, autocomplete, Ctrl+hover tooltips, theme (picks the red "glossing" look).
5. [5:32] `all(x => x.pianoroll())` to see that all three drum lines land on the same beat (removed later).
6. [6:01–7:20] The house beat: `s("bd*4")` — "play the bass drum four times every measure. That's the times four." Snare: `s("[~ sd]*2")` — brackets "subdivide a unit of time": `sd*2` alone = half notes; `[sd sd]*2` = quarters; `[~ sd]*2` = rest-then-snare = backbeat. `~` or `-` is a rest ("they're the same").
7. [7:32–8:32] Hats: `s("hh*16")` for 16th notes, tamed with `.decay(0.3 → 0.1 → 0.05)` ("you have all of the ADSR parameters"); `._spectrum()` added to *see* how tight the hat is.
8. [8:42–9:59] Open hats on the offbeat: wants them opposite the kick → `s("[~ hh]*4")`, same rest-subdivision trick. Realizes she never downloaded open hats, so the undecayed `hh` plays "open" vs the 0.05-decay "closed". Names them `closedhat:` / `openhat:`.
9. [10:02–10:57] Pad: sounds panel shows `tut_pad(22)` — "that's the number of samples in that bank"; `.n()` picks which. Solo trick: "take whatever you labeled it as and put an S in front of it" — frame t00630 shows `S$:` soloing the kick while she auditions `n(0..8)` of 9 bd samples.
10. [11:02–11:56] `pad: s("pad").bank("tut").clip(1)`. The clip rule: a long sample retriggers every cycle and overlaps itself for minutes — "just write clip one if you have long samples."
11. [12:03–12:46] Levels: `.postgain(0.5)`. Gain vs postgain: "Gain happens first in the signal chain. Post gain... happens last," so it isn't overridden by later distortion. "These are linear gains... literally multiplying the volume."
12. [12:46–13:38] Pitch: "by default samples play note C2"; either write another note (`A1`) or keep `.note("C2")` and `.transpose(-8)` (shift by semitones). Settles on -8.
13. [13:49–15:16] Sidechain: pad gets `.orbit(5)` ("an orbit is a collection of effects shared by a bunch of different patterns"), kick gets `.duck(5)` — "duck, which is the strudel name for side chain" — then `.duckattack(0.3)`: 0 = instant recovery, 1 = held down ("nothing"), 0.3 = "nice pumping to the beat."
14. [15:16–16:00] Pad space: `.room(0.3)` ("room. That's the name for reverb... 0.3 will send like a third of the signal") and `.delay(0.3)` (narrated 0.1, demos 1 to make it obvious).
15. [16:06–17:13] Reads the pad's Splice filename (kept as the comment on line 6) → it's G# minor. Future-self correction: she forgot the `transpose(-8)`, so the working key is actually C minor ("G# down to G, F, E, D, C").
16. [17:14–19:17] Bass: `s("saw")` from the built-in oscillators (tour of wavetables, sample banks, drum machines, GM soundfonts). `note("G#1")` to confirm key, then `.lpf(200)` — "it's a cutoff frequency... 200 hertz, which will make it pretty low."
17. [19:42–24:15] The "classic glossing way" — patterned scale degrees instead of note names. Key beginner theory: pattern chains sample left-to-right, "the parts that come first sort of dominate"; `s("saw")` fires once/cycle, so a later `.note("g#1 a1")` only ever gets asked once → always the first note. Fix: `set.mix(...)` "does a bit more of an intuitive thing." Backtick = multi-line quotes. `<...>*8` = "brackets and then times some number... tells it what kind of note you're writing" (8 = eighth notes). `~ 0` inside = rest-then-note = offbeat bass. `.as("n")` = "shorthand for writing n of the thing"; `.scale("G#1:minor")` maps degree 0 → G#.
18. [24:33–25:00] Alt+Shift+Down the pattern rows and vary them: root rows `3 / 5 / 2 / 6` (a minor-key house progression in scale degrees), sixteen rows spanning the `<>` alternation.
19. [25:04–26:42] Movement: put `.lpf()` *after* the note pattern — "patterns happen left to right... this is only measuring once every cycle" — so placed late it re-evaluates at eighth-note rate. `.lpf(rand.range(200, 800))` for random cutoff; `.log()` to print the values and prove placement matters (before the pattern = one value held for the whole cycle).
20. [26:44–28:06] Acid shaping: `.lpe(4)` — lowpass envelope, "it takes two to that power... exponentially impactful number"; tightens the random range to `rand.range(50, 200)`; `.lpq(8)` resonance "for a bit more of an acid sound"; `.postgain(1.5)` (typed 2 first) to bring the now-darker bass up. (`.lpdecay(0.3)` also appears in frames, unnarrated; `.lpe` later lowered to 2.)
21. [28:12–29:47] Probability: `x => x.ply("2")` — "X is the pattern that we already have written" (JS arrow notation) — wrapped in `sometimes` (50%), demoed `rarely` (~25%) and `almostNever`, then settles on explicit `.sometimesBy(0.125, ...)`: occasionally double a bass note.
22. [29:51–30:10] Flavor notes: replaces two row-roots with `7` and `4` ("maybe sometimes I want to add a little flavor note in here").
23. [30:32–31:30] Vocal: `vocal: s("vox").bank("tut").clip(1)` ("Remember to put clip of one so it doesn't break everything"). Master trim when things distort: `all(x => x.mul(postgain(0.7)))` — "for every pattern X... take whatever the post gain was already at and multiply it further by 0.7."
24. [31:32–32:44] Vocal tuning: `.note("C2").trans(4)` — "-8 ≡ +4, they add up to 12 for an octave," and up sounds better than making a low voice lower. Works because "all of the samples I got were in G# minor." Auditions `n()` values (one "sounds like a clown horn. Skip."), keeps `n(5)`.
25. [32:44–33:49] Patterned transpose: `.trans("<4!3 [-8!2]>")` — up 4 three times, then down 8 twice; `!` = "a shorthand you can use for writing something twice... exclamation point 2." But it only changes once per cycle — the left-to-right sampling trap again, demonstrated in isolation.
26. [34:14–34:52] Second attempt: `.note("C2".add("<4 ...>"))` — "Strudel does some magic in the back end to properly add numbers to letters" — still sampled too slowly.
27. [34:55–35:40] The real fix: `setDefaultJoin('mix')` — "will change all of the updates from functions in the pattern to have something like set domix," so `.set(...)` and `.add(...)` now behave intuitively everywhere; bass's `set.mix` becomes plain `.set`. Vocal melody works: `"C2".add("<4!3 [-8 -8]>")`, plus `.delay(0.3)`.
28. [35:47–36:30] Tops: "top loops... everything but the bass drum, so they don't clash with your other elements." `tops: s("tops:4")` (sample 4 of 14) `.clip(1)`, soloed + `_pianoroll()` — it doesn't line up with the cycle boundary.
29. [36:48–39:45] Beat-matching a loop, the whole recipe: label the kick (`kick:`) to compare; **guess** the loop length in measures; `"tops:4/2"` — "divide by two is equivalent to writing slow of two" (also `*0.5`); then `.fit()` squeezes the sample into that window. Guessed wrong: "if it sounds really fast and crazy... it's being compressed into too short of a length" → try 4: `"tops:4/4".fit()` lines up. Overshooting (8) = "too low of a pitch and clearly playing too slowly." Rule of thumb: "just pick powers of two... and write divide by that number and fit and clip and then it will sound right."
30. [40:08–41:17] (Jump cut) Vocal gets `.compressor(-20)`; snare replaced by a clap `$: s("[~ cp]*2")` with reverb — "size sets the size of the reverb... 0.8 gives you a somewhat small room" — and `.postgain(1.3)`.
31. [41:21–42:30] Lead: `pluck:` starts as a copy of the bass line; melody becomes sparse `~!3 0 / 3 / 5 / 4` (three rests then a note, per row); `scale("C4:minor")` — "I don't want C1... C minor defaults to three," she wants 4; strips the lpf/lpq/lpe; adds `.delay(0.6).delayfb(0.6)` — "This goes up to one, which is what you don't want to write... Write 0.6 for 60% of the signal fed back."
32. [42:54–43:45] Detune trick: `.add(note("0,0.3"))` — "comma does a stack in strudel... it kind of splits the pattern into two patterns": one fork unchanged, one 0.3 semitones sharp → "this nice d-tuning effect."
33. [44:15–44:40] Arrangement via filter: `.lpf("<200 2800>/4")` on the pluck — 200 Hz (ducked dark) while the vocal phrase lands, opening to 2800 Hz the rest of the time; `/4` because the vocal "comes in once every four measures."
34. [45:00–45:45] During the outro playback the pluck quietly gains `.sometimes(x => x.ply(2)).vib(0.3)` (visible only in the final frame, never narrated). "So that's the track."

## Techniques

- **Fundamental: the cycle** — everything in Strudel repeats per cycle (= one measure here); `*N` packs N events into a cycle, `/N` (or `.slow(N)`) stretches over N cycles, and long samples retrigger every cycle unless clipped. Idioms: `"bd*4"`, `"tops:4/4"`, `.clip(1)`.
- **Fundamental: mini-notation** — `*N` repeat, `[ ]` subdivide a step ("start to subdivide that half note into more things"), `~` or `-` rest, `!N` repeat an element (`4!3`, `~!3`), `< >` alternate one entry per step, `,` stack patterns in parallel, backticks for multi-line pattern strings.
- **Fundamental: left-to-right pattern sampling** — the earlier part of a chain "has dominance": a once-per-cycle sound asks a later melody pattern for a value only once per cycle. Fix with `set.mix(...)` or globally with `setDefaultJoin('mix')`; same reason effect placement matters (`.lpf(rand...)` *after* an eighth-note pattern changes at eighth-note rate, before it only once per cycle — proven with `.log()`).
- **Labels, solo, layering** — `$:` anonymous lane, `name:` named lane (duplicates: last wins; `$name:` to run several), prefix `S` to solo a lane (`S$:`), first line of the file as a `//` inventory comment of every planned element.
- **House beat kit** — four-on-floor `s("bd*4")`; backbeat snare `s("[~ sd]*2")`; 16th closed hats `s("hh*16").decay(0.05)`; offbeat open hats `s("[~ hh]*4")` — the offbeat is always the same idiom: subdivide the kick's quarter note into `[~ x]`.
- **Own samples via bank** — upload folders in the sounds panel; folder name = sound name; `s("bd").bank("tut")` keeps names short; `.n(i)` indexes the sample in the bank; sounds panel shows each bank's count.
- **clip(1) on every loop/one-shot longer than a cycle** — "if I play a sample that is very long... it also will start the sample again every cycle" → self-overlapping mud. Pads, vocals, tops all get `.clip(1)`.
- **Sidechain via orbits** — melodic layer `.orbit(5)`, kick `.duck(5)` + `.duckattack(0.3)` (0 = instant back, 1 = held down). Orbit = "a collection of effects shared by a bunch of different patterns", pick any number.
- **Gain staging** — `.postgain()` (not `.gain()`) because it's last in the chain and survives later effects; linear multiply; master trim with `all(x => x.mul(postgain(0.7)))` when the sum distorts.
- **Sample pitch** — samples default to `note("C2")`; retune with `.note("A1")` or `.note("C2").transpose(-8)`; ±semitones adding to 12 are the same pitch class (-8 ≡ +4); read the key off the Splice filename and keep it as a comment.
- **Degrees-not-notes melody writing** — her signature: `s("saw").set(`\`<rows>*8\``.as("n")).scale("C1:minor")` — a multi-line `<>` pattern of scale degrees, `*8` = eighth notes, `~ d` rows = offbeat bass, one row per eighth, roots outlining a progression (3→5→2→6), plus stray degrees (7, 4) as flavor notes. Transposable and always in key.
- **Random-filter acid bass** — `.lpf(rand.range(50, 200)).lpq(8).lpe(2).lpdecay(0.3)` placed *after* the note pattern so the cutoff re-rolls per note; lpe is "two to that power" — exponentially impactful envelope depth.
- **Probability ornaments** — `.sometimesBy(0.125, x => x.ply("2"))`: occasionally ratchet a note into a double. Family: `sometimes` = sometimesBy(0.5), `rarely` ≈ 0.25, `almostNever`, `never`; arrow notation = plain JS lambda over the existing pattern.
- **Fitting an unknown loop** — guess its length in powers of two, `"sample/N"` (= `.slow(N)`) then `.fit()`: too-fast-and-crazy → N bigger; too-low-and-slow → N smaller. Plus `.clip(1)`. Tops loops specifically avoid clashing since they contain no kick.
- **Stacked-detune width** — `.add(note("0,0.3"))`: comma-stack splits into an unchanged fork and a +0.3-semitone fork → instant chorus/detune on the lead.
- **Call-and-response filter arrangement** — `.lpf("<200 2800>/4")` on the lead, matched to the vocal's 4-measure period (`~!4` rest in the vocal's melody pattern): lead is dark when the vocal speaks, opens up when it's silent.
- **Inline visualizers as workflow** — `._spectrum()` to judge hat decay and bass filtering, `._pianoroll({labels:1,width:1000})` to check alignment and melodies, `all(x => x.pianoroll())` to see every lane at once, `.log()` to print sampled values.

## Vocabulary

- `s("...")` — "S is just sound": picks the sample/synth ("bd", "sd", "cp", "hh", "pad", "vox", "tops", "saw").
- `$:` / `name:` / `$name:` — anonymous label / named label (last duplicate wins) / multi-instance label; prefix `S` (e.g. `S$:`) solos a lane.
- `.bank("tut")` — prepend a sample-bank prefix so `s("bd")` resolves to `tut_bd`.
- `.n(5)` — sample index within a bank (also scale-degree index when used with `.scale`).
- `"x*4"` — mini-notation: repeat 4× per cycle (quarter notes here).
- `"[~ sd]*2"` — `[]` subdivides a step; `~` (or `-`) is a rest → offbeat/backbeat idiom.
- `"4!3"` / `"~!4"` — `!N` repeats an element N times.
- `"<a b c>"` — alternation: one entry per step, cycling; `<rows>*8` = each row lasts an eighth note.
- `` `...` `` — backtick string: multi-line mini-notation.
- `"0,0.3"` — comma = stack: both values pattern in parallel ("splits the pattern into two patterns").
- `"tops:4/4"` — `:4` = sample index; `/4` = slow by 4 (play over 4 cycles).
- `.decay(0.05)` — envelope decay; part of the ADSR set (attack, decay, sustain, release).
- `.clip(1)` — cut each triggered sample at one event length; mandatory on long samples.
- `.postgain(0.5)` / `.gain()` — linear volume multiplier at the end / start of the signal chain.
- `.note("C2")` — set pitch (samples default to C2); octave suffix optional.
- `.transpose(-8)` / `.trans(4)` — shift by semitones (trans = shorthand).
- `.add(...)` — add a pattern of numbers to notes/values ("Strudel does some magic... to properly add numbers to letters").
- `.orbit(5)` — assign the pattern to a numbered effects bus.
- `.duck(5)` — sidechain: this pattern ducks orbit 5.
- `.duckattack(0.3)` — duck recovery length, 0 (instant) to 1 (held).
- `.room(0.3)` — reverb send amount (0 none, 1 all, "10 if you want to destroy your speakers").
- `.size(0.8)` — reverb room size (0.8 = "somewhat small room").
- `.delay(0.3)` — delay send amount.
- `.delayfb(0.6)` — delay feedback; "don't write one for the feedback. Are you crazy?"
- `.compressor(-20)` — compressor on the pattern (threshold argument; added off-narration).
- `.lpf(200)` — lowpass filter cutoff in Hz.
- `.lpq(8)` — lowpass resonance ("for a bit more of an acid sound").
- `.lpe(4)` — lowpass envelope depth; multiplies cutoff by 2^n ("exponentially impactful number").
- `.lpdecay(0.3)` — lowpass filter envelope decay.
- `rand.range(50, 200)` — continuous random signal scaled to a range.
- `.log()` — print the values a pattern emits (debugging placement/rate).
- `.set(...)` / `set.mix(...)` — apply a pattern of controls; `.mix` join makes the *later* pattern's event rate win (the intuitive behavior).
- `setDefaultJoin('mix')` — make every function update behave like set.mix globally, "magically do the thing that we expect."
- `.as("n")` — interpret a bare number pattern as the `n` control ("shorthand for writing n of the thing").
- `.scale("C1:minor")` — map degree numbers to a scale rooted at C1; degree 0 = root.
- `.ply("2")` — repeat each event N times in place (note doubling).
- `.sometimesBy(0.125, fn)` / `sometimes` / `rarely` / `almostNever` / `never` — apply fn to events with the given probability (0.5 / ~0.25 / less / 0).
- `x => x.ply("2")` — JS arrow notation: "X is the pattern that we already have written."
- `.slow(2)` — play half as often; `"/2"` and `*0.5` are equivalents.
- `.fit()` — timestretch a sample to fill its event duration (pair with a `/N` length guess).
- `.vib(0.3)` — vibrato (appears in the final frame only, unnarrated).
- `all(x => x.mul(postgain(0.7)))` — apply a transform to every pattern at once (master bus).
- `.pianoroll()` / `._pianoroll({labels:1,width:1000})` / `._spectrum()` — visualizers; `_`-prefixed versions render inline in the editor.
