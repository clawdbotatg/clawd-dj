---
source: https://www.youtube.com/watch?v=Mbeku_nj0Nk, https://www.youtube.com/watch?v=LaKT3pli5EQ
creator: DJ_Dave (+ Switch Angel on Cycles)
genre: hyperpop / digicore (Cycles), sample-based electronic pop / house (GitHub Universe)
software: Strudel (Cycles), Sonic Pi 3.2.2 (GitHub Universe)
---

# DJ_Dave x Switch Angel — "Cycles" (Live) + DJ_Dave — GitHub Universe 2020

Two performances, five years apart, that bracket DJ_Dave's practice: the 2020
GitHub Universe set is solo Sonic Pi (her original platform), the 2025 "Cycles"
collab with Switch Angel is Strudel. Together they show the same performer's
arrangement instincts translated across two livecoding systems — and Cycles
shows how two livecoders share one stage.

## Cycles — DJ_Dave + Switch Angel (Live, 2025)

~3.5 min, 195k views. A finished *song* performed live, not an improvisation.

### Performance architecture (who does what)

- **One codebase, one coder.** DJ_Dave sits cross-legged with the laptop and
  drives a single Strudel REPL for the entire piece. Switch Angel sits beside
  her with a handheld mic and **sings live** — she is the featured vocalist,
  not a second livecoder. (No second REPL is ever visible; the second laptop
  on the floor feeds the audio interface — a red Focusrite Scarlett.)
- **The vocal exists twice.** The track scrubs a pre-recorded vocal sample
  bank literally named `"cycles"` (`$vox: s("cycles").scrub(…)`) *while*
  Switch Angel sings over it live — coded vocal chops and live voice layered
  as separate parts. Near the end, DJ_Dave picks up a mic at ~2:56 too — both
  sing the outro while the code keeps playing.
- **Pre-written song, live-mixed.** All parts (`$bass`, `$drums`, `$vox`,
  `$melodics` + the `LEAD`/`DIGICORE`/`PAD` consts) exist in the buffer from
  the start; the performance is comment-toggling stack members, swapping
  variant instruments (`kick` → `kick3` → `kick2`), riding `slider()` widgets,
  and changing pattern indices. This is DJ_Dave's signature set-mode
  technique (same as the Intercell EPs): arrangement-as-editing.
- The screen overlay is the Strudel REPL keyed over the video (mirrored copy
  on the right side is decorative). `_pianoroll()` / `_scope()` visuals render
  inline in the code.

### Code (assembled across frames; overlay is stylized — fidelity flagged)

Hi-hat pattern bank [partial — visible only at t8]:

```js
const hhpat = [
  "x!4 ~!6 x!5 [x | ~]",   // [uncertain: middle of string]
  "x!16",
  " x!8"
]
```

Bass — two chord-tone phrases picked per 8 cycles, supersaw acid voice
[verbatim except where flagged]:

```js
const bassNotes = [
  "{F@7 G@9 C@7 A#@9 G#@15 D4 C3@7 A#@9}%8",
  "{F@7 G@9 C@7 A#@9 G#@15 D4 C3@7 A#@6 D@3}%8",   // [uncertain: final "D@3"]
]
const bassPat = pick(bassNotes,"<0 1>@8").sub(12)
$bass: note(bassPat).s("supersaw, jc:8:.1").seg(8).lpf(200)
  .lpenv(slider(3.1,0,8,.1))          // slider ridden live: 3.1→3.7→2.9→4.1→4.6→5.1→4.6
  .lpq(0).lps(.2).lpd(.2)
  .detune(rand.range(0.1, 0.7)).ftype(1).clip(1).begin(rand.div(2))
  .distort("2.5")                      // [uncertain: could be "2:.5" gain:mix form]
  .orbit(3)._pianoroll({height:30})
```

Late in the set (t168, ~2:48) the bass line is edited to
`.s("supersaw, jc:8:.3").seg(16).lpf(200)` — double-time 16th-note bass with
more of the `jc` layer blended in, and `.lpd(.1)`.

