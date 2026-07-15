---
source:
  - https://www.youtube.com/watch?v=W24pteoigXk
  - https://www.youtube.com/watch?v=xAAbQMW0dFk
  - https://www.youtube.com/watch?v=ZCcpWzhekEY
creator: DJ_Dave
genre: dance/pop electronic
software: strudel (video 2 also shows Logic Pro as the finishing DAW)
---

# DJ_Dave process shorts — performance-file layout, DAW workflow, and dance-track scaffolding in Strudel

Three vertical shorts (each <100s) where DJ_Dave walks through *how she organizes* her Strudel code rather than building from scratch. All three are the same blue Strudel REPL (mini-notation chips, `slider()` widgets, `_punchcard`/`_scope` inline visuals); video 2 cuts to Logic Pro for the record-and-arrange half of her workflow. The unifying idea across all three files: **const arrays of pattern strings + one integer index + `pick()`**, so changing a single number re-patterns the kick structure and the "sidechain" gain pattern of every instrument at once — her build/drop macro for live shows.

**Shorts-crop caveat (applies to all three):** these are 9:16 crops of a widescreen editor with the webcam covering the top third. In video 1 the editor word-wraps, so lines are complete; in videos 2 and 3 long drum lines run off the right edge and their tails are unverifiable (flagged inline). In video 2 the top of the file (the `bassnotes`, `postgainnn`, `b34t`, `kickk`, `leads`, and likely `ssaw` definitions) is never on screen.

## Video 1 — "My process making my track Hard Refresh" (85s)

The YouTube title says *Hard Refresh*, but the file header on screen reads `@title Heartbeat` and the vocal sample is `"heartbeat:0"` — likely a working title or a different track file than the video title claims.

### Code

Final state assembled across frames (she toggles `beat` between 0/1/2 and comments/uncomments the hi-hat block during the video):

```js
/* @title    Heartbeat
   @by       DJ_Dave

*/

// ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡

setCps(150/60/4)

samples('github:algorave-dave/samples')
samples('github:tidalcycles/dirt-samples')

const Structures = [
  "{x ~!6 x ~ ~ x ~!3 x ~}%16",
  "{x*4}",
  "{~}",
]

const PG = [
  "{0.3 0.8!6 0.3 0.8!2 0.3 0.8!3 0.3 1}",
  "{0.3 0.8}%8",
  "{0.8}",
]

const beat = 2
//0-2

DRUMS: stack(
  s("tech:5").postgain(5).pcurve(2).pdec(1).struct(pick(Structures, beat)),
  s("[~ cp]").bank("KorgDDM110").speed(1).fast(2).postgain(0.15).lpf(3000),
// ---
// ---

  s("hh").struct("[x!3 ~!2 x!10 ~]").postgain(0.5).bank("RolandTR808").speed(1.25).jux(rev).room(sine.range(0.1, 0.4)).gain(0.6),
  s("~ hh").bank("RolandTR808").room(0.7).speed(0.75).gain(0.5).fast(4),

// ---
// ---
  s("breaks165").gain(0.4).loopAt(1).chop(16).fit().postgain(pick(PG, beat)),
  // s("psr:[2|12|24|25]".fast(4)).struct("x!7 ~ x!3 ~ x!3 ~").jux(rev).hpf(1000).postgain(pick(PG, beat)).speed(0.5).gain(0.2)
)
  ._punchcard({width: 600})

BASSLINE: note("f#3@8 c#3@3 d3@5 a3@8 c#3@3 d3@5 f#2@8 c#3@3 d3@5 d2@8 d3@3 c#3@5".slow(8))
  .struct("x!16")
  .sustain("0.5")
  .sound("[square, sawtooth]")
  .transpose("[-12, 0]")
  .coarse(2)
  .decay(0.075).gain(0.75) .hpf(150)
  .lpf(mouseX.segment(4).range(350,2000))
  // .lpf(slider(350, 350, 2000))
  .postgain(pick(PG, beat))
  ._punchcard({width: 600})

VOXCHOP1: s("heartbeat:0".slow(2))
  .note("g#1")
  .slice(8, "<5 6>".fast(2))
  .chop(32).cut(1).loopAt(4)
  .room(2)
  .gain("<0.6 1.6>".slow(2))
  .lpf(slider(4000,600,4000))
  .postgain(pick(PG, beat))
  ._scope({width: 600})

_VOXCHOP2: s("heartbeat:<1 0>".slow(2))
  .striate("<2 4>".slow(2)).ply("[4|8]".fast(8))
  .note("a1")
  .phaser(8).room(2).rfade(30)
  .cut(1).clip(1)
  .lpf(slider(5000,600,5000))
  .postgain(1.75)
  .room(1)
  ._scope({width: 600})

// all(x=> x.cut(2))
```

