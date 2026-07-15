---
source: https://www.youtube.com/watch?v=YvsoWehBbec, https://www.youtube.com/watch?v=v5V6dsMhB8E
creator: DJ_Dave
genre: electronic pop / house
software: sonic pi (Oatly set), hydra (Fail-safe visualizer)
---

# DJ_Dave — "Easy" live-coded for Oatly (Sonic Pi) + "Fail-safe" visualizer (Hydra)

Two very different artifacts from the same artist. The Oatly video (2021, 13 min) is
the real prize: a full commissioned live-coding performance of her song "Easy" in
**Sonic Pi**, code projected on the wall behind her, built from empty buffer to full
arrangement to teardown. The Fail-safe video (2026, 3.5 min) has no Sonic Pi at all —
it's a produced song visualizer whose footage is processed through a **Hydra** video
patch, with the Hydra code left on screen as a static overlay.

Evidence note: everything below is transcribed from projector frames shot at an angle
in a dark room (every 8s). The narration transcript is useless (lyrics/crowd only), so
all code is read off the wall. Structure and identifiers are high-confidence; exact
digits in a few pattern strings and arguments are flagged `[approx]`.

## Easy — Live Coded for Oatly (Sonic Pi)

### Code

Fullest reconstruction of the buffer near its peak (~8–11 min). Loops are listed in
the order they appear on screen. `[approx]` = readable but not pixel-certain.

```ruby
## hi my name is DJ DAVE                  # [approx wording — 3-line greeting header]
## this is my song EASY                   # [approx]
## thank you for having me oatly!!!

use_bpm 130                               # added mid-set; digit could be 138 [approx]

live_loop :met1 do
  sleep 1
end

cmaster1 = 120                            # global cutoff macro A (starts wide open)
cmaster2 = 120                            # global cutoff macro B

define :pattern do |pattern|
  return pattern.ring.tick == "x"
end

live_loop :kick, sync: :met1 do
  a = 2.5
  kick = "/Users/sarah/Desktop/dj_dave/samples/easy/kick.wav"
  sample kick, amp: a, cutoff: cmaster1 if pattern "x--x--x---x--x--"   # [approx dashes]
  sleep 0.25
end

live_loop :hhc, sync: :met1 do
  hhc = "/Users/sarah/Desktop/dj_dave/samples/easy/hhc.wav"
  sample hhc, cutoff: cmaster1 if pattern "x---x---xx--x---"            # [approx]
  sleep 0.25
end

live_loop :synthbass, sync: :met1 do
  c = 80                                   # ridden 70–100 over the set
  c1 = "/Users/sarah/Desktop/dj_dave/samples/easy/c.wav"
  g  = "/Users/sarah/Desktop/dj_dave/samples/easy/g.wav"
  eb = "/Users/sarah/Desktop/dj_dave/samples/easy/eb.wav"
  bb = "/Users/sarah/Desktop/dj_dave/samples/easy/bb.wav"
  sb = "/Users/sarah/Desktop/dj_dave/samples/easy/synthbass.wav"
  sample c1, cutoff: c
  sleep 4
  sample g, cutoff: c
  sleep 4
  sample eb, cutoff: c
  sleep 4
  sample bb, cutoff: c
  sleep 4
end
# mid-set variant: the four chord-stab lines get commented out and replaced by
#   sample sb, cutoff: c, amp: 2
#   sleep 16
# (one long synthbass phrase instead of the stepped C–G–Eb–Bb progression);
# at the outro she flips back — sb line commented, chord stabs uncommented.

live_loop :arp, sync: :met1 do
  a = 0.4                                  # read as 0.3 in some frames [approx]
  r = 0.125
  s = 0.1
  c = 100                                  # cutoff var added late in the set
  use_synth :saw
  notes = chord(:g3, :minor, num_octaves: 4).mirror
  tick
  play notes.look, sustain: s, release: r, amp: a, cutoff: c
  sleep 0.25
end

live_loop :vox, sync: :met1 do
  a = 0.6                                  # raised to 0.75 at the outro
  vox = "/Users/sarah/Desktop/dj_dave/samples/easy/versevox.wav"
  slice = rand_i(32)                       # [approx — could be rand_i(16)]
  slice_size = 0.125/2/2                   # [approx arithmetic, clearly 0.125/…/…]
  s = slice * slice_size
  f = s + slice_size
  sample vox, start: s, finish: f, amp: a
  sleep 1
end
# outro variant: the four slice lines are commented out and it becomes
#   sample vox, start: …, finish: …, amp: a   /   sleep 32
# — the full verse vocal plays through instead of random chops.

live_loop :hho, sync: :met1 do
  hho = "/Users/sarah/Desktop/dj_dave/samples/easy/hho.wav"
  sleep 0.5
  sample hho, cutoff: cmaster2
  sleep 0.5
end

live_loop :clap, sync: :met1 do
  clap = "/Users/sarah/Desktop/dj_dave/samples/easy/clap.wav"
  sleep 1
  sample clap, cutoff: cmaster2
  sleep 1
end

live_loop :cowbell, sync: :met1 do
  cowbell = "/Users/sarah/Desktop/dj_dave/samples/easy/cowbell.wav"
  sample cowbell, cutoff: cmaster2 if pattern "--x---x-x--x--x-"        # [approx]
  sleep 0.25
end

live_loop :synth, sync: :met1 do
  c = 120                                  # started 100, opened to 120
  synth = "/Users/sarah/Desktop/dj_dave/samples/easy/synth_sine.wav"
  sample synth, cutoff: c
  sleep 16
end

live_loop :chorus, sync: :met1 do
  stop                                     # parked until the drop (## stop to release)
  chorus = "/Users/sarah/Desktop/dj_dave/samples/easy/chorus.wav"
  sample chorus, amp: 1.5
  sleep 32
end
```