Drums — a stack of pre-baked consts (defs scrolled off-screen), toggled live:

```js
$drums: stack(
  kick,                          // ↔ kick3 (t96+), ↔ kick2 (t168+)
  hat.struct(pick(hhpat, "0")),  // index changed live: "0" → "2" → "1"
  snare.slow(1),                 // ↔ snare.slow(2) in the kick3 section
  // glitch,                     // uncommented for the final section (t168)
)._scope({height:30})
```

Organ stab riff [verbatim; name could read M1ORGAN or M10RGAN — "M1 organ"
(the Korg M1 house preset) is the musically likely reading]:

```js
$M1ORGAN: note(bassPat.sub(0)).s("jc:7").struct("{0 1}%8")
  .clip(1).gain(.7).rel(.2).hpf(25)   // [uncertain: hpf value]
```

Vocal chop loops — two `$vox` patterns over the "cycles" sample [partial]:

```js
$vox: s("cycles").scrub(irand(16).div(16).seg("16 8 16 16")).speed(-1)
  .ribbon(40,"{1 [1 .25] 1 2}%1")
  .clip(saw.fast(4).range(0,.2).add(.7))
  .room(.3).ir("pad:6").roomsize(.3).hpf(500)
  .orbit(7)

$vox: s("cycles").scrub("{.3@4 [~ .3] 0 [.1!2] [.1!2]}%4".add("<.455 <.45 .2 .1 .3>>"))  // [uncertain: scrub string + nested add]
  .room(.3).orbit(2).ir("pad:6").roomsize(.2)
  .ribbon(0, 1).att(.2)
  // .lpf(400)                        // commented out live at ~3:04
  .orbit(7)
```

(One of the two `$vox` lines is muted `_$vox:` at any given time — they are
alternate chop treatments of the same vocal, swapped between sections.)

Melodic layer bank + performance stack:

```js
const PAD = s("pad:7:.5").scrub(rand.seg(8).rib(4,2)).phaser(.3).orbit(5).gain(.3)

const LEAD = note("{D#@7 A#@9 D#@7 F#@6 D#@3}%8".add(-12)).s("jc:5")   // [uncertain: F#@6 vs F@6]
  .seg(8).begin(rand.mul(.1)).detune(.37).clip(1).lpf(200)
  .lpenv(slider(4.8,0,8,.1))          // ridden live: 2.1→3.5→4.8→7.1→6.7→1.3
  .lpsustain(.2).lpd(.25).gain(.6).dist("2:.4").orbit(5)

const digiNotes = [
  "{0 D# A# F4 ~ G4 ~ D4 ~ D#4 ~ 0 D# A# D#4 A#4}%8",   // [partial — 4 similar strings in the bank]
  …
]
const DIGICORE = note(pick(digiNotes, "<0 1 2 3>/2").add("12")).s("sawtooth")
  .lpf(300).lpenv(tri.fast(.5).mul(3).add(slider(1.3,0,4,.1))).lpd(.3)   // [partial]
  ._pianoroll({height:30})

$melodics: stack(
  LEAD,
  DIGICORE,   // toggled per-section
  PAD,
)
```

### Timeline

1. [0:00] Camera only — the duo seated on the floor, DJ_Dave typing, Switch
   Angel with mic. Music already running (intro).
2. [0:08] REPL overlay fades in: `hhpat`, bass, drums visible. Bass lpenv
   slider at 3.1. Full groove: kick + hat + snare, vocal chops.
3. [0:16] Switch Angel starts singing verse 1 live over the scrubbed
   `"cycles"` chops.
4. [0:56] First breakdown: `kick,` and `snare.slow(1),` commented out —
   hats-only under the vocal.
5. [1:04] Drop: kick + snare uncommented back in.
6. [1:28–1:36] Chorus ("And if you're falling, I'm falling with you").
7. [1:36] `$melodics: stack()` section begins assembling: first all members
   commented, then `LEAD` + `PAD` in with `// DIGICORE`.
