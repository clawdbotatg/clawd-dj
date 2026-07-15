---
source: https://www.youtube.com/watch?v=DnphhsOii7c
creator: DJ_Dave
genre: glitchy electronic / techno-pop with live sung vocals
software: Sonic Pi
---

# Intercell EP Live Coded: Part 04 - Bitrot

**What this video is (and is not):** unlike a screencast tutorial, this is an
audience-filmed live performance in a warehouse venue (part 4 of DJ_Dave
performing her *Intercell* EP live-coded, track "Bitrot", 6:51). There is no
narration — the transcript is entirely her sung lyrics ("in my subconsciousness",
"you always make the same mistakes", "I thought I waited out for you"). The code
is only ever visible as a wall projection behind her (mixed with generative VJ
visuals) and on her laptop screen from across the stage, so **the code itself is
mostly unreadable**. The value of this lesson is the software ID, the
performance-rig pattern, and the structural reads that *are* recoverable.

## Final code

**UNREADABLE — flagged.** No frame in the corpus shows the editor close enough
to transcribe a single full line verbatim; the projection is defocused,
keystone-warped, and overlaid with video-glitch VJ art. Below are the only
legible fragments (from zoom-enhanced crops), given as fragments, not as code:

```
# Fragments only — NOT a reconstruction. Positions/arguments lost.

live_loop …                       # multiple live_loop blocks fill 2+ editor columns
  play …
  sleep 0.5                       # sleep with small decimal args (0.5 / 0.7 shapes at t00088)
  … synth …                       # a synth reference near a loop head

"spheres1", …                     # green string sample names with numeric args (t00368)
"spheres2", …

# Sonic Pi log pane (right of projection, t00176–t00320) repeatedly shows
# 2–3-line entries in the standard format:
#   {run: NN, time: NNN.N, thread: :live_loop_…}
#    └─ sample "/Users/sarahdavis/Desktop/dj_dave/…", amp: …, …
# i.e. sample playback from a custom folder on her disk ("sarahdavis" =
# DJ_Dave's real name), with keyword args after the path.
```

Fidelity notes:
- Software identification is high-confidence; every fragment above is
  low-to-medium confidence on exact spelling and zero confidence on arguments.
- The buffer already contains a full screen of code in the first projection
  frame (t00008, ~0:08): this is a **prepared piece performed with live edits**,
  not a from-scratch build, so there was never a moment where short readable
  code was on screen.

## Software identification

**Sonic Pi**, from converging evidence:
- Projected editor shows Ruby-style `live_loop … do/end` block shapes with
  `play` / `sleep <float>` / `synth` keyword shapes (t00088 right wall).
- The white log block matches Sonic Pi's log pane format exactly: bracketed
  `run/time/thread` header lines with an indented `sample "…"` continuation
  (t00176–t00320), including a green absolute sample path
  `/Users/sarahdavis/Desktop/dj_dave/…` (t00128).
- Laptop screen (t00104, t00224) shows Sonic Pi's layout: dark editor left,
  scope waveform + log stacked on the right.
- A status-bar `Line: N  Position: N` readout at the projection's bottom left
  (t00200/t00240) matches Sonic Pi's editor status bar.
- DJ_Dave (Sarah Davis) is a well-documented Sonic Pi performer; this matches
  her whole catalog.

## Build timeline

(Frame times ≈ video seconds; no narration, so reads are visual/aural.)

1. [0:00] Wide venue shot, lights still up: warehouse space, audience seated on
   the floor, DJ_Dave center behind a table with laptop + Pioneer DJ mixer +
   CDJ, big projection wall behind her.
2. [0:08–0:24] Lights drop. Projection shows the full Sonic Pi mirror: a
   multi-column editor buffer **already full of live_loops**, log pane
   streaming, scope at top — the piece starts from a prepared scaffold.
3. [0:32] Close shot: she rides knobs on the Pioneer mixer (EQ/filter moves)
   while the code runs — hardware mixing layered over the code output.
4. [~1:00–2:13] First vocal section: she picks up the mic and sings live over
   the live-coded backing ("myself… in my subconsciousness… you always make the
   same mistakes"). Between vocal lines she returns to the laptop (t00104,
   ~1:44, typing).