Fidelity flags:
- Sample paths are crystal clear in many frames: everything lives in
  `/Users/sarah/Desktop/dj_dave/samples/easy/` (kick, hhc, hho, clap, cowbell,
  c/g/eb/bb chord stabs, synthbass, synth_sine, versevox, chorus — all `.wav`).
- The x/- pattern strings are the least certain characters on the projector; kick is
  consistently a 16-step string starting `x--x--x-…`, but exact dash counts drifted
  across frames. Treat rhythm placements as approximate, the mechanism as exact.
- One frame (~8:24) hints the arp may briefly have been wrapped in a
  `with_fx :reverb, room: 1 … do` block; too blurry to confirm — unverified.
- `use_bpm` does not exist in the opening frames; it appears at the top of the buffer
  by ~7:20. Early-set tempo was whatever default she started with.

### Timeline

1. [0:00–0:30] Log shows "all runs completed / stop recording" — fresh take. She types
   the 3-line greeting header, the `:met1` metronome loop (`sleep 1`, nothing else),
   `cmaster1 = 120 / cmaster2 = 120`, and the `define :pattern` helper. Scaffold first,
   sound later.
2. [0:45–1:20] Kick loop: path into a variable, `a = 2.5`, one `sample … if pattern
   "x--x--x-…"` line, `sleep 0.25`. The whole drum machine idiom is established here.
3. [1:20–1:45] Closed hats (`:hhc`) — same idiom, different pattern string, also on
   `cmaster1`.
4. [1:45–2:40] `:synthbass`: loads five pitched sample stems (c, g, eb, bb chord
   stabs + a long synthbass phrase), then steps the progression `c1 → g → eb → bb`
   with `sleep 4` between — a chord progression made of .wav files, filtered by local
   `c = 80`. (An autocomplete popup for Sonic Pi's built-in `ambi_*` samples flashes
   by — she's using the IDE's completion constantly.)
5. [2:45–3:55] `:arp`: `use_synth :saw`, `notes = chord(:g3, :minor, num_octaves:
   4).mirror`, then `tick` + `play notes.look` at 16ths with short
   sustain/release and low amp — the only synthesized (non-sample) voice in the piece.