Fidelity notes:
- The first PG entry renders on screen as `0.816` / `0.8!2` / `0.8!3`; the `0.816` is almost certainly `0.8!6` (the 16-step count then matches `Structures[0]` exactly, and `!` renders close to `1` at this resolution).
- The hi-hat pair is commented out in some frames (`// s("hh")…`) and active in others; the `beat` const reads 2 (t0:08–0:32), 0 (t1:04), and 1 (t1:20) — she is demonstrating the switching, so there is no single "final" value.
- At t0:24 the BASSLINE lowpass was still `.lpf(slider(350, 350, 2000))` with the mouseX line commented; by t0:32 they are swapped (as narrated).
- `"cp"`, `"hh"`, `"breaks165"`, `"KorgDDM110"`, `"RolandTR808"`, `"square, sawtooth"`, `"-12, 0"`, `"x!16"` etc. render as boxed widget chips; underlying text as transcribed.

### Timeline

1. [0:00] Full file already written — this video is a *tour*, not a build. Header comment block, heart-emoji divider.
2. [0:05] "Below the header, I have my BPM set, which in Strudel is cycles per second" — `setCps(150/60/4)` (150 BPM, 4 beats/cycle).
3. [0:09] "Links to all the samples I'm going to use in this file" — `samples('github:algorave-dave/samples')` (her own sample repo) + dirt-samples.
4. [0:14] "These patterns I've been talking about where I'm able to quickly switch between kick patterns and also side chaining" — the `Structures` array (three kick structures: syncopated / four-on-floor `x*4` / silent `~`) and the `PG` (postgain) array (matching gain-dip patterns), both indexed by `const beat` via `pick(…, beat)`. During the video she flips `beat` 2→0→1.
5. [0:21] "Then we start getting into instruments. My drum stack here first, which right now is just playing a clap" — `DRUMS: stack(…)` with the kick (`tech:5` with pitch-envelope `pcurve/pdec`) silenced by `Structures[2] = "{~}"`, the DDM-110 clap on the offbeat, hi-hat lines toggled by comments, and the fitted `breaks165` loop.
6. [0:27] "And then this break loop sample down here" — `s("breaks165").loopAt(1).chop(16).fit().postgain(pick(PG, beat))`.
7. [0:30] "Then I have my baseline, which is playing these notes here" — the `@`-weighted 8-cycle note melody, forced to 16th notes by `.struct("x!16")`, square+saw stacked an octave apart.
8. [0:34] "The low pass filter is on a slider, which I could also change to my mouse movement if I want" — swaps `.lpf(slider(350,350,2000))` for `.lpf(mouseX.segment(4).range(350,2000))`.
9. [0:42] "Then I have a vocal chop down here" — unmutes `VOXCHOP1` (was `_VOXCHOP1` at t0:32–0:40); music plays.
10. [0:47] "And I included a second one as well, just for fun" — `_VOXCHOP2`, a striate/ply/phaser variant (still muted in every frame).
11. [0:53] The thesis: "Setting my code file this way just makes it possible for me to make a lot of changes at once, which is especially helpful during live shows if I want to do like a build and a drop."