5. [~2:08] Projection shows the Sonic Pi log scrolling `sample
   "/Users/sarahdavis/Desktop/dj_dave/…"` entries — the track is heavily built
   from her own sample library being triggered by loops.
6. [~2:32] Generative VJ visuals (glitch/organic textures) surge over the code
   projection — arrangement peak; code becomes fully unreadable.
7. [~2:56–3:20] Wide shots: editor + log + scope visible again; status bar
   shows cursor at buffer top (Line 2) — she's editing near the head of the
   buffer between sections. Music drops to a sparser section.
8. [~3:44–4:32] Alternating close shots of typing on the laptop and mixer
   moves; log keeps confirming loop-triggered samples (steady run numbers =
   loops re-evaluated live, not restarted).
9. [~4:56–5:13] Second vocal section ("I thought I waited out for you… every
   day"), mic in hand, other hand still on the rig.
10. [~5:44–6:08] Editing burst: `"spheres1"` / `"spheres2"` sample lines
    visible in the projected buffer — new texture layer named "spheres" enters.
11. [~6:32–6:51] Finale under red lighting: both hands on the Pioneer mixer,
    performing the outro with EQ/level rides rather than code edits.

## Techniques

- **Prepared-buffer performance (not from-scratch)** — the set opens with a
  full buffer of live_loops already written; performance = selective
  re-evaluation, small edits, mutes, and parameter changes. This is the other
  end of the live-coding spectrum from Switch Angel's from-scratch build: the
  code is a *score* she conducts.
- **Hybrid rig: code → DJ mixer** — Sonic Pi's output runs through a Pioneer
  DJM-style mixer, so macro dynamics (EQ kills, filter sweeps, level rides,
  transitions) are performed on hardware in real time while the code handles
  composition. Frees the hands from the keyboard at musical peaks — repeatedly
  visible at section climaxes and the finale.
- **Live vocals over live code** — she sings verses into a mic between edits;
  the live_loops keep time autonomously, which is exactly what makes a
  code-based backing band viable (nothing needs hands to keep playing).
- **Custom sample library as the sound source** — the log shows loop after loop
  triggering `sample "/Users/<her>/Desktop/dj_dave/…"` files: pre-produced,
  named one-shots/stems (e.g. `"spheres1"`, `"spheres2"`) sequenced by
  live_loops, rather than synth-only sound design on stage.
- **Numbered sample-name families** — `spheres1` / `spheres2` style naming:
  variations of a texture as numbered files so a loop can swap or alternate
  them with a one-character edit.
- **Screen mirror as stage design** — the full Sonic Pi window (editor + log +
  scope) is projected room-sized and *blended with generative VJ visuals* that
  swell at drops; the scrolling log doubles as proof-of-liveness for the
  audience.
- **live_loop as arrangement unit** — the buffer is organized as many parallel
  live_loops (visible as repeated block shapes in columns); sections change by
  editing/re-running individual loops, so the transport never stops.

## Vocabulary

(Sonic Pi terms observable or directly implied in this corpus; arguments were
not readable, so definitions are of the primitives, not her specific values.)

- `live_loop :name do … end` — Sonic Pi's core construct: a named, self-looping
  thread that survives re-evaluation; edit the body and re-run to mutate the
  music without stopping. The buffer is built almost entirely from these.
- `sample "…/path.wav", opt: val` — play an audio file; takes an absolute path
  for custom libraries (her `/Users/sarahdavis/Desktop/dj_dave/…` folder) plus
  keyword options (amp:, rate:, etc. — hers unreadable).
- `play` — trigger a note on the current synth.
- `synth` — select/trigger a named synthesizer.
- `sleep 0.5` — advance the loop's logical clock by half a beat; the sequencing
  primitive between events.
- Sonic Pi **log pane** — right-hand pane printing one `{run, time, thread}`
  header per event plus the triggered sample/synth line; on stage it reads as a
  live receipt of what the code just played.
- Sonic Pi **scope** — built-in oscilloscope view of master audio, visible top
  of her laptop screen and projection.
- **run number** — increments each time code is (re-)evaluated; steadily
  climbing run numbers in the log are the visible trace of live editing.