6. [4:00–5:10] `:vox` — the signature move: random 1-beat slices of the verse vocal.
   `rand_i` picks a slice index, `slice_size` arithmetic converts it to fractional
   `start:`/`finish:` positions, re-rolled every `sleep 1`. Glitch-chopped vocals with
   four lines of math.
7. [5:10–5:50] Open hat on the offbeat (`sleep 0.5 / sample / sleep 0.5`) and clap on
   the backbeat (`sleep 1 / sample / sleep 1`) — both on `cmaster2`, splitting the kit
   across the two filter macros.
8. [5:50–6:20] Cowbell on its own x/- pattern (also `cmaster2`).
9. [6:20–6:50] `:synth` — a 16-beat sine pad sample, one hit per phrase.
10. [~6:48] Breakdown 1: back at the top of the buffer, `cmaster1`/`cmaster2` slashed
    from 120 to ~10 — every drum voice muffles at once. `use_bpm 130` now sits at the
    top. Log confirms: samples playing with `lpf: 10`.
11. [~7:04] A red **Runtime Error: undefined method / "Did you mean?"** panel appears
    — a live typo. She fixes and re-evals within one frame; the music never stops
    (only the erroring loop's thread dies).
12. [7:20–8:00] Synthbass rework: chord-stab lines commented out, single
    `sample sb, cutoff: c, amp: 2 / sleep 16` in. Cutoff macros ridden back up
    10 → 90 → 100 → 120 — the filter-sweep rebuild.
13. [8:24] `:vox` gets a `stop`; a new `:chorus` loop is typed (chorus.wav, `amp:
    1.5`, `sleep 32`) but parked behind `stop`.
14. [8:56–9:30] Breakdown 2: `stop` inserted into the kick loop (kick vanishes),
    arp gets `stop` too; cmasters ridden again (log shows lpf 90/100/120).
15. [10:48] A full select-all flash (whole buffer highlighted) — big re-eval. The
    `stop` lines in `:synth` and `:chorus` are now commented (`## stop`): the sine pad
    and the chorus vocal enter together — the drop.
16. [11:36–12:16] Outro reshape: vox slice lines commented, full verse vocal plays
    (`sleep 32`, `a = 0.75`); arp gains `cutoff: c` with `c = 100`.
17. [12:32–12:56] Teardown mirrors the build: kick `stop`, synthbass `stop` and
    flipped back toward the chord stabs, `cmaster2 = 90` — the set exits filtered and
    thinning, loop by loop.

### Techniques

- **Metronome-loop clock** — an empty `live_loop :met1 do sleep 1 end` is the first
  thing written; every other loop declares `sync: :met1`. One master clock, N phase-
  locked loops; re-evaluating any loop can never drift the grid.
- **Three-line step sequencer** — `define :pattern do |pattern| return
  pattern.ring.tick == "x" end`, then any percussive loop is
  `sample X, … if pattern "x--x--x---x--x--"` at `sleep 0.25`. The x/- string is the
  entire drum-machine UI, editable live per-voice.
- **Global cutoff macros as a DJ mixer** — `cmaster1` (kick + closed hat) and
  `cmaster2` (open hat, clap, cowbell) are plain top-of-buffer variables passed as
  `cutoff:` everywhere. Editing one number and re-evaluating sweeps a whole bus:
  120 = open, 10 = breakdown, ride it back up for the build. Two variables = two-bus
  filter mixer.
- **Samples as instruments, code as arrangement** — nothing except the arp is
  synthesized. Kick, hats, clap, cowbell, chord stabs, bass phrase, pad, verse vocal
  and chorus vocal are pre-produced stems from her DAW; Sonic Pi is the sequencer,
  mixer, and performance surface. This is how a produced *song* (not a jam) gets
  performed live-coded.
- **Chord progression from pitched stem files** — one .wav per chord (`c.wav`,
  `g.wav`, `eb.wav`, `bb.wav`) stepped with `sleep 4`: a four-bar C-minor progression
  with zero music theory in the code, and a swappable `synthbass.wav` "chorus bass"
  variant toggled by commenting.
- **Random vocal chop** — `slice = rand_i(32); s = slice * slice_size; f = s +
  slice_size; sample vox, start: s, finish: f` re-rolled every beat: stuttering,
  never-repeating vocal glitches from one verse stem. For the outro she comments out
  the randomizer and lets the same file play whole — chop and full-song modes are one
  comment apart.
- **`stop` as a mute button** — a `stop` line at the top of a `live_loop` parks it
  silently; `## stop` (commented) releases it. Mute states + comments are the entire
  arrangement system: parts are pre-typed, then toggled in/out for breakdowns and
  drops.
- **Locals at loop-top as performance knobs** — `a = 2.5`, `c = 80`, `r = 0.125` sit
  on their own lines above the play call, so a one-character edit + re-eval is a
  volume/filter/envelope move. Same philosophy as the cmasters, scoped per-voice.
- **Beat-offset one-liners** — offbeat open hat as `sleep 0.5 / sample / sleep 0.5`
  and backbeat clap as `sleep 1 / sample / sleep 1`: placement by sleep-padding, no
  pattern string needed for simple placements.
- **Errors are survivable** — a mid-set undefined-method typo raised a red runtime
  error, killed only that loop's thread, and the rest of the music carried on while
  she fixed and re-evaluated. Live-coding failure mode: local, not global.
- **Set arc** — additive build (one loop at a time, drums → bass → arp → vox →
  percussion → pad) → filter breakdown (cmasters down) → rework under the breakdown →
  drop (un-`stop` chorus + pad together) → subtractive teardown that mirrors the
  intro. ~13 minutes, fully legible in the code's mute/comment states.

## Fail-safe (Visualizer) — Hydra

No Sonic Pi and no live coding here: it's a music video for a produced vocal
electronic-pop track ("Give me something to believe… so far away and I can't sleep").
One locked wide shot — DJ_Dave lying on grass with a laptop and a wired mic — is fed
through a **Hydra** (livecoding video synth) patch, and the patch's source code is
left on screen top-left for the whole video as a static overlay. Code-as-aesthetic:
the tool is the brand even when the video isn't a performance.

### Code

The overlay never changes across the video. The top of the chain (the source call,
e.g. `src(s0)` on the camera footage) is cropped above the frame edge in every shot;
what's visible starts mid-chain:

```js
// …source line(s) off-screen above…
  .scale(1, 1)
  .saturate(1)
  .contrast(1.3)
  .layer(src(o0)
      .mask(shape(4, 1, 1)
          .blend(o0, 0.3)
          .contrast(1.2)
          .saturate(0)
          .scale(0.8, 0.5)
          .pixelate(100, 100)
          .rotate(1, 0.1).blend(o0, 0.2)   // second blend arg [approx]
          .scrollX(0.4, 0.1))
      .scrollX(0.01))
  .modulate(o0, 0.02, 0.024)               // digits [approx]
  .blend(o0, 0.4)
  .out(o0)
```

Fidelity: structure and function names are clear in the opening frame; the flagged
numeric arguments shimmer with the video effect itself. Note the heavy use of `o0`
(the output buffer) inside its own chain — `blend(o0, …)`, `modulate(o0, …)`,
`layer(src(o0)…)` — this is a **feedback patch**: the previous frame is layered,
masked, and blended back into the next one.

### Timeline

- [0:00–0:40] Intro: grass scene mostly clean, green smears blooming around her
  outline (feedback trails picking up motion), code overlay visible top-left.
- [0:40–1:50] Verse/build: white sparkle-streak explosions radiate from her hand/mic
  on transients — the pixelated, rotated feedback layer smearing highlights outward;
  intensity tracks the song's energy.
- [1:50–2:40] Peak sections: whole-body white-out blooms, the masked rectangle layer
  (`shape(4,…)` = quad mask) visibly slides across the frame (`scrollX`), laptop and
  figure ghosting through feedback.
- [2:40–3:27] Falls back toward the calmer grass look for the outro; the code overlay
  is identical from first frame to last — the patch is fixed, the *footage* (and
  audio-reactive intensity of motion) does the work.

### Techniques

- **Feedback as the whole effect** — everything distinctive (trails, blooms, sparkle
  smears) comes from routing `o0` back into itself via `layer(src(o0)…)`,
  `.modulate(o0, …)` and `.blend(o0, 0.4)`. One camera source + a feedback loop =
  a full music-video look.
- **Masked sub-chain** — the inner `shape(4, 1, 1).…` chain builds a rectangle-masked
  copy of the feedback buffer that is desaturated (`saturate(0)`), crushed
  (`pixelate(100,100)`), rotated and scrolled — a glitch "window" drifting over the
  clean footage.
- **Slow drift, tiny numbers** — the motion params are all small (`scrollX(0.01)`,
  `modulate(o0, 0.02, …)`): the patch idles as a shimmer and only erupts when the
  underlying footage moves. Restraint in constants, drama from feedback gain.
- **Code overlay as identity** — the patch text is composited into the final video
  on purpose. For an AI DJ: showing the running code *is* the visual brand, even in a
  non-live artifact.

## Vocabulary

Sonic Pi (Oatly set):
- `live_loop :name do … end` — a named, hot-swappable concurrent loop; re-evaluating
  the buffer redefines it without stopping time.
- `sync: :met1` — block the loop's start until the named loop cues, phase-locking it
  to the metronome loop.
- `sleep n` — advance this loop's clock by n beats (0.25 = 16th grid, 4 = a bar of 4).
- `use_bpm 130` — set beats-per-minute for beat-based timing.
- `sample "<path>", opts` — play a .wav from disk; her instruments are absolute paths
  into `~/Desktop/dj_dave/samples/easy/`.
- `amp:` — gain (kick at 2.5, chorus at 1.5, vox 0.6–0.75).
- `cutoff:` — lowpass cutoff (MIDI-note scale, ~130 = open); the whole mix rides on
  variables passed here.
- `start:` / `finish:` — fractional (0–1) playback window into a sample — the vocal-
  chop primitives.
- `define :pattern do |pattern| … end` — user-defined function; hers turns an
  `"x--x"` string into a per-step boolean gate.
- `.ring` — make an array/string cycle infinitely.
- `.tick` / `.look` — advance and read a per-loop counter into a ring (`tick` on its
  own line advances; `look` reads without advancing).
- `if pattern "x--…"` — one-line conditional trigger: the step-sequencer idiom.
- `use_synth :saw` — select the synth for subsequent `play` calls.
- `play note, sustain:, release:, amp:, cutoff:` — trigger the current synth.
- `chord(:g3, :minor, num_octaves: 4)` — build a chord/arp note ring spanning 4
  octaves; `.mirror` appends its reverse for an up-down arp.
- `rand_i(32)` — random integer 0–31 (fresh every pass — her chop randomizer).
- `stop` — inside a live_loop: park the loop silently (her mute button); `## stop`
  un-mutes on next eval.
- `##` / `#` — comments; commenting code in/out per-eval is the arrangement tool.
- `cmaster1` / `cmaster2` — her convention, not a builtin: top-level cutoff variables
  shared across loops as bus-filter macros.

Hydra (Fail-safe visualizer):
- `src(o0)` — read the output buffer back in (feedback source).
- `.out(o0)` — write the chain to output buffer 0.
- `.layer(tex)` — composite another chain on top.
- `.mask(shape(4, 1, 1))` — clip a layer through a geometric mask (4 = quad).
- `.blend(o0, n)` — crossfade with the feedback buffer by n (persistence/trails).
- `.modulate(o0, …)` — displace pixel lookup by the feedback buffer (warp/smear).
- `.pixelate(100, 100)` — mosaic downsample.
- `.scrollX(a, b)` — horizontal offset (+ speed): drifting glitch windows.
- `.rotate(angle, speed)` / `.scale(x, y)` / `.saturate(n)` / `.contrast(n)` — the
  standard color/geometry operators, chained jQuery-style.
