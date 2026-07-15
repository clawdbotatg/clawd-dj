---
source: https://www.youtube.com/watch?v=8vGjGJpNX6M
creator: DJ_Dave
genre: live-coded electro-pop / dance (sung vocals over four-on-the-floor electronics)
software: sonic pi
---

# Intercell EP Live Coded: Part 01 - React

## What this corpus actually is (read first)

Unlike a screencast tutorial, this is a **filmed live performance** (4:22, cinematic
edit): DJ_Dave performs her track "React" in a warehouse, singing live into a mic,
with her Sonic Pi buffer projected onto the wall behind her. There is **no
narration** — `transcript.txt` is the auto-captioned *sung lyrics* of the track
("wish I didn't know that you didn't care", "but I keep coming back", "thought
that I wanted to"), which match lyric comments visible inside the code buffer.
The code is only readable where the camera gets close to the projection, so the
"Final code" below is a **partial reconstruction from overlapping projected
views** (frame crops, upscaled), not a keystroke-accurate transcript. Software is
unambiguous: `live_loop` / `with_fx` / `use_synth :tech_saws` / `##|` comments /
Sonic Pi's log pane (`{run: 1, time: 55.4549, thread: :live_loop_kick}` …
`bd_haus.flac` resolved from `/Applications/Sonic Pi*.app/Contents/…`) — **Sonic Pi**
(v3.x on a Mac, alongside a Pioneer DJ mixer she rides for live EQ/FX).

## Final code

Best-effort verbatim reconstruction; later frames win. `‹?›` marks characters I
could not resolve; whole-line uncertainty is flagged inline. Order follows the
buffer top-to-bottom as projected. The drum loops (`:kick`, `:clap`, `:shaker`)
**never appear in the projected region** — they exist only as log-pane evidence,
so they are reconstructed from the log, not the editor.