### Techniques

- **Pattern-bank consts + one index = macro arrangement** — `const Structures = […]; const PG = […]; const beat = 2` then `.struct(pick(Structures, beat))` on the kick and `.postgain(pick(PG, beat))` on everything else. Editing one integer (0–2) simultaneously changes the kick pattern and every instrument's ducking — a one-keystroke build/drop.
- **Manual sidechain as a gain pattern** — instead of Strudel's `.duck`, the `PG` strings put a low gain value (0.3) exactly where the kick hits and 0.8 elsewhere, applied with `.postgain()` (post-FX so reverb tails duck too). The pump is *composed*, not triggered.
- **Comment-block toggles as arrangement** — `// ---` separator lines fence off groups (hats, percussion) she comments in/out live; muting a whole labeled pattern is one `_` prefix (`_VOXCHOP2:`).
- **Pitch-enveloped sample kick** — `s("tech:5").pcurve(2).pdec(1).postgain(5)` shapes a sample into a punchy pitched kick.
- **Fitted breakbeat** — `.loopAt(1).chop(16).fit()` locks a sampled break (`breaks165`) to the cycle tempo in 16 slices.
- **Octave-stacked chiptune bass** — one melody, `.sound("[square, sawtooth]")` + `.transpose("[-12, 0]")` = square an octave down layered with saw at pitch; `.coarse(2)` for lo-fi grit, tiny `.decay(0.075)` for pluck.
- **Weighted melody + struct** — the tune is written with `@` durations (`f#3@8 c#3@3 d3@5 …`) over 8 slow cycles, then `.struct("x!16")` retriggers it as driving 16ths.
- **Mouse as a performance controller** — `.lpf(mouseX.segment(4).range(350,2000))`: horizontal mouse position, sampled 4× a cycle, rides the bass filter hands-free (interchangeable with a `slider()`).
- **Two flavors of vocal chop** — VOXCHOP1: `.slice(8, "<5 6>".fast(2))` picks specific slices, `.chop(32).cut(1).loopAt(4)` grains them and chokes overlaps; VOXCHOP2: `.striate("<2 4>").ply("[4|8]".fast(8))` re-stutters random-count repeats through a phaser. Both repitched with `.note(…)`.
- **Every pattern carries its own visualizer** — `._punchcard({width:600})` on rhythmic layers, `._scope()` on vocal chops: the file doubles as a performance display.

## Video 2 — "my process in #strudel !!" (67s)

The Strudel-to-Logic workflow: how a live-coded loop becomes a finished, mixable record.

### Code

The visible Strudel file (the consts `bassnotes`, `postgainnn`, `b34t`, `kickk`, `leads` — and `ssaw`, presumably a registered supersaw — are defined above the crop and never shown):

