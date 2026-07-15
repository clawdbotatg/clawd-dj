---
source: https://www.youtube.com/watch?v=2F85nuwf4m4
creator: DJ_Dave
genre: techno / live-coded club (Intercell EP)
software: Sonic Pi
---

# Intercell EP Live Coded: Part 02 - idc [live sketch]

A 3.5-minute venue-filmed performance sketch (warehouse show, code projected on a
brick wall, live visuals by LADYBAMBS), not a screencast. There is **no narration**
(auto-captions contain only `[Music]`/`[Laughter]`), and the camera never gives a
clean full-screen view of the editor — so unlike a screencast lesson, the code
below is a **partial reconstruction** from 1080p frame crops of the wall
projection, cross-checked against Sonic Pi's log/cue panes, which ARE readable in
several frames. Software identification is unambiguous: `live_loop` / `with_fx` /
`use_synth` / `use_bpm` syntax, the `define … pattern.ring.tick` idiom, Sonic Pi's
log format (`{run: 26, time: 1.4504, thread: :live_loop_arp}`), and its cue list
with a `tempo-change [130.0]` entry.

This is part 2 of a 5-part live-coded EP; the end-card menu lists: PART 01 React,
PART 02 IDC, PART 03 Bloom, PART 04 Bitrot, PART 05 Array. Credits: directed by
DJ_Dave, live visuals LADYBAMBS, video Sam Klegerman / Ella Warren, produced by
Hannah Peale [GODMODE] and Hannah Hicks [Against All Evil]. Rig: laptop running
Sonic Pi INTO a Pioneer DJ mixer she rides throughout — the live-code and DJ-mixer
layers are both part of the performance.

## Final code

VERBATIM CAPTURE NOT POSSIBLE — flagged reconstruction. The projection is warped
over a brick wall and the camera is wide; roughly 60–70% of tokens are legible
across all frames combined. `«?»` marks unreadable/uncertain tokens; loop names
are taken from the log pane where the editor text was too blurry. Structure,
indentation, and every value shown were read off actual frames.