```ruby
##| (ASCII-art banner comment:)
##|  ██▀▄ ██▀ ▄▀▄ ▄▀▀ ▀█▀   -- "REACT"

use_bpm 11‹?›          # blue literal reads as 3 digits, ~110–118; exact value unreadable

live_loop :met‹?› do   # master metronome; every other loop syncs to :met1
  sleep 1
end

counter1 = 1‹?›        # blue ints; read as 12/13 in different frames
counter2 = 1‹?›

splice = "~/Splice/**"
samp   = "~/Desktop/dj_dave/samples/samples/**"
react  = "~/Music/Logic/copy2/**"          # var name partially blurred; 5–6 chars, reads "react"
smu    = "~/Desktop/dj_dave/samples/still miss u‹?›"   # "still miss u" clearly visible

define :pattern do |pattern|
  return pattern.ring.tick == "x"
end

##| live_loop :live‹?›, sync: :met1 do
##|   with_fx :slicer, invert_wave: 1, wave: 1, phase: 1, mix: 0.7, smooth: 0.1, sync: :met1 do
##|     with_fx :echo, phase: 0.5, mix: 0.‹?›, decay: 4 do
##|       live_audio :mac, amp: 2
##|       sleep 1
##|     end
##|   end
##| end

##| you told me I'd only see you in my dreams          <- full lyric sheet lives in the
##| can't believe that it's exactly how it seems          buffer as comments; she sings
##| I wore my heart out on my sleeve                      these live over the code
##| cause you ‹meant everything› to me
##| I let you drag me down so deep
##| how will you make it up to me?
##| wish I didn't know that you didn't care, but ‹?›
##| trying to dissuade this but ‹now?› I'm falling through
##| every inch I give you make sure you take two
##| but I keep coming back to you
##| I always thought that I wanted to
##| ‹live/loved› in my head cause it fell so ‹?›
##| I always thought that I wanted to
##| maybe I ‹never?› wanted you

# ---- drums: never on-camera in the editor; reconstructed from the log pane ----
# :live_loop_kick   -> sample built-in :bd_haus  {amp: 1.5, rate: 1, lp...}
# :live_loop_clap   -> sample "~/Splice/sounds/packs/Oliver Power Tool/
#                              OLIVER_snare_live_mixready_phat.wav"
# :live_loop_shaker -> sample "~/Dropbox/Mac/Desktop/dj_dave/samples/s.../shake.wav",
#                              {amp: 1.7, finish: 0.4, ...}

live_loop :hh‹?›, sync: :met1 do        # closed-hat loop; name unreadable (short, "hh…")
  ##| stop
  p = -0.7
  a = 0.5
  ##| 64.times do
  sleep 0.5
  sample samp, "hh‹?›_analog", pan: p, cutoff: ‹?›, amp: a, rate: 0.9
  sleep 0.5
  ##| end
  ##| sleep 32
end        # (an adjacent duplicate of the sleep/sample/sleep block, part-commented,
           #  is visible mid-performance — she A/Bs two hat densities by comment toggle)

with_fx :reverb, ‹mix/room args unreadable› do
  live_loop :vox‹?›, sync: :met1 do
    with_fx :slicer, invert_wave: ‹0/1›, phase: 0.25, wave: 1, smooth: 0, mix: 0.9 do
      with_fx :echo, phase: 2, mix: 0.7, decay: 8 do
        stop                                    # un-stopped when the vocal drop hits
        vox = "/Users/sarahd‹?›/Dropbox/Mac/Music/Logic/copy2/Sources/vox.wav"
        sleep 0.01
        sample react, "loud", amp: 1.25, cutoff: 130, finish: 0.3   # folder-var + "loud" filter;
        sleep 15.2                              # var read as react/vox‹?› — one long stem per 15.2 beats
      end
    end
  end
end

with_fx :reverb, mix: 0.75 do
  live_loop :synthlea‹?›, sync: :met1 do        # reads "synthlead"
    ##| stop
    a  = 3.‹?›
    r  = 0
    c  = 50
    p  = 0.5
    at = 0.2
    use_synth :tech_saws
    play :‹e5?›, sustain: 0, cutoff: c, amp: a, attack: at
    sleep 4
    play :‹d5?›, sustain: 0, cutoff: c, amp: a, attack: at
    sleep 4
    play :‹g5?›, sustain: 0, cutoff: c, amp: a, attack: at
    sleep 4
    play :‹?›,   sustain: 0, cutoff: c, amp: a, attack: at
    sleep 4
  end
end

# a second tech_saws melody loop (the verse hook) — nested reverb+echo:
with_fx :reverb, mix: 0.5, room: 1, dam‹p?›: 0.5 do
  live_loop :sing‹?›, sync: :m‹et1› do          # name reads "sing…"; delay: arg clipped
    with_fx :echo, phase: 0.‹25?›, decay: 8 do
      stop
      c = 110
      a = 0.7
      r = 0.25
      p = 0.5
      use_synth :tech_saws
      sleep 4
      play :‹d5?›, cutoff: c, release: r, pan: p,    amp: a
      sleep 2
      play :‹b4?›, cutoff: c, release: r, pan: p*-1, amp: a
      sleep 2
      play :‹g4?›, cutoff: c, release: r, pan: 0,    amp: a
      sleep 4
      play :‹e5?›, cutoff: c, release: r, pan: p*-1, amp: a
      sleep 2
      play :‹a4?›, cutoff: c, release: r, pan: p,    amp: a
      sleep 2
      play :‹c5?›, cutoff: c, release: r, pan: p*-1, amp: a
      # (6 play/sleep pairs total visible; note names are the least certain tokens)
    end
  end
end

live_loop :arp‹?›, sync: :met1 do, delay: ‹?›   # 16th-note arp; "do," + delay arg as projected
  ##| stop
  a = 1.5
  c = 90
  r = 0.1
  notes = [:‹e5?›, :‹b4?›, :‹g4?›, :‹d5?›]      # 4-element list, exact notes unreadable
  tick
  use_synth :‹dsaw/…›                            # pink token unreadable
  64.times do
    play notes.look, release: r, amp: a, cutoff: c
    sleep 0.25
  end
end

# the "singular"/notes square-wave section (right-wall close-ups, 2:47–3:04,
# confirmed against the full-buffer views at 3:28/4:00):
use_random_seed 7
with_fx :echo, mix: (line 0, 0.1, ‹steps: ?›)‹…› do
  live_loop :‹notes2/singular›, sync: :met1 do
    stop
    c = (line 60, 110, steps: 120*2).mirror
    a = 0.2
    r = line(0.1, 0.2, steps: 120*2).mirror.look
    p = [-0.5, 0.5].choose        # an alternate line(-0.5, 0.5, steps: ‹?›).mirror.look
                                  # is visible overlapping in late frames
    use_synth :square
    notes = (scale :‹e2?›, :minor_pentatonic).shuffle
    tick
    play notes.look, amp: a, cutoff: c.look, release: r, pan: p
    sleep [0.25, 0.5].choose
  end
end

with_fx :bitcrusher, mix: 0.5 do
  live_loop :notes‹2?›, ‹and 5?›, sync: :met1 do   # middle token unreadable
    stop
    use_synth :‹square?›
    notes = (scale :‹e5?›, :minor_pentatonic).shuffle
    tick
    play notes.look, cutoff: 9‹0?›, release: 0.1, amp: 0.8
    sleep [0.25, 0.5].choose
  end
end

live_loop :bass‹?›, sync: :met1 do
  with_fx :slicer, invert_wave: 1, phase: 1, wave: 1, ‹smooth?›: 0.‹3?›, mix: 0.9 do
    stop
    a  = 3.5
    r  = 0
    c  = 100
    p  = 0.5
    at = 0
    use_synth :square
    play :‹e2?›, release: r, cutoff: c, amp: a, attack: at
    play :‹e3?›, release: r, cutoff: c, amp: a, attack: at   # octave doubling
    sleep 4
    play :‹?›,  ‹…›
    ‹further pairs unreadable›
  end
end

live_loop :crash, sync: :met1 do
  ##| stop
  ‹s?› = 13
  sample smu, "cr‹ash?›", ‹rate?›: 0.225, ‹amp?›: ‹?›, ‹?›.ch‹oose?›   # mostly unreadable
end
```