```js
const energy = slider(6.281,5,12)

BASS: note(bassnotes.add("{-12  0}%8")).mux(ssaw).struct("x(8,8)")
  .detune(.5)
  .unison(4)
  .decay(0.25).release(1).sustain(0.3)
  .gain(1.5)
  .postgain(pick(postgainnn, b34t))
  .lpenv(energy)
._punchcard({height:60, width: 900})

_VOCALS: s("forget:2")
  .chop(4).loopAt(1).fit().gain(0.35).note(35.2)
  .postgain(pick(postgainnn, b34t))
  .hpf(mouseX.segment(4).range(200,500))
  .room(0.5)
  .lpf(slider(1,0.4,1).mul(100).pow(2)).lpq(5)
  ._scope({height:60, width: 900})

_SUB: note(bassnotes.add("0").sub("0")).struct("{0 1}%8")
  .s("gm_percussive_organ:1")
  .room(.8)
  .postgain(2)
  .lpenv(energy)
  ._punchcard({height:60, width: 900})

_LEAD: note(  pick("<0>/4", leads).add(12)).mux(ssaw).struct("x(8,8)")
  .gain(0.5)
  .detune(.55)
  .sustain(0.4)
  .hpf(100)
  .mask(1)
  .lpenv(energy)
  .postgain(pick(postgainnn, b34t))
._punchcard({height:60, width: 900})

DRUMS: stack(
  s("bd").bank("RolandTR909").postgain(1.5).struct(pick(kickk, b34t)),
  s("~ cp").bank("RolandTR808").fast(2).gain(0.6).lpf(5000).speed(1.2).end(0.045),
  s("~ hh!4 ~!5 hh*6").bank("RolandTR808").gain(0.3),
  s("~!1.33 lt").bank("RolandTR808").gain(0.4),
  s("hh*8").bank("RolandTR808").gain(0.4),
  s("~ oh").bank("KorgMinipops").postgain(0.2).fast(4).lpf(sine.range(5000, 8000)),
  s("white").struct("x(8,8)").decay(saw.range(0.03, 0.2).fast(4)).postgain(.3).almostNever(ply("2"))
)
._punchcard({height:60, width: 900})

// all(x => x.lpf(mouseX.segment(8).range(4000,200)))
// all(x => x.hpf(mouseX.segment(4).range(100,2000)))
```

Fidelity notes:
- `.mux(ssaw)` is transcribed as it renders; `mux` is not a stock Strudel op, so it (like `ssaw`) is presumably a helper defined in the unseen top of the file.
- The `energy` slider reads 6.281 at t0:00 and 10.474 at t0:16 — she sweeps it while recording.
- The white-noise line's `.struct("x(8,8)")` is boxed chips at tiny size (could be another Euclid variant) and its tail `…almostNever(ply("2"))` reaches the right crop edge — the closing characters are unverified. The `lt` line's `"~!1.33 lt"` is unusual but reads clearly.
- `_VOCALS`, `_SUB`, `_LEAD` are muted (`_` prefix) in the Strudel frames — she records/solos layers one at a time.

### Timeline

1. [0:00] In Strudel with a macOS screen-audio recorder panel open (top right): "when I want to build out a finished recorded track, I record whatever I'm doing in Strudel."
2. [0:08] "Usually I record each loop individually, but for the sake of the demonstration I'll just record them all together" — the file's mute-prefix layout (only `BASS` unmuted) is exactly the record-one-loop-at-a-time rig; she sweeps the `energy` lpenv slider (6.28 → 10.47) while it records.
3. [0:18–0:24] "Then I bring them into Logic" — Logic Pro, 145 BPM, 4/4, C maj: four audio tracks named BASS / VOCALS / SUB / LEAD with regions `BASS.6`, `VOCALS.`, `SUB.6`, `LEAD.4` at bar 17.
4. [0:26–0:34] "I just start building out the song structure. The recordings are longer a lot of the time, which helps if I'm using a randomizer — I can pick the parts that I like the most" — loop-drags a region (tooltip: `Loop Stop: 18 1 1 1, Repetitions: 2`), staggers entries: BASS runs long, VOCALS enters, then SUB, then LEAD.
5. [0:34–0:41] "It also makes it easier to mix the song later… easier in sessions if I'm working with other people."
6. [0:44–0:56] Cut to a full production session (playhead at bar 42): tracks LEADS, sub, Screen Recording…, EQ bass sidechain ×3, "EQ bass sidechain trial 2", 1970s Analog Arp, KICK, Audio 7/9, Absolute Zero, Above and Beyond; regions named "Tears In The Club (feat. …)". "When I'm really ready to flesh out a full track, this is the easiest way… to make a radio edit of whatever I've been working with. This way I can also make tweaks without having to re-record."
7. [0:58–1:05] Back to the Strudel file: "But then I still have the original code for performances, for remixes, for any edits I want to make" — scrolls the SUB/LEAD/DRUMS blocks and the commented `all()` mouse-macros.