```ruby
# ##### (comment banner)
# ███ IDC ███   <- ASCII-art "IDC" title comment at top of file

use_bpm 130          # cue list shows tempo-change [130.0]

live_loop :met1 do   # bare metronome loop; everything else sync's to it
  sleep 1
end

cmaster1 = 13«?»     # global cutoff macros (~130); two of them,
cmaster2 = 13«?»     # separate cutoff busses for drums vs. percussion

define :pattern do |pattern|
  return pattern.ring.tick == "x"
end

samp    = "~/Desktop/dj_dave/samples/singles"
bitsamp = "~/Desktop/dj_dave/samples/bitrot"
«vox_dir?» = "~/Desktop/dj_dave/samples/«idc?»"

live_loop :kick«?», sync: :met1 do
  ##| stop
  a = 2
  sample «kick_sample», amp: a, cutoff: cmaster1 if pattern "x-------x--..----x------x-x-----"  # exact string unreadable
  sleep 0.25
end

live_loop :crshfade, sync: :met1 do
  with_fx :slicer, invert_wave: 1, phase: 0.25, wave: 1, mix: 0.8, smooth«?»: 0.6 do
    ##| stop
    a = 4
    sample samp, "crshfade", amp: a, rate: 0.5
    sleep 32
  end
end

live_loop :snr«?», sync: :met1 do
  ##| stop
  a = 1
  snare = "~/Splice/sounds/packs/Snare City/Black_Octopus_Sound_-_Snare_City/Heavy_Snares/SC_Snare_Th_04.wav"
  sleep 1
  sample snare, amp: a, cutoff: cmaster1
  sleep 1
end

with_fx «:echo?», mix: 0.75«?», «?»: 1 do
  live_loop :hhc, sync: :met1 do          # log: sample "...analoghhc.wav", {amp: 3, rate: 1.2, ...}
    ##| stop
    «p?» = rrand(-0.3, 0.3)
    a = 0.2
    sample samp, ("hh_analog«?»", "rimshot").choose, amp: a, cutoff: cmaster2«, ...?»
    sleep 0.25
  end
end

live_loop :sounds1, sync: :met1 do        # log: sample "...rimshot.wav", {amp: 0.9096, rate: 1.9...}
  ##| stop
  a = 3
  sample samp, "«?»", cutoff: cmaster2, amp: a, rate: 1.«?»
  sleep 0.25
end

live_loop :vox, sync: :met1 do            # the title vocal drop
  with_fx :slicer«?», phase: 0.25, mix: «?» do
    ##| stop
    a = 4.5
    vox = "~/Desktop/dj_dave/samples/idc/idc_vox_down.wav"
    sample vox, amp: a, cutoff: 130
    sleep 64
  end
end

# ---- chord section (16 bars of stacked 4.times blocks) ----
with_fx «:slicer?», «invert_wave: 1?», phase: 0.25«?», amp: 1, mix: 0.9 do
  live_loop «:chords?», sync: :met1 do
    ##| stop
    a = 0.7
    c = 130
    r = 0.25
    f = 0.6
    use_synth «:blade?»
    4.times do
      play «n1», amp: a, cutoff: c, sustain: s«?», release: f
      sleep 0.5
      play «n2», amp: a, cutoff: c, sustain: s«?», release: f
      sleep 0.5
    end
    4.times do
      play «n3», amp: a, cutoff: c, sustain: «?», release: f
      sleep 0.5
      play «n4», amp: a, cutoff: c, sustain: «?», release: f
      sleep 0.5
    end
    4.times do
      play «n5», amp: a, cutoff: c, sustain: «?», release: f
      sleep 0.5
      play «n6», amp: a, cutoff: c, sustain: «?», release: f
      sleep 0.5
    end
    4.times do
      play «n7», amp: a, cutoff: c, «?», release: f
      sleep 0.5
      play «n8», amp: a, cutoff: c, «?», release: f
      sleep 0.5
    end
  end
end

# ---- long pad / fall (rings out over 4-beat bars) ----
with_fx :reverb, room: 0.9«?» do
  live_loop «:synthfall?», sync: :met1 do
    with_fx :slicer, invert_wave: 1, phase: 1«?», wave: 1, mix: 0.8 do
      ##| stop
      a = 0.4
      c = 130
      s = 3.«?»
      use_synth «?»
      play «n1», amp: a, cutoff: c, sustain: 3.7
      sleep 4
      play «n2», amp: a, cutoff: c, sustain: 3.7
      sleep 4
      play «n3», amp: a, «?», sustain: 3.7
      sleep 4
      play «n4», amp: a, cutoff: c, sustain: 3.7
      sleep 4
    end
  end
end

# ---- lead/solo (random hard pan each round) ----
with_fx :reverb, mix: 0.6, room: 0.8 do
  live_loop :solo, sync: :met1 do         # log: synth :blade, {note: 62.4, release: 0.4923, cut...}
    use_synth :blade
    ##| stop
    a = 1.3
    r = 0.2
    c = 130
    p = [-0.9, 0.9].choose
    4.times do
      play «n1», release: r, cutoff: c, amp: a, pan: p
      sleep 0.25
    end
    2.times do
      play «n2», release: r, cutoff: c, amp: a, pan: p
      sleep 0.5
    end
    «3?».times do
      play «n3», release: r, cutoff: c, amp: a, pan: p
      sleep 0.25
    end
    4.times do
      play «n4», release: r, cutoff: c, amp: a, pan: p
      sleep 0.25
    end
  end
end

# ---- arp / wob (line-automated filter + pan) ----
with_fx «?», mix: 0.4 do
  live_loop :arp, sync: :met1 do          # log: synth :blade, {note: 77.0, amp: 0.9, cutoff: 1«?»}
    ##| stop
    c = (line 1«?»0, «?», steps: 120*2).mirror
    a = 0.9
    r = 0.2«?»
    p = (line -0.25, 0.25«?», steps: 120).mirror«.look?»
    «...» :minor_pentatonic«?»            # a scale reference is visible in side-wall frames
    play «?», amp: a, cutoff: c.look«, pan: p.look?»
    sleep «0.25?»
  end
end
```

Notes on fidelity:
- Loop thread names `:crshfade`, `:hhc`, `:sounds1`, `:solo`, `:arp`, `:met1` and
  the `tempo-change [130.0]` cue are read directly from the log/cue panes (sharp
  white-on-black text) and are reliable. Editor-side names marked `«?»` are not.
- All parameter values shown (`amp: 4.5`, `rate: 0.5`, `sleep 32`, `sustain: 3.7`,
  `p = [-0.9, 0.9].choose`, `steps: 120*2`, etc.) were legible in at least one
  1080p crop. Note names/chords were never legible — the log confirms `:blade`
  synth notes (77.0, ~62.4 MIDI) but not the progression.
- `(line …).mirror` + `.look` and `:minor_pentatonic` appear clearly in the
  side-wall projection frames (t72–t88) but their exact loop placement is partly
  inferred.