8. [1:36–1:52] Second breakdown/rebuild: kick and snare commented, hi-hat
   `pick(hhpat, …)` index changed, then `kick3` + `snare.slow(2)` in — a
   heavier drum variant for the second half. Bass slider swept 3.7→2.9→4.1.
9. [2:32] Full melodic drop: `LEAD, DIGICORE, PAD` all active. LEAD lpenv
   slider ridden up 4.8→7.1 (audible filter opening).
10. [2:48] Final-section edits: bass to `.seg(16)` double-time, `kick2` swap,
    `glitch` layer uncommented, `.lpf(400)` on the vox chops commented out
    (vocal chops open up full-range).
11. [2:56] DJ_Dave picks up a mic — **both** sing the outro over the running
    code ("Heat. Heat. Heat.").
12. [3:12–3:30] Outro strip-down: `kick2` commented, snare + glitch
    highlighted and commented — song ends on melodics + voices.

### Techniques

- **Song-mode livecoding** — the whole arrangement pre-written as named consts
  and labeled patterns; the live performance is toggling stack members and
  riding sliders. Zero code is written from scratch on stage.
- **Instrument variants as consts** — `kick` / `kick2` / `kick3`,
  `snare.slow(1)` / `.slow(2)`: section changes are one-word swaps inside
  `$drums: stack(…)`.
- **Pattern banks + `pick()`** — `hhpat`, `bassNotes`, `digiNotes` arrays with
  `pick(bank, "<0 1>@8")` or a live-edited literal index. One integer edit =
  new phrase.
- **Layered synth voice** — `.s("supersaw, jc:8:.1")`: two sound sources in
  one `s()` call with a blend amount, later rebalanced to `:.3`.
- **Slider-riding as the main "instrument"** — both bass and LEAD keep
  `lpenv(slider(…))` filter-depth widgets that get swept continuously across
  sections; the printed slider value differs in nearly every frame.
- **Vocal sample scrubbing** — `s("cycles").scrub(…)` with random
  (`irand(16).div(16)`) or hand-written position patterns, `.speed(-1)`
  reverse playback, `ribbon()` to freeze a random chop sequence into a
  repeating riff, convolution reverb via `.ir("pad:6")`.
- **Live vocalist over coded chops** — the same voice appears as code
  (scrubbed sample) and as live performance simultaneously; the human vocal
  is the one element the code doesn't control.
- **Grouped stacks per role** — `$drums: stack(…)`, `$melodics: stack(…)`:
  one label per musical role so a whole section can be muted/unmuted or
  reshaped in one place, with `_scope`/`_pianoroll` per stack as instrumentation.

## GitHub Universe 2020 — DJ_DAVE Sonic Pi set

~30 min, six original songs, Sonic Pi v3.2.2 on a Mac, full screen capture
(editor left; Scope, Log, Cues panels right; buffer tabs |0|–|9|). This is the
richest public record of DJ_Dave's original platform: an entire DJ *set* of
pre-written songs, one buffer per song, mixed live by editing code.

### The set structure (one buffer per song, all at 125 BPM)

| ~Time | Buffer | Song | Sample bank |
|---|---|---|---|
| 0:16–6:40 | 4 | VELVIA | `samples/Velvia/` |
| 6:40–11:50 | 1 | CANT DO THIS ALONE | `samples/mud/125/` |
| 11:52–16:20 | 5 | MISS_MADELINE | `samples/MM/` |
| 16:40–20:40 | 3 | MURIELLE | `samples/murielle/` |
| 21:00–25:00 | 6 | MK | `samples/mk/` |
| 25:04–29:36 | 2 | DEALER'S GONE | `samples/von/` |

Every song shares the identical skeleton, which is the deepest lesson here —
the *set* is six instances of one template:

```ruby
##| SONG TITLE

use_bpm 125                 # constant across the whole set = beatmatched for free

live_loop :met1 do          # bare metronome; plays nothing
  sleep 1
end

cmaster1 = 100              # master-cutoff buses: drums / hats-extras / textures
cmaster2 = 100
cmaster3 = 100

##| PERC
live_loop :kick, sync: :met1 do
  ##| stop                  # ← THE fader: commented = playing, uncommented = kill
  a = 5
  kick = "/Users/sarah/Desktop/dj_dave/samples/<song>/kick.wav"
  sample kick, amp: a, cutoff: cmaster1
  sleep 1
end
# … clap, hhc, xtra1, xtra2, woodblock/ding/perc …
##| SYNTHS
# … basses (synth + pre-rendered stem versions), arps …
##| VOX
# … long vocal-stem loops with hand-tuned sleeps …
```

Every loop is `sync: :met1`; every loop's first body line is a `stop` toggled
with Cmd+/ ("Toggle line comment" flashes in the status bar all set long),
then Run re-evaluates the buffer. Muted parts hold a bright `stop` so a
full-buffer re-run is always safe/idempotent (Log: `Redefining fn
:live_loop_X` / `Thread … exists: skipping creation`).

### Representative code (all verified against the Log panel)

Groove loop with counted rhythm blocks (VELVIA shaker):

```ruby
live_loop :hhc, sync: :met1 do
  ##| stop
  r = 1
  a = 0.5
  p = -0.3
  shake = "/Users/sarah/Desktop/dj_dave/samples/Velvia/hhc.wav"
  8.times do
    sample shake, rate: r, amp: a, cutoff: cmaster2, pan: p
    sleep 0.25
  end
  sample shake, rate: 0.75, amp: a, cutoff: cmaster2, pan: p   # pitched-down turnaround
  sleep 0.5
  6.times do
    sample shake, rate: r, amp: a, cutoff: cmaster2, pan: p
    sleep 0.25
  end
end
```

Melody with slow triangle-LFO automation via `line().mirror` (VELVIA arp):

```ruby
with_fx :reverb, mix: 0.6 do
  live_loop :arp, sync: :met1 do
    stop
    a = line(0.5, 1, steps: 128).mirror.look
    r = line(0.25, 0.5, steps: 128).mirror.look
    use_synth :saw
    notes = (ring :e3, :g3, :b3, :d4, :e4, :g4, :b4, :d5)#.shuffle
    tick
    play notes.look, amp: a, cutoff: 70, release: r, pan: 0.25
    sleep 0.25
  end
end
```

Long-form vocal arrangement inside one loop — verse structure as data, with
hand-tuned off-grid sleeps to butt full sung phrases against the 125 BPM grid
(VELVIA `:vox1`; same pattern in every song):

```ruby
with_fx :flanger, mix: 1 do
  live_loop :vox1, sync: :met1 do
    ##| stop
    a = 1
    c = 100
    v1a = "/Users/sarah/Desktop/dj_dave/samples/Velvia/v1_01.wav"
    # … v1b v1c v1d v2a v2b …
    sleep 1
    sample v1a, amp: a, cutoff: c, start: 0.0019
    sleep 15.45
    sample v1b, amp: a, cutoff: c
    sleep 16.4
    sample v1c, amp: a, cutoff: c, start: 0.002
    sleep 15.63
    sample v1d, amp: a, cutoff: c, start: 0.001
    sleep 15.52
    sleep 20
  end
end
```

(One-shot sections end in `sleep 1000` / `sleep 9000` / `sleep 100000` —
play once, then park forever.)