### Techniques

- **Record loops into a DAW, arrange there** — the finished-track pipeline is: named Strudel patterns (BASS/VOCALS/SUB/LEAD) → record each loop as its own long audio take → Logic tracks named to match → loop/trim regions and stagger entrances to build song structure → radio edit. Long takes matter because randomized patterns never repeat: "I can pick the parts that I like the most."
- **Code stays the source of truth** — the DAW arrangement is a *render*; the Strudel file is kept for live shows, remixes, and re-records ("I still have the original code").
- **One global "energy" macro** — `const energy = slider(6.281,5,12)` feeds `.lpenv(energy)` on BASS, SUB, and LEAD at once: a single slider opens every synth's filter envelope together — the build knob.
- **Indexed sidechain, again** — `.postgain(pick(postgainnn, b34t))` on all pitched layers and `.struct(pick(kickk, b34t))` on the kick: the same shared-index (`b34t`) kick-pattern + gain-duck system as video 1, proving it's her standing template.
- **Octave-doubling in the note pattern** — `note(bassnotes.add("{-12  0}%8"))`: alternate 8ths sound the bass note an octave down then at pitch.
- **Perceptual filter slider** — `.lpf(slider(1,0.4,1).mul(100).pow(2))`: a 0.4–1 slider squared into 1.6k–10k Hz, giving an exponential (ear-linear) cutoff sweep; resonance via `.lpq(5)`.
- **Layered drum machine banks** — TR-909 kick under TR-808 clap/hats/low-tom plus KorgMinipops open hat with a sine-wobbled lowpass, and a white-noise 8th-note tick whose decay is modulated by `saw.range(0.03,0.2).fast(4)` (hats that continuously morph), spiced with `.almostNever(ply("2"))` (rare doubles).
- **Global mouse macros held in reserve** — commented `all(x => x.lpf(mouseX…))` / `all(x => x.hpf(mouseX…))` one-liners ready to uncomment for a whole-mix filter ride.

## Video 3 — "coding dance music in #strudel !!!!!" (96s)

Anatomy of a supersaw dance groove: one sound, two filter treatments, indexed sidechain, and a drum stack revealed by uncommenting.

### Code

Final state (t1:28; earlier frames show the rim/hat/psr drum lines still commented out and `gooo = 0`):