Fidelity notes:
- **Never fully on screen.** The buffer is taller than the projection; the kick /
  clap / shaker loops and anything above the `REACT` banner were never visible.
  Log-pane lines are verbatim where quoted (`bd_haus.flac`, `OLIVER_snare_live_
  mixready_phat.wav`, `shake.wav {amp: 1.7, finish: 0.4}`, `hh?_analog.wav
  {pan: -0.7, amp: 0.5}`, `synth :square {note: 52.0, amp: 0.2}`).
- Note names inside `play` calls are the least reliable tokens (small pink text on
  brick); treat every melody pitch as approximate. Structure (arg names, sleeps,
  fx nesting, variable blocks) is high-confidence — it's corroborated across 4+
  frames each.
- Thread names seen in the log: `:live_loop_kick`, `:live_loop_clap`,
  `:live_loop_shaker`, `:live_loop_singular`, `:live_loop_notes2`, plus the
  hat loop. Editor loop names are mostly clipped.
- The two `counter1/counter2` vars and `define :pattern` (an `"x"`-string step
  helper) are visible but their *call sites* are in the never-projected region.

## Build timeline

This is a performance of pre-written code, not a from-scratch build: **the whole
buffer exists at 0:00 and the set is played by un-stopping sections** (`stop` /
`##| stop` toggles) and re-running, plus live singing and hands-on mixer rides.

1. [0:00] Wide shot: full rig visible — left wall = Sonic Pi editor (REACT ASCII
   banner, metronome loop, sample-folder vars, `define :pattern`, lyric comments),
   right wall = Sonic Pi log + spectrum visual. Drums already pumping (kick/hat/
   shaker in the log).
2. [0:08–0:16] Buffer scrolled to the hat loop + vocal-sample loop; hat plays
   `samp, "hh…_analog", rate: 0.9` off the folder-glob var.