Ring arpeggio chord progression, 2 bars per chord (DEALER'S GONE):

```ruby
live_loop :arpsynth, sync: :met1 do
  ##| stop
  p = 0.2
  c = 100
  a = 0.6
  r = 0.15
  use_synth :saw
  arpc  = (ring :c3, :eb3, :g3, :c4, :eb4, :g4, :c5, :eb5)
  arpg  = (ring :g2, :bb2, :d3, :g3, :bb3, :d4, :g4, :bb4)
  arpbb = (ring :bb2, :d3, :f3, :bb3, :d4, :f4, :bb4, :d5)
  32.times do
    play arpc.tick, release: r, pan: p, cutoff: c, amp: a
    sleep 0.25
  end
  32.times do
    play arpg.tick, release: r, pan: p, cutoff: c, amp: a
    sleep 0.25
  end
  32.times do
    play arpbb.tick, release: r, pan: p, cutoff: c, amp: a
    sleep 0.25
  end
  32.times do
    play arpc.tick, release: r, pan: p, cutoff: c, amp: a
    sleep 0.25
  end
end
```

The same Cm→Gm→Bb→Cm progression is mirrored by a 16th-note saw bass
(`:synthbass2`: 32× `play :c2` / `:g2` / `:bb2` / `:c2`) and a third saw
layer an octave up — three loops, one progression.

Coded filter-sweep automation on vocal chops (DEALER'S GONE `:randvox`):

```ruby
with_fx :echo do
  live_loop :randvox, sync: :met1 do
    stop
    a  = (line 2, 4, steps: 16).mirror.tick
    cu = (line 100, 120, steps: 16).mirror.tick
    c  = "/Users/sarah/Desktop/dj_dave/samples/von/vox/c_1.wav"
    bb = "/Users/sarah/Desktop/dj_dave/samples/von/vox/bb_1.wav"
    g  = "/Users/sarah/Desktop/dj_dave/samples/von/vox/g_1.wav"
    eb = "/Users/sarah/Desktop/dj_dave/samples/von/vox/eb_1.wav"
    sample [c, bb, g, eb].choose, amp: a, cutoff: cu, pan: 0
    sleep 0.5
  end
end
```

Hand-coded echo decay + hard pan alternation (MURIELLE `:TTMFL`): the same
vocal snip repeated `pan: -0.5 / 0.5` with stepwise falling amps 3 → 2.5 → 2
→ 1 — a delay effect written as arrangement. Harp arpeggio through
`with_fx :ping_pong, pan_start: -0.5` with three 8-note rings (E/D/C chords,
16+16+32 steps).

Sliver sampling (MK `:cello`): four cello one-shots each cut to just the
attack — `sample a, start: 0.05, finish: 0.1, pan: p1` — stacked per beat
inside `with_fx :reverb, mix: 0 { with_fx :echo, mix: 1 { … }}` (a fully-wet
echo bed under a dry shell), turning bowed notes into a plucked texture.

Vocal thickening tricks: double-trigger the same stem 5 ms apart
(`sample vox1 …; sleep 0.005; sample vox1 …` in CANT DO THIS ALONE's chorus);
layer `pitch: 0` + `pitch: 3` copies (`:wysilt`); dub-drop a phrase at
`pitch: -12` inside a one-shot `with_fx :flanger, mix: 0.9` wrapper (MK
`:v2`); chop one vocal (`worried.wav`) into a long phrase (`finish: 0.43`) vs
a 1-beat stutter (`start: 0.41, finish: 0.5`) repeated 8×.

### Timeline highlights

1. [0:16] Set already running as video starts: VELVIA texture intro
   (shaker/hats/clicks/vocal chops), kick and clap muted.
2. [~1:20] Kick + FM bass drop; [~1:28] main vocal `:vox1` in.
3. [~2:08] Vocal chops out, `cmaster1/2/3` edited 100 → 120 — grouped filter
   open as the groove brightens.
4. [3:30–5:12] Melodic build: saw arp in, square melody in, `never_know.wav`
   hook in — then both melodics `stop`ped for a breakdown.
5. [6:40] **Transition 1 (overlap crossfade):** buffer 1 (CANT DO THIS
   ALONE) launched while VELVIA still plays — same loop names, same BPM, so
   the new buffer's parts land on the shared grid; VELVIA parts then get
   `stop`s typed in one by one.
6. [7:36–11:00] Song 2 arc: square solo `:rand` + `:trying` + `:fun` stack
   up; amp rides typed live (`a = 0.3` → `0.4`); `worried.wav` chop verse;
   drop with kick amp 5 / lpf 120.
7. [11:52] **Transition 2 (same overlap technique):** buffer 5
   (MISS_MADELINE) percussion up under song 2, then buffer 1 parts stopped.
8. [13:44–14:56] MM arc: bigsawbass stems (F–Eb–Ab–Db, 8 beats/chord),
   blip/tap `.choose` textures, `:blade` pentatonic lead with
   `line().mirror` cutoff+pan sweeps; mass-stop of five loops staged via a
   big selection + run (Log bursts `=> Stopping thread …` × 5); cmasters
   100 → 120.
9. [16:40–20:40] MURIELLE: verse stems under the groove; clap pulled;
   breakdown by killing the kick; `:TTMFL` vocal echo launched *then its
   `stop` re-typed while playing* — a scheduled one-shot that self-terminates
   after exactly one pass; square harp arp enters; kick relaunched for the
   chorus (run 659).
10. [21:00–25:00] MK: `bd_fat` built-in kick (the `bd_808.wav` path variable
    is assigned but unused), cello slivers, FM pentatonic arp — she edits its
    groove live from `sleep 0.25` to `sleep [0.25, 0.5].choose`.
11. [25:04] **Transition 3 (hard cut):** MK fully stopped (`All runs
    completed` / `Pausing SuperCollider Audio Server`), buffer 2 (DEALER'S
    GONE) rebuilt from silence: kick → hats → bigdrum/shiny → glitter →
    saw basses → arps → vocal chops → "bloody hands" / "know your body like"
    stems. Both crossfade *and* hard-cut transitions are in her vocabulary.
12. [29:00+] Outro: vocal loops re-armed with `stop`s, `cmaster` sweep down
    (Log shows `lpf: 10` muffling the percussion) — set ends on filtered
    percussion + arps.

### Techniques

- **One buffer per song = a DJ crate.** Six songs, identical scaffolding,
  constant 125 BPM. Transitions are either overlap-crossfades (launch the
  next buffer's percussion while the old song plays, then stop the old parts
  one by one) or a hard stop-all + rebuild-from-percussion.
- **`stop`-toggle as channel fader.** Comment/uncomment a loop's first-line
  `stop` + re-run. Also *pre-arming*: re-type `stop` into a still-playing
  loop so the next Run kills several parts at once, or so a long vocal loop
  self-terminates after exactly one pass.
- **`cmaster` cutoff buses as macro faders.** Global vars threaded through
  `cutoff:` of whole instrument groups; editing `100` → `120` and re-running
  is her filter-knob sweep (and `cutoff: cmaster1-5` for relative offsets).
  Direct precursor of the Strudel `slider()` riding in Cycles.
- **Per-loop param locals** (`a`, `r`, `p`, `c` = amp/rate-or-release/pan/
  cutoff) at the top of each loop — every level ride is a one-character edit
  at a predictable location.
- **Own-sample kits, path variables as patch lists.** Everything under
  `~/Desktop/dj_dave/samples/<song>/`; loops bind WAVs to named vars. Trims
  via tiny `start:` offsets (0.0019, 0.005), `finish:` windows, `rate:` for
  pitch (0.75 turnarounds, 0.9/0.94 vocal slow-downs), `pitch:` shifts.
- **Counted rhythm blocks** (`8.times`/`sleep 0.25` + turnaround +
  `6.times`) instead of pattern strings — rhythm as literal Ruby structure,
  asymmetric claves via mixed sleep values (`2.times(0.75)` + `3.times(0.5)`
  + `sleep 4.5`).
- **`line(a, b, steps: n).mirror.tick/.look` as LFOs** on amp, cutoff,
  release, pan — slow triangle sweeps with zero extra machinery.
- **Constrained randomness:** `(ring …).shuffle.tick`,
  `(scale :f3, :minor_pentatonic).shuffle`, `[x, y, z].choose` on samples,
  sleeps, pans, rates — generative sparkle on ornaments only; kick, bass, and
  vocals stay deterministic. Includes pinned randomness like `[0.77].choose`
  (a one-element choose kept as an adjustable slot).
- **FX are part identity, wrapped outside the loop** — `with_fx` chains
  belong to a part permanently (flanger on basses, distortion→reverb on
  claps, reverb→wobble→panslicer on a chorus vocal, triple
  flanger→reverb→slicer on backgrounds); live variation comes from
  stop-toggles and numbers, never from re-wiring FX mid-set.
- **Commented alternates as a pre-composed menu:** unused `##| sample …`,
  `##| sleep 96`, `##| 2.times do`, alternate note-scales and `line()` mixes
  stay inline, ready to enable — the same philosophy as Cycles' commented
  stack members.
- **The Log is the meter bridge.** She verifies every run by reading resolved
  amp/pan/lpf values back from the Log; the Cues panel doubles as a
  what's-playing display.

## Vocabulary

Strudel (Cycles):

- `$name:` / `_$name:` — play / mute a labeled pattern; `stack(a, b, c)`
  groups layers under one label.
- `pick(bank, "<0 1>@8")` — choose from a pattern array by (patternable)
  index.
- `"{F@7 G@9 …}%8"` — mini-notation with per-step durations (`@n`) fitted to
  8 steps per cycle.
- `.s("supersaw, jc:8:.1")` — layered sound source: two synths/samples with a
  blend amount.
- `.lpenv(slider(v,min,max,step))` — filter-envelope depth exposed as an
  on-screen slider to ride live.
- `.scrub(pos)` — play a sample from patterned/random positions;
  `irand(16).div(16)` for random chop points, `.speed(-1)` reverse.
- `.ribbon(seed, cycles)` / `.rib(…)` — freeze randomness into a repeating
  loop.
- `.ir("pad:8")` — convolution reverb using a sample as impulse response.
- `.begin(rand.div(2))` — random sample start offset per event.
- `tri.fast(.5).mul(3).add(x)` — signal math as an LFO into any parameter.

Sonic Pi (GitHub Universe):

- `live_loop :name, sync: :met1 do … end` — a named loop synced to the
  metronome loop; re-running redefines it seamlessly at its next pass.
- `stop` — inside a live_loop, kills that loop when evaluated; `##|` is
  Sonic Pi's comment marker (so `##| stop` = armed but inert).
- `use_bpm 125` — per-buffer tempo.
- `sample path, amp:, rate:, pan:, cutoff:, start:, finish:, pitch:, attack:` —
  play a WAV with per-call shaping; `start:`/`finish:` are 0–1 positions.
- `play :e3, amp:, cutoff:, release:, sustain:, pan:` — play a synth note;
  `use_synth :saw | :square | :fm | :blade` selects the voice.
- `with_fx :reverb|:flanger|:echo|:distortion|:slicer|:panslicer|:wobble|:ping_pong, mix: x do … end`
  — effect wrapper (nestable) around loops or single hits.
- `(ring :a, :b, :c)` — cyclic list; `.tick` / `.look` advance/read a
  per-loop counter; `.shuffle` permutes; `(scale :f3, :minor_pentatonic)`
  builds note lists.
- `(line a, b, steps: n).mirror` — linear ramp up/down (triangle LFO) sampled
  by `.tick`/`.look`.
- `[a, b, c].choose` — uniform random pick (works for samples, sleeps, pans).
- `n.times do … end` + `sleep` — rhythm as counted blocks.
- `cue` / `sync` — the Cues panel logs every loop pass as `/live_loop/<name>`.

## Cross-video takeaway

The 2020 Sonic Pi set and the 2025 Strudel duet are the same performance
system in two languages: pre-write the whole song as named, individually
mutable parts; make every part's first line a kill-switch; group parts under
master controls (cmaster vars → `slider()` widgets / stacks); keep alternate
material inline as comments; then perform by *editing*, not typing — toggles,
number nudges, index swaps — while visualizers (Scope/Log → `_scope`/
`_pianoroll`) confirm what's actually sounding. What changed in five years:
mini-notation replaced counted `n.times` blocks, sliders replaced re-run
variable edits, and a live vocalist joined the loop the code can't control.
