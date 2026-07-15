---
source: https://www.youtube.com/watch?v=x012gyly4ok
creator: DJ_Dave
genre: experimental club / techno (live-coded)
software: Sonic Pi (v4.4 on Mac — version watermark visible in the projected UI)
---

# Intercell EP Live Coded: Part 05 - Array (live performance film)

**What this video is:** NOT a screen-capture tutorial. It's a 4:47 cinematic film of a
live warehouse show (ends on a "DAVE" logo card): DJ_Dave performs the track "Array"
from her Intercell EP in Sonic Pi, with the Sonic Pi editor + cue log projection-mapped
onto the venue walls behind/beside her. There is no speech and no transcript. All code
was read off wall projections filmed at a distance, so **verbatim capture of the full
buffer is impossible** — what follows is every fragment that could be verified, flagged
line-by-line. The code is clearly **pre-written before the show**; she performs by
evaluating, muting/unmuting, and editing it live (the status bar's `Line:/Position:`
readout changes between shots) plus riding a Pioneer DJ mixer and singing/talking into
a mic that is routed *into* Sonic Pi.

## Final code

Full verbatim transcription is NOT possible from this footage (projector on brick,
camera at distance, motion blur). Below is the verified structure. `⟨?⟩` = unreadable;
lines without a flag were read directly off a frame.

```ruby
# ---- top of buffer: green comment header (2 lines) — UNREADABLE ----

# Vocal FX chain wrapping her live mic (read at t8/t32 front wall + t176/t216 side wall):
live_loop ⟨?name⟩, sync: ⟨?:met1⟩ do            # flagged: loop name unreadable
  with_fx :rlpf, cutoff: ⟨?⟩ do                 # "rlpf, cutoff" partially readable at t8
    with_fx :slicer, ⟨?⟩, wave: 1, phase: 1, mix: 0.⟨?⟩ do   # slicer opts partially readable
      with_fx :echo, phase: 0.5, mix: 0.⟨?⟩, decay: ⟨?⟩ do
        live_audio :vox, amp: 0.⟨?⟩             # her live microphone as an input node
      end
    end
  end
end

# Crash/transition one-shot (t8, t176 — sample name "crashfade" verified):
live_loop :crashfade⟨?⟩, sync: ⟨?:met1⟩ do
  stop                                          # staged mute (verified `stop` under several loop heads)
  s = 1.⟨?⟩
  sample samp, "crashfade", amp: s⟨?…⟩
  sleep ⟨?⟩
end

# Manual random-slice chopper (t8/t24/t32 front wall, mid-buffer block):
with_fx :reverb, mix: 0.6⟨?…⟩ do                # "reverb, mix: 0.6" verified at t224
  live_loop ⟨?name⟩, sync: ⟨?:met1⟩ do
    ⟨?⟩
    slice = rand_i(⟨?16⟩)                       # "slice = rand_i(...)" readable
    slice_size = 0.125/2⟨?⟩                     # readable
    s = slice * slice_size                      # readable
    f = s + slice_size                          # readable (verbatim at t216)
    sample samp, "vox", start: ⟨?s⟩, finish: ⟨?f⟩⟨?…⟩   # "sample samp, \"vox\", start:" verbatim at t216
    sleep ⟨?⟩
  end
end

# One stem-player loop PER STEM — identical template, repeated down the buffer.
# Stem names verified across frames: "bassline", "voice", "toms", "try", "gang", "bubble".
live_loop :bubble, sync: :met1 do               # loop head verbatim at t216
  stop                                          # present on not-yet-active stems
  ⟨?⟩ = ⟨?⟩
  tick
  args = {num_slices: 16, slice: look⟨?…⟩       # verbatim at t216 ("16" is "64" on the "try" loop, t224)
  sample samp, "bubble", args, amp: ⟨?⟩
  # ⟨?⟩ status                                  # dim commented line, unreadable
  sleep sample_duration samp, "bubble"⟨?, args⟩ # "sleep sample_duration samp, \"<stem>\", args" pattern verified
end

# ...same template repeats for "bassline", "voice", "toms" (t56/t72),
# "try" (num_slices: 64, t224) and a sparse "gang" loop inside a with_fx
# wrapper that sleeps 32 (t72: `sample samp, "gang", ...` / `sleep 32`).

# bottom of buffer: one more loop head `..p :⟨?⟩start_action⟨?⟩, sync: ⟨?⟩` — UNREADABLE
```