```js
setCps(140/60/4)

samples('github:algorave-dave/samples')
samples('github:tidalcycles/dirt-samples')

const gainnn = [
  "2",
  "{0.75 2.5}*4",
  "{0.75 2.5!9 0.75 2.5!5 0.75 2.5 0.75 2.5!7 0.75 2.5!3 <2.5 0.75> 2.5}%16",
]

const Structures = [
  "~",
  "x*4",
  "{x ~!9 x ~!5 x ~ x ~!7 x ~!3 < ~ x > ~}%16",
]

const gooo = 2
// off/on

bassline: note("[eb1, eb2]!16 [f2, f1]!16 [g2, g1]!16 [f2, f1]!8 [bb2, bb1]!8")
  .sound("supersaw")
  .slow(8)
  .postgain(2)
  .room(0.6)
  .lpf(slider(725,300,2000))
  .room(0.4)
  .postgain(pick(gainnn, gooo))
  ._punchcard({height:200, width:1670})

const arpeggiator = [
  "{d4 bb3 eb3 d3 bb2 eb2}%16",
  "{c4 bb3 f3 c3 bb2 f2}%16",
  "{d4 bb3 g3 d3 bb2 g2}%16",
  "{c4 bb3 f3 c3 bb2 f2}%16",
]

main_arp: note(pick(arpeggiator, "<0 1 2 3>".slow(2)))//.rev()
  .sound("supersaw")
  .lpf(300)
  .sustain(0.5).release(0.01).attack(0)
  .room(0.6)
  .lpenv(slider(3.53,1.25,6))
  .postgain(pick(gainnn, gooo))
  ._punchcard({height:200, width:1670})

drums: stack(
  s("tech:5").postgain(6).pcurve(2).pdec(1).struct(pick(Structures, gooo)),
  s("{~ ~ rim ~ cp ~ rim cp ~!2 rim  ~ cp ~ < rim ~ >!2}%8").bank("[KorgDDM110, dmx]").speed(1.2).fast(2).postgain(…   // tail off-screen
  s("sh").struct("[x!3 ~!2 x!10 ~]").postgain(0.5).lpf(7000).bank("RolandTR808").speed(0.8).jux(rev).room(sine.ran…   // tail off-screen
/////
  s("hh").struct("x*16").postgain(0.5).bank("RolandTR808").speed(1).jux(rev).room(sine.range(0.1, 0.4)).gain(0.6),
  s("~ hh").bank("RolandTR808").room(0.3).speed(0.75).gain(1.2).fast(4),
  s("psr:[2|5|6|7|8|9|12|24|25]").fast(16).almostNever(ply("0")).hpf(1000).postgain(pick(gainnn, gooo)).speed(0.5)…   // tail off-screen
)
._punchcard({height:200, width:1670})

// all(x => x.crush(mouseX.segment(4).range(12,1)))
// all(x => x.hpf(mouseX.segment(4).range(100,1000)))
// all(x => x.cut(2))
```