- The full kick `pattern "x---…"` gate string is visible as a long green string
  but individual x/- characters cannot be counted at this resolution.

## Build timeline

This is a performed *arrangement* of a pre-written file, not from-scratch typing:
the whole track's code is already on screen at 0:00, and the performance consists
of un/commenting `stop` lines to bring loops in and out, re-running with tweaked
params, and riding the DJ mixer. Timeline reconstructed from frames (no speech):

1. [0:00] Full file already projected; intro section playing — kick loop with
   `if pattern "x…"` gate, `:crshfade` slicer-chopped crash wash (`sleep 32`),
   off-beat Splice snare, hi-hat loop. Log streaming sample events; cue panel
   shows ~8 live_loop threads plus `tempo-change [130.0]`.
2. [0:08–0:35] Close shots: she alternates between typing/re-evaluating on the
   laptop (Sonic Pi visible: pink-highlighted code left, log pane right) and
   tweaking Pioneer mixer EQ/filter knobs — the mixer is a second instrument
   layered over the code.
3. [0:40–1:00] Wide venue shots; percussion layers building. Waveform visuals
   (LADYBAMBS) overlay the projected editor.
4. [1:04] Clear view of the file header: `IDC` ASCII banner, `use_bpm`, bare
   `:met1` metronome loop, `cmaster1`/`cmaster2` cutoff macros, the
   `define :pattern` helper, and sample-directory variables (`samp`, `bitsamp`).
   Cursor is parked near the kick loop's pattern string — she's gating drums.
5. [1:12–1:44] Side-wall shots show melodic machinery scrolling past:
   `sync: :met1`, `(line 0.25, 0.5, steps: 120*2).mirror`, `:minor_pentatonic`,
   `play …, cutoff: c.look`. She dances at the decks (the 1:37 `[Laughter]`
   caption) — energy peak of the first drop.
6. [1:52–2:08] Chord section fully visible and active: a big `with_fx` wrapper
   around stacked `4.times do play …; sleep 0.5 end` blocks (8-chord, 16-bar
   progression, shared `a`/`c`/`r`/`f` param variables), plus the reverb'd
   `use_synth :blade` loop below it being edited (cursor mid-block).
7. [2:16–2:32] Log shows the full melodic stack running simultaneously: `:arp`
   (blade, note 77), `:hhc` (analoghhc.wav, rate 1.2), `:solo` (blade, short
   release), `:sounds1` (rimshot.wav, rate 1.9) — densest section of the track.
8. [2:40] The title moment readable in full: `:vox` loop —
   `idc_vox_down.wav`, `amp: 4.5`, slicer fx, `sleep 64` — the "idc" vocal
   drop fired once per 64 beats. Below it the long-sustain fall pad
   (`sustain: 3.7`, `sleep 4`, reverb `room: 0.9`).
9. [2:48] Solo/outro section: `p = [-0.9, 0.9].choose` hard-pan lead and the
   `(line …).mirror` filter-swept `:arp` wob visible; she rides mixer filters.
10. [3:04–3:16] Close shots, track winds down (loops stopped in code + mixer
    fades — the exact teardown edits are not visible).
11. [3:20] Credits card; [3:28] EP part-picker menu with PART 03 "Bloom" queued.

## Techniques

- **Metronome loop as global clock** — an empty `live_loop :met1 do sleep 1 end`
  that every other loop declares `sync: :met1`. All phase relationships are
  guaranteed; re-evaluated loops rejoin on the beat. This is the backbone of
  DJ_Dave's set structure.
- **Step-gating with a pattern string** — her signature drum idiom:
  `define :pattern do |pattern| return pattern.ring.tick == "x" end`, then
  `sample …, … if pattern "x---x---…"` inside a `sleep 0.25` loop. An
  x/- string is a 16th-note step sequencer; editing the string live re-programs
  the drum. (Same helper appears across her sets.)
- **`stop` lines as a mixing desk** — every loop body starts with a
  commented-out `stop` (`##| stop`). Uncommenting it and re-running kills that
  loop at its next pass; commenting again brings it back. Arrangement =
  comment-toggling, not deleting code.
- **Global cutoff macros (`cmaster1`, `cmaster2`)** — top-of-file variables used
  as `cutoff:` on whole instrument groups (drums vs. percussion). One number
  edit + re-run = a filter sweep across a bus, like channel EQ on a mixer.