Notes on fidelity:
- `samp` is never seen being assigned; from the `sample samp, "<name>", args` calls it is
  almost certainly a variable holding her stems folder path (Sonic Pi's
  `sample <dir>, <filter>` idiom). Flagged as inference.
- The right-hand projection panel is Sonic Pi's cue log (visible `{run: NN, time: …,
  thread: :live_loop_…}` lines and `sample "/…/Contents/Resources/…"` paths), not code.
- The Sonic Pi status bar ("Line: N  Position: N", a BPM box, "Sonic Pi v4.4 on Mac")
  is projected bottom-right and is how the software was identified.
- `:met1` appears as the `sync:` target on every readable loop head; the metronome loop
  itself (`live_loop :met1`) was never on camera.

## Build timeline

Times are frame timestamps (frames every 8s). This is a performance arc, not a
from-scratch build — the buffer is fully written at 0:08 and evolves by evaluation.

1. [0:00] Black. [0:08] First wide shot: full code wall already projected — editor
   (left), cue log + waveform strip (right), status bar with BPM box bottom-center,
   "Sonic Pi v4.4 on Mac" bottom-right. Audience seated on the floor of a bare-brick
   warehouse; she stands at a flight-cased rig (laptop + Pioneer mixer + CDJ).
2. [0:16] Lights fully down between sections — stage nearly dark, projection off.
3. [0:24–0:40] Projection back up; cue log scrolling hard (many loops firing). Status
   bar `Line:/Position:` values change between 0:08 and 0:24 — she is editing, not
   just listening.
4. [0:48–1:20] Camera closeups: typing on the laptop, then a hand on the mixer EQ/faders
   — she plays the Pioneer as much as the code (hybrid live-code + DJ-mixer set).
5. [1:04–1:44] Projected visuals shift from raw editor-on-black to heavy red/orange
   textured composites (code still legible through it) — a build section.
6. [2:08–2:40] She takes the handheld mic and sings/talks — this feeds `live_audio :vox`
   inside the slicer→echo chain (the vox FX block is the code on the side wall right at
   this point, t176). Visuals go green/psychedelic at the peak (2:24).
7. [2:56] Side wall shows the `crashfade` loop and the vox chain — transition tooling
   in play between sections.
8. [3:28–3:44] Head-down typing closeup, then the side wall shows the stem loops:
   `"try"` with `num_slices: 64`, the `reverb, mix: 0.6` wrapper, `loop :gang, sync: :met1`
   with `stop` — she's bringing vocal-chant stems in/out by deleting/re-adding `stop`.
9. [3:36 t216] Clearest code shot of the night: `f = s + slice_size` /
   `sample samp, "vox", start:` chopper and the full `:bubble` stem loop with
   `args = {num_slices: 16, slice: look…}`.
10. [4:00] She dances at the mixer, one hand on a knob — outro mix-down.
11. [4:08–4:32] Wide shots, visuals washing out to warm noise; crowd silhouettes.
12. [4:40] Cut to black; "DAVE" planet logo card ends the film.

## Techniques

- **Stem-array performance template (the core of this video):** the finished track is
  bounced into named stems ("bassline", "voice", "toms", "try", "gang", "bubble",
  "crashfade", "vox"), and the buffer holds one `live_loop` per stem with an identical
  body: `tick` → build an `args` hash → `sample samp, "<stem>", args` →
  `sleep sample_duration samp, "<stem>", args`. The song becomes a wall of uniform,
  independently-toggleable loops — a live-codable mixing desk.
- **`stop` as a staged mute:** not-yet-active stem loops have `stop` as their first
  line, so the loop exists and stays synced but plays nothing. Arrangement = delete
  `stop` (or add it back) and re-evaluate. This is her equivalent of Strudel's `_$:`
  mute prefix.
- **Slice-array stepping (`num_slices:`/`slice:` + `tick`/`look`) — the "Array" of the
  title:** `args = {num_slices: 16, slice: look}` makes each pass of the loop play the
  next 1/16th slice of the stem (`num_slices: 64` on the "try" stem for finer chops).
  Because `slice:` is driven by the tick counter, the stem is treated as an array being
  indexed — re-slicing a fixed recording into a mutating sequence.
- **Manual random chopper as a second slicing voice:** `slice = rand_i(n)`,
  `slice_size = 0.125/2`, `s = slice * slice_size`, `f = s + slice_size`,
  `sample samp, "vox", start: s, finish: f` — same idea, but with explicit arithmetic
  on `start:`/`finish:` and a random index instead of a sequential one. Sequential
  `slice:` = groove; random `start/finish` = glitch.
- **Everything syncs to one metronome cue:** every readable loop head is
  `sync: :met1`. One hidden metronome loop broadcasts the beat; every stem loop
  blocks on it, so re-evaluated or un-muted loops always re-enter phase-locked.
- **Perfect loop lengths via `sample_duration`:** sleeping
  `sample_duration samp, "<stem>", args` (passing the *same* args hash) makes the sleep
  exactly the (rate-adjusted) length of what just played — stems loop seamlessly without
  hand-computed beat counts.
- **`args` hash as a reusable performance object:** sample options live in a named hash
  built fresh each pass, so one edit (e.g. `num_slices:`) retunes both the `sample` call
  and the `sample_duration` sleep. Also keeps every stem loop textually identical —
  cheap to eyeball-diff on stage.
- **Live mic as a synth node:** `live_audio :vox` pulls her real microphone into Sonic Pi
  inside a nested FX chain — `with_fx :rlpf → with_fx :slicer (wave: 1, phase: 1) →
  with_fx :echo (phase: 0.5)` — so her voice arrives pre-gated to the grid and echoed.
  Singing at a live-coded techno show, processed by the same buffer as the track.
- **Dedicated transition one-shot:** a `crashfade` sample in its own muted loop with an
  `amp` variable — a pre-armed crash/fade gesture she can fire between sections instead
  of improvising a transition.
- **Sparse-event loop for chants:** the "gang" (gang-vocal) loop plays once then
  `sleep 32` — long-period punctuation rather than a per-bar loop, wrapped in
  `with_fx :reverb, mix: 0.6` for size.
- **Hybrid rig, projection as the show:** Sonic Pi runs the music; a Pioneer mixer/CDJ
  sits in the signal path for hands-on EQ/fader rides; the editor + cue log ARE the
  stage visuals, projection-mapped over the brick with generative textures composited
  in. The audience literally watches the cue log scroll.

## Vocabulary

- `live_loop :name, sync: :met1 do … end` — a named, hot-swappable loop that waits for
  the `:met1` cue before (re)starting, keeping every layer phase-locked.
- `sync: :met1` — block until the metronome loop cues; her global clock idiom.
- `stop` — as a loop's first line: keep the loop defined but silent (staged mute).
- `tick` / `look` — advance / read the loop's counter; `slice: look` = step through
  slices one per pass.
- `sample samp, "name", args` — play the sample in folder `samp` whose filename matches
  "name" (Sonic Pi's directory+filter idiom), with an options hash.
- `args = {num_slices: 16, slice: look}` — options hash: cut the sample into 16 equal
  slices and play slice number `look`.
- `num_slices:` / `slice:` — built-in sample slicing opts (16 for grooves, 64 for fine
  vocal chops on the "try" stem).
- `start:` / `finish:` — play a sub-window of a sample (0–1 normalized); used with
  manual `slice * slice_size` arithmetic for the random chopper.
- `rand_i(n)` — random integer; picks which slice the manual chopper plays.
- `sample_duration samp, "name", args` — exact playback length of that sample call;
  used as the `sleep` so stems loop seamlessly.
- `live_audio :vox` — treat a live audio input (her mic) as a playable node inside FX.
- `with_fx :slicer, wave: 1, phase: 1` — rhythmic gate on the mic (square-ish wave,
  1-beat period): entrains a free vocal to the grid.
- `with_fx :echo, phase: 0.5, decay: …` — half-beat echo on the vocal.
- `with_fx :rlpf, cutoff: …` — resonant low-pass, outermost shaper of the vocal chain.
- `with_fx :reverb, mix: 0.6` — space wrapper around the sparse gang-vocal loop.
- `amp:` — per-sample gain; parked in a variable (`s = 1.…`) on the crashfade for a
  rideable fade.
- `sleep 32` — long fixed sleep = sparse punctuation layer.
- Cue log — Sonic Pi's right-hand pane printing `{run:, time:, thread: :live_loop_…}`
  per event; projected as part of the show visuals.