Fidelity notes:
- The rim/clap, shaker (`sh`), and `psr` lines run past the right crop edge; everything after the marked `…` is unverified (the hh lines fit because they're shorter). The stray `/////` line between drum entries is really in the file.
- `gainnn[2]` mirrors `Structures[2]` step-for-step (0.75 wherever the kick's `x` falls); the `!` repeats render near-identically to `1` at this size but the step-count alignment confirms the transcription.
- The bassline really has both `.room(0.6)` and `.room(0.4)` and two `.postgain()` calls (2, then the pick) — later calls win, so the earlier ones are leftovers.
- Slider drift: bassline lpf 725 in most frames, 1532.5 at t0:40 (mid-sweep); arp lpenv 2.19 early, 3.53 from t0:56.
- `gooo` is 0 at t0:24–0:32 and 2 at t1:20.

### Timeline

1. [0:00] "Here is what it sounds like with a four on the floor" — full groove playing; punchcards animate under every block.
2. [0:05] "I have this arpeggiator that's running through a sequence of notes or chords, using a supersaw sound, and I have the envelope set here, and also a low pass filter envelope that's on a slider" — `main_arp`: the 4-entry `arpeggiator` array cycled by `pick(…, "<0 1 2 3>".slow(2))` (a 4-chord progression, each chord spelled as a 6-note up-down arp in 16ths), `.sustain/.release/.attack` envelope, `.lpenv(slider(…))`.
3. [0:16] "If I change the slider, it's going to make it sound brighter" — sweeps the arp's `lpenv` slider (2.19 → 3.53).
4. [0:23] "A similar setup on this baseline up here — the low pass filter slider set pretty low so it sounds more like a bass, but it's using the same sound, just a different sequence of notes" — `bassline`: octave-stacked whole notes (`[eb1, eb2]!16 …` over `.slow(8)`, an Eb–F–G–F–Bb progression), same `"supersaw"`, `.lpf(slider(725,…))` doing the bass-vs-lead split.
5. [0:42] "On both of them I have post gain set to a variable. That variable makes it possible for me to side chain these sounds to a kick drum" — `.postgain(pick(gainnn, gooo))` on both; `gainnn[2]`'s 0.75-dips fall exactly on `Structures[2]`'s kick hits.
6. [0:51] "So if I bring those patterns in, it's also going to bring the kick drum in" — sets `gooo` to 2: one edit simultaneously switches every layer's gain pattern *and* un-silences the kick (`Structures` goes from `"~"` to the syncopated pattern).
7. [0:58–1:05] "Here is what it sounds like with a four on the floor" — the `x*4` variant (gooo = 1 territory) demoed.
8. [1:05–1:12] "I have another kick pattern set here, so I can bring that in with a couple more drums" — uncomments the rim/clap line (KorgDDM110 + dmx banks, 8-step rim/cp weave).
9. [1:23–1:36] "I'll bring a few more drums, too" — uncomments the shaker and hi-hat lines and the `psr` percussion (random sample per hit from `[2|5|6|7|8|9|12|24|25]`, `fast(16)`, rare `ply("0")` sprinkles, hpf'd to sit on top). Final frames: everything in, all three `all()` mouse-macros still commented and ready.

### Techniques

- **One synth, two filter identities** — bass and lead are both `"supersaw"`; the *only* meaningful difference is the lowpass treatment (bass: static low `lpf(slider(725…))`; arp: `lpf(300)` + big swept `.lpenv(slider(…))`). Timbre economy: one sound family keeps the mix coherent.
- **Chord progression as an array of arp strings** — `const arpeggiator = […4 strings…]` + `pick(arpeggiator, "<0 1 2 3>".slow(2))`: each string is one chord pre-spelled as a d4→bb2 descending 16th-note arp; the `<>` cycle walks the progression every 2 cycles. A commented `//.rev()` is kept as a one-keystroke variation.
- **Bassline as stacked-octave whole notes** — `note("[eb1, eb2]!16 …").slow(8)`: chords `[low, lower]` repeated 16×/8× then slowed, so the harmony changes every 2 cycles in lockstep with the arp progression.
- **The gooo master switch** — same pattern-bank trick as videos 1–2, but here narrated as *the* sidechain system: `gainnn` (postgain patterns, labeled `// off/on`) and `Structures` (kick patterns) share the index `gooo`, so the sidechain pump can never disagree with the kick pattern — silent kick pairs with flat gain "2", four-on-floor pairs with `{0.75 2.5}*4`, syncopated kick pairs with its mirrored 16-step dip pattern.
- **Duck-to-above-unity** — the gain patterns duck to 0.75 but *boost* to 2.5 between kicks, exaggerating the pump beyond what subtractive ducking gives.
- **Progressive uncomment as arrangement** — the drum stack is fully written in advance; the performance is just uncommenting lines (rim/clap → shaker → hats → psr) — build sections are pre-composed, not improvised.
- **Two banks in one hit** — `.bank("[KorgDDM110, dmx]")` layers the same rim/cp pattern through two drum machines simultaneously.
- **Randomized percussion topper** — `s("psr:[2|5|6|7|8|9|12|24|25]").fast(16).almostNever(ply("0")).hpf(1000)`: every 16th picks a random sample index, high-passed into a shimmer layer, ducked by the same `gainnn` pick.
- **Held-in-reserve global FX** — commented `all()` lines mapping mouseX to `crush(12→1)` (bitcrush intensifying as the mouse moves right) and `hpf`, plus a global `cut(2)` — the same "macro shelf" pattern as video 2.

## Vocabulary

Combined across the three videos (see the Switch Angel lesson for `setCps`, `s()`, `!n`, `.seg`, `.lpf/.lpenv/.lpq`, `slider()`, `.room`, `._scope/._pianoroll`, `jux(rev)` basics).

- `samples('github:user/repo')` — load a sample pack from GitHub; she always loads her own `algorave-dave/samples` plus `tidalcycles/dirt-samples`.
- `NAME:` (e.g. `DRUMS:`, `BASSLINE:`, `main_arp:`) — named pattern registration; `_NAME:` mutes it. Naming layers after mixer stems (BASS/VOCALS/SUB/LEAD) makes the DAW-recording step 1:1.
- `const X = [ "...", "...", … ]` + `pick(array, index)` — her core idiom: banks of interchangeable mini-notation strings selected by one shared integer (`beat`, `b34t`, `gooo`) to re-arrange many layers with one edit.
- `"{…}%16"` — polymetric mini-notation: fit the braced steps to 16 steps per cycle.
- `"a@8 b@3"` — `@` weights: hold a for 8 units, b for 3 (melody with durations).
- `"<a b c>"` — alternation: one entry per cycle (used with `.slow(n)` to stretch).
- `"[a|b|c]"` — random choice per event (random sample indexes, random ply counts).
- `"x(8,8)"` — Euclidean structure: 8 hits over 8 steps (straight 8ths) used as `.struct` on synth lines.
- `.struct("x!16")` — impose a rhythmic skeleton on a pattern (retrigger melody as 16ths).
- `.postgain(n)` — gain applied *after* the FX chain; her sidechain lever (patterned dips duck reverb tails too), distinct from `.gain()` (pre).
- `.pcurve(2).pdec(1)` — pitch-envelope curve and decay: turns `tech:5` into a punchy pitched kick.
- `.bank("RolandTR808")` / `.bank("[KorgDDM110, dmx]")` — choose drum-machine sample bank; a bracketed pair layers two banks on one pattern.
- `.loopAt(n)` — stretch a sample loop over n cycles at tempo; `.fit()` — squeeze a sample to its event duration; `.chop(n)` — cut into n grains; `.slice(n, pat)` — cut into n slices and index them; `.striate(n)` — interleave n progressive slices across events.
- `.cut(1)` — choke group: a new hit in group 1 silences the previous (keeps vocal chops monophonic); `.clip(1)` — trim sample to event length.
- `.ply("2")` — repeat each event n times; `.almostNever(fn)` — apply fn to a tiny random fraction of events (rare stutters).
- `.note("g#1")` on a sample — repitch the sample to that note; `.note(35.2)` — fractional MIDI-number pitching.
- `.transpose("[-12, 0]")` — layered transposition (octave-down copy + original); with `.sound("[square, sawtooth]")` gives a stacked two-oscillator voice.
- `.add("{-12  0}%8")` on a note pattern — patterned interval addition (octave alternation per 8th).
- `.unison(4).detune(.5)` — supersaw voice stacking and spread.
- `.attack(0).sustain(0.5).release(0.01)` / `.decay` — ADSR pieces set individually.
- `.coarse(2)` — sample-rate reduction (lo-fi); `.crush(n)` — bitcrush (12 = subtle, 1 = destroyed; her mouse macro sweeps 12→1).
- `.phaser(8)` — phaser rate; `.rfade(30)` — reverb fade time; `.end(0.045)` — play only the first 4.5% of a sample (clap transient).
- `mouseX.segment(4).range(a,b)` — mouse-position signal, sampled 4×/cycle, scaled to a–b: hands-free filter riding, also inside commented `all()` global macros.
- `slider(v,min,max).mul(100).pow(2)` — math on a slider signal to get an exponential (ear-friendly) sweep.
- `.mask(1)` — gate a pattern by a boolean pattern (here always-on, kept as a switch).
- `sine.range(a,b)` / `saw.range(a,b).fast(n)` — LFO signals modulating fx (wobbling hat lowpass, morphing noise-tick decay).
- `.mux(ssaw)` — as-rendered; `ssaw`/`mux` (video 2) and `bassnotes`, `postgainnn`, `b34t`, `kickk`, `leads` are user consts/helpers defined off-screen — evidence her files start with a personal helper preamble.
- `all(x => x.effect(…))` — apply an effect to *every* playing pattern; she keeps 2–3 commented at the file's foot as break-glass performance macros.
- `._punchcard({height:200, width:1670})` — inline step-grid visualizer sized to the editor; one per pattern turns the file into its own VJ display.