3. [0:24–0:43] Camera close on DJ_Dave: she picks up the mic; sung vocal enters
   ("I can't believe…" per captions). Right-wall close-up shows the tech_saws
   verse loop (`cutoff: 110/release/pan` block) and slicer/echo vocal fx chain.
4. [0:56] Full-buffer view: the `use_synth :tech_saws` phrase loop (play/sleep 4/
   sleep 2 ladder) and the 16th-note `64.times … notes.look` arp are running; the
   square `:singular` loop with its `(line 60, 110…).mirror` cutoff ramp is queued
   (`##| stop`).
5. [1:04] Visual flip to red/orange projection scene (VJ layer over the same code).
6. [1:36] Close view of the vocal one-shot loop: `vox.wav` path pasted in,
   `sample react, "loud", amp: 1.25, cutoff: 130, finish: 0.3`, `sleep 15.2` —
   the full sung stem fired as one long sample under her live vocal.
7. [2:00] Back on the REACT header view — verse 2, lyric comments on the wall
   line up with what she's singing ("wish I didn't know that you didn't care").
8. [2:33] Chorus ("but I keep coming back") — clap loop appears in the log
   (`OLIVER_snare…phat.wav`), arrangement at full density.
9. [2:47–3:04] Long close-up on the square-wave section: `use_random_seed 7`,
   echo `mix: (line 0, 0.1…)` automation, cutoff `(line 60, 110, steps: 120*2)
   .mirror`, `notes = (scale …, :minor_pentatonic).shuffle`, humanized
   `sleep [0.25, 0.5].choose` — the moving synth texture of the bridge.