- **Sample-library-as-variables** — directory paths (`samp`, `bitsamp`, Splice
  pack paths) bound to short names at the top; loops then say
  `sample samp, "crshfade"` / `sample samp, ("hh_analog", "rimshot").choose`.
  Named-string lookup into folders keeps performance code terse.
- **Long-cycle wash layers** — a crash/fade sample at `rate: 0.5` under
  `with_fx :slicer` with `sleep 32`, and the vocal drop with `sleep 64`: layers
  that fire once per 8/16 bars provide arrangement-scale motion while the
  16th-note loops churn.
- **Slicer as rhythmic glue** — `with_fx :slicer, invert_wave: 1, phase: 0.25,
  wave: 1, mix: 0.8` wrapped around pads, washes, and the vocal chops sustained
  material into the track's 16th/quarter grid — Sonic Pi's equivalent of
  sidechain pump/trance-gate.
- **Param variables at loop top** — `a = 0.7; c = 130; r = 0.25; f = 0.6` then
  every `play` uses `amp: a, cutoff: c, release: f…`. Live-tweak one number,
  re-run, and the whole section responds; also makes 8 chord lines readable.
- **`(line …).mirror` + `.look` as an LFO** — `c = (line 110, …, steps: 120*2).mirror`
  then `cutoff: c.look` inside a ticking loop: a triangle-wave automation lane
  built from a ring, giving synth loops continuous filter/pan motion with no fx.
- **Random-but-musical variation** — `("hh_analog", "rimshot").choose` for hat
  timbre, `rrand(-0.3, 0.3)` for humanized params, `p = [-0.9, 0.9].choose` to
  hard-pan each solo phrase left or right per round.
- **Chord section as unrolled blocks** — the progression is literal stacked
  `4.times do play chord1 … play chord2 … end` blocks rather than data-driven
  rings: verbose, but each block is a grabbable handle during performance.
- **Hybrid rig: code + DJ mixer** — Sonic Pi's output runs through a Pioneer
  mixer; frames repeatedly show her sweeping filter/EQ between edits. Transitions
  and the final fade are mixer moves, not code moves — code is the sequencer,
  hands are the dynamics.

## Vocabulary

- `use_bpm 130` — set global tempo; `sleep` units become beats at 130 BPM.
- `live_loop :name do … end` — a named, hot-swappable loop thread; re-evaluating
  the buffer replaces its body at the next iteration.
- `sync: :met1` — start/phase-lock this loop to the cue fired each pass of the
  `:met1` loop.
- `stop` — inside a live_loop, halts that loop (her mute switch, toggled via
  comments).
- `##|` — Sonic Pi block-comment prefix; `##| stop` is a disarmed mute.
- `sample <path-or-dir>, "name", amp:, rate:, cutoff:, finish:` — play a sample;
  with a directory + string, matches a file by name. `rate: 0.5` = half-speed/
  octave-down; `rate: 1.2`/`1.9` = sped-up percussion. `finish: 0.4` plays the
  first 40% (seen in the log for `shake.wav`).
- `synth`/`use_synth :blade` — her melodic voice of choice in this track (soft
  PWM-ish lead); set once per loop, all `play`s use it.
- `play note, amp:, cutoff:, sustain:, release:, pan:` — trigger a synth note.
- `with_fx :slicer, phase:, wave:, invert_wave:, mix:, smooth:` — amplitude
  slicer/gate: `phase:` = slice period in beats, `wave: 1` = square chop,
  `invert_wave: 1` flips the gate, `mix:` = wet/dry.
- `with_fx :reverb, room:, mix:` — reverb wrapper (`room: 0.8–0.9` = long hall).
- `define :name do |args| … end` — define a helper function (her `pattern` gate).
- `.ring` / `.tick` / `.look` — turn a list into a cyclic ring; `tick` advances
  and reads per loop pass, `look` re-reads the current position without
  advancing (used to read one automation lane from several places in a beat).
- `(line a, b, steps: n)` — a ring interpolating a→b in n steps; `.mirror`
  appends the reverse, making a triangle LFO ramp.
- `rrand(a, b)` — random float in range, per evaluation.
- `[x, y].choose` / `("a", "b").choose` — pick one element at random each pass.
- `n.times do … end` — repeat a phrase block n times inside one loop pass.
- `if pattern "x---…"` — her step-sequencer gate (see Techniques).
- cue/log panes — Sonic Pi's right-hand panes; the log line format
  `{run:, time:, thread: :live_loop_x}` plus a cue list of running loops is what
  the audience sees scrolling as "the track playing itself".