10. [3:12–3:28] Full buffer again; `:crash` loop (sample from the `smu` = "still
    miss u" folder) and the bitcrusher notes loop visible; she rides the Pioneer
    mixer between edits.
11. [3:52–4:08] Final section: lead variant with `attack: 0.2` + square `:bass…`
    loop under `with_fx :slicer, invert_wave: 1` (sidechain-pump feel); kick/
    shaker/hat still firing in the log at t≈240s.
12. [4:16] Cut to "powered by SOUNDCLOUD" outro card.

## Techniques

- **Pre-written buffer as a performable score** — every loop ships with a `stop`
  (or `##| stop`) as its first statement; performing = commenting/uncommenting
  `stop` lines and re-evaluating. The arrangement is a sequence of un-mutes, the
  Sonic Pi equivalent of flipping channel mutes on a mixer.
- **Master metronome loop** — a bare `live_loop :met1 do; sleep 1; end` that does
  nothing but keep time; every other loop declares `sync: :met1`, so freshly
  un-stopped loops always re-enter on the beat.
- **Sample-library variables (folder globs + name filter)** — `samp =
  "~/Desktop/dj_dave/samples/samples/**"`, `splice = "~/Splice/**"`, then
  `sample samp, "hh…_analog"` / `sample react, "loud"` picks a file whose name
  matches the filter string. One-word swaps re-voice a whole loop mid-set.
- **Lyrics as comments** — the full lyric sheet lives in the buffer as `##|`
  comments; the projected editor doubles as her teleprompter and as crowd-facing
  visuals. Performance ergonomics, zero audio effect.
- **Live vocal + processed vocal stem together** — she sings live into the mic
  while a `sample …, "loud", finish: 0.3` one-shot of the recorded vocal fires
  every 15.2 beats through nested `slicer → echo` inside `reverb`; there's also a
  (commented) `live_audio :mac` block for running the live mic through the same
  slicer/echo chain.
- **Long-arc parameter automation with `line(…).mirror` + `tick/.look`** — e.g.
  `c = (line 60, 110, steps: 120*2).mirror` then `cutoff: c.look`: each loop pass
  advances one step of a 240-step cutoff sweep that rises then falls. Same trick
  on release (`r = line(0.1, 0.2, …).mirror.look`) and on an fx arg
  (`with_fx :echo, mix: (line 0, 0.1, …)`) — evolving texture with zero manual
  knob-riding.
- **Frozen randomness** — `use_random_seed 7` before the shuffled-scale loops, so
  "random" melodies repeat identically every run/performance (same idea as
  Strudel's `.rib`: pick a seed you like, pin it).
- **Shuffled-scale melody engine** — `notes = (scale :root, :minor_pentatonic)
  .shuffle; tick; play notes.look` with `sleep [0.25, 0.5].choose`: a melody
  generator with deterministic pitch order (seeded shuffle) but humanized rhythm.
- **Variables as macro knobs at loop top** — `a/c/r/p/at` (amp, cutoff, release,
  pan, attack) declared once and referenced by every `play` in the loop; one edit
  re-voices the whole phrase. `pan: p` vs `pan: p*-1` bounces call-and-response
  notes across the stereo field.
- **Hand-written phrase melodies** — the tech_saws leads are literal
  `play`/`sleep 4`/`sleep 2` ladders, not generators: the hooks that need to be
  *the song* are hardcoded; generators are reserved for texture.
- **Slicer as sidechain-pump** — `with_fx :slicer, invert_wave: 1, phase: 1,
  wave: 1, mix: 0.9` on the square bass chops it against the beat (inverted saw
  = duck-on-the-one), the Sonic Pi idiom for the pumping-bass feel.
- **`##|` A/B blocks** — duplicated hat blocks with one half commented: pre-baked
  pattern variations she can swap by moving the comment marker.
- **Hybrid rig** — Sonic Pi is the sequencer/synth, but output runs through a
  Pioneer DJ mixer she rides continuously (EQ/filter/fx as the "right hand" while
  the code is the "left").

## Vocabulary

- `use_bpm N` — set global tempo; all `sleep`s are in beats.
- `live_loop :name do … end` — a named, hot-swappable loop; re-running the buffer
  redefines it without stopping time.
- `sync: :met1` — start/phase-lock this loop to the metronome loop's cue.
- `stop` (inside a loop) — the loop runs but produces nothing: a code-level mute.
  `##|` is Sonic Pi's comment prefix; `##| stop` = unmuted.
- `with_fx :reverb / :echo / :slicer / :bitcrusher do … end` — wrap everything
  inside in an fx node; freely nestable (vocals: reverb ▸ slicer ▸ echo).
- `:slicer` args: `phase:` (chop rate, beats), `wave:` (LFO shape), `invert_wave:
  1` (flip the duck), `smooth:`, `mix:` — rhythmic gating/sidechain feel.
- `:echo` args: `phase:` (delay time), `decay:`, `mix:` (patternable with `line`).
- `use_synth :tech_saws` — thick detuned-saw lead synth (the track's melodic
  voice); `use_synth :square` — the bass/texture voice.
- `play :e5, cutoff:, release:, sustain:, attack:, pan:, amp:` — one synth note
  with per-note envelope/filter args.
- `sample <folder-glob-var>, "filter"` — play the file in the glob whose name
  matches the filter; args seen: `amp:, pan:, rate:, cutoff:, finish:` (play only
  the first fraction), `attack:`.
- `live_audio :mac` — pull a live audio input (her mic) into the fx graph.
- `sleep n` — advance loop time n beats; `sleep [0.25, 0.5].choose` = humanized.
- `tick` / `.look` — advance the loop's counter once per pass / read the current
  value without advancing (used on rings, `line`s, and note lists).
- `.ring` — make a list cycle infinitely; `pattern.ring.tick == "x"` = step
  sequencing from an `"x--x"`-style string (her `define :pattern` helper).
- `(line a, b, steps: n)` — a ring sweeping a→b in n steps; `.mirror` makes it
  sweep back; with `.look` it becomes a slow automation lane.
- `(scale :e2, :minor_pentatonic)` — note ring from a scale; `.shuffle` =
  deterministic reorder under the current random seed.
- `[x, y].choose` — random pick per pass (pan sides, sleep values).
- `use_random_seed 7` — pin the RNG so shuffles/chooses repeat identically.
- `define :name do |arg| … end` — plain Ruby helper functions inside the buffer.
- `64.times do … end` — bounded inner loop for one phrase-length burst of steps.
