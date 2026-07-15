---
source: https://www.youtube.com/watch?v=IqhKVEsSkls (Castles), https://www.youtube.com/watch?v=nXzTGiLcRL4 (Still Miss U)
creator: DJ_Dave
genre: live-coded electronic pop / dance
software: Sonic Pi (v3.3.1 visible on screen in Castles; fragments only in Still Miss U)
---

# DJ_Dave — Castles (Live Coded Visualizer) + Still Miss U (Live Coded Video)

Two produced *release videos* (not tutorials — zero narration; Still Miss U's
auto-captions catch only "[Music]", "right", "uh", "[Applause]"). Both put real
Sonic Pi code on screen, but as art direction, not screencast: Castles
datamoshes actual editor captures into the visuals; Still Miss U projects the
editor onto a school-hallway set. Code is therefore **partially recoverable for
Castles** (several frames show the genuine editor + log + cue panes) and
**fragments only for Still Miss U**.

## Castles (Live Coded Visualizer)

### Code (partial, with fidelity flags)

The visualizer alternates glitched live-venue footage with real Sonic Pi
screen captures (clearest at ~0:56, ~1:12, ~1:36). **Sonic Pi v3.3.1**, ten
buffer tabs `|0|…|9|`, editor left, scope + log + cue panes right. A magenta
bloom overlay washes out most fx names and opt keys, so `<?>` marks unreadable
tokens. Everything below is transcribed from frames t00056/t00064/t00072/t00096.

```ruby
# ~0:56 frame — arp / synth-stem / bass-stem section (buffer |0|)

with_fx <?>, <?>: 0.4 do
  live_loop <?> do
    ##| stop
    c = (line 80, 110, steps: <?>128*<?>).mirror        # cutoff ramp 80->110  [line args partly hidden]
    a = 0.6
    r = line(0.25, 0.5,  steps: <?>128*<?>).mirror.look # rate/param ramp      [key names hidden]
    p = line(-0.25, 0.25, steps: 128).mirror.look       # pan sweep L<->R
    use_synth <?>
    notes = (scale <?>, <?>).shuffle
    tick
    play notes.look, <?>: a, <?>: c.look, <?>: r, <?>: p
    sleep 0.25
  end
end

with_fx <?>, <?>: 0.3, <?>: 1 do
  live_loop <?> do
    with_fx <?>, <?>: 1, <?> do
      ##| stop
      a = 1.5
      c = 130
      synth = "/Users/sarahdavis/Desktop/dj_dave/samples/castles/synth.wav"
      sample synth, <?>: a, <?>: c
      sleep 16
    end
  end
end

live_loop <?> do
  ##| stop
  bass = "/Volumes/dave/DJ_DAVE/castles/bassbounce.wav"
  sample bass, <?>: 1.5
  sleep 16
end

with_fx <?>, <?>: 0.3, <?>: 1 do
  live_loop <?>, 13 do            # "13" flag partly legible — uncertain
    with_fx <?>, <?>: 1, <?>: 1, <?>: 1, <?>: 0.7, <?>: 0.2 do
      stop
      c = 130
      # ...clipped by frame edge
```

```ruby
# ~1:12 frame — chord/arp stab block (top of a buffer; note names hidden by overlay)
sleep <?>
play <?>, <?>: a,  <?>: c
play <?>, <?>: a2, <?>: c
sleep <?>
play <?>, <?>: a2, <?>: c
play <?>, <?>: a2, <?>: c
sleep <?>
play <?>, <?>: a2, <?>: c
play <?>, <?>: a2, <?>: c
sleep <?>
end
```

```ruby
# ~1:36 frame — stem-chop + random vox slicer loops
    sample vox, <?>, <?>: a
    sleep 32
  end
end

live_loop <?> do
  stop
  a = 2.5                                   # "2.5" partly legible
  chops = "/Volumes/dave/DJ_DAVE/castles/chops.wav"
  sample chops, <?>, <?>: a
  sleep 64
end

live_loop <?> do
  ##| stop
  am = 2
  c = 130
  a = "/Volumes/dave/DJ_DAVE/castles/vox7.wav"
  slice = rand_i(<?>)
  slice_size = <?>                          # value hidden by overlay
  s = slice * slice_size
  f = s + slice_size
  sample a, start: s, finish: f, <?>: am, cutoff: c
  sleep 0.5 #[0.5, 1].choose
  ##| end
end
```

**Log pane (verbatim — this is ground truth for opts the editor hides):**

```text
{run: 35, time: 201.9231, thread: :live_loop_hhc2}
 └ sample "~/Desktop/dj_dave/samples/kisses", "hhc3.wav", {amp: 1, lpf: 130}
{run: 35, time: 201.9231, thread: :live_loop_hho}
 └ sample "~/Desktop/dj_dave/samples/still miss u", "hho.wav", {amp: 1.5, lpf: 130}
{run: 51, time: 39.3417, thread: :live_loop_arp}
 └ synth :saw, {note: 67.0, amp: 0.6, cutoff: 100.1563, release: 0…}
{run: 35, time: 202.0385, thread: :live_loop_hhc}
 └ sample "~/Desktop/dj_dave/samples/kisses", "hhc2.wav", {rate: 0.6, amp: 1, lpf: 130}
{run: 46, time: 88.9983, thread: :live_loop_synth}
 └ sample "~/Desktop/dj_dave/samples/castles", "synth.wav", {amp: 1.5, lpf: 130}
{run: 51, time: 44.6494, thread: :live_loop_arp}
 └ synth :saw, {note: 63.0, amp: 0.6, cutoff: 94.7656, …}
```

**Cue pane** (live_loop names actually running): `hhc`, `hhc2`, `hho`, `kick`,
`clap`, `arp`, `vox`, `met1`, `crashfade`, plus the synth/bass stem loops.
A blurrier frame (~1:04) also shows the sample bank file list:
`…/kisses/zenhiser_kick.wav`, `kick2.wav`, `hhc1.wav`, `clap6.wav`,
`hhc2.wav`, `hhc3.wav`, `…/still miss u/hno.wav`, `…/kisses/build_fade.wav`,
`…/still miss u/crashfade…`.

Fidelity notes:
- The log confirms what the washed-out editor hides: her drum `sample` calls
  carry `{amp:, lpf: 130}` (lpf 130 = effectively wide open — likely a habit
  default), hats get `rate:` variation (0.6/0.7), and `:live_loop_arp` is
  `synth :saw` with the `cutoff:` riding ~94→100 — matching the
  `line(80,110).mirror` ramp in the editor.
- The arp's `notes` values (67.0, 63.0 in the log) confirm `play notes.look`
  feeds MIDI-note floats from a shuffled `scale`.
- Nothing here is a complete runnable program; treat it as an authentic
  skeleton + verified opts, not a full transcription.

### Timeline

1. [0:00–0:15] Blurry handheld club footage (crowd, DJ_Dave at her laptop under pink light). Title context only — no code.
2. [0:16–0:48] Footage progressively datamoshed: halftone/ASCII-dither shredding, a pixel-mosaic silhouette of her at the decks, liquid smears. Music builds.
3. [0:56] First clean Sonic Pi frame (code above): arp loop with `line(…).mirror` cutoff/pan automation + `synth.wav`/`bassbounce.wav` stem loops. Log shows runs 35–51 already ~200s in — this is a captured *performance*, not a from-scratch build.
4. [1:04] Editor mostly dissolved into the glitch, sample-bank file list and cue pane legible (kisses/still-miss-u/castles banks, Zenhiser kick).
5. [1:12] Chord-stab `play … a2 … c` block visible while code text itself melts into the visual (letters literally raining apart).
6. [1:20–1:28] Pure abstraction: halftone starburst, blown-out white/pink grids.
7. [1:36] Second clean editor frame: `chops.wav` stem loop + the random vox slicer (`rand_i` slice windows into `vox7.wav`), cue pane now shows `vox`, `met1`, `crashfade` firing — the arrangement has thickened.
8. [1:44–2:56] Finale is entirely visual: blue/white dot-matrix explosions, liquid chrome, her silhouette resolving in and out of the mosaic. No further code.
9. Throughout, glitch intensity tracks the arrangement's energy — the visualizer *is* the code screen being destroyed and reassembled in sync.

### Techniques

- **live_loop-per-instrument architecture** — separate named loops (`kick`, `clap`, `hhc`/`hhc2` closed hats, `hho` open hat, `arp`, `vox`, `synth`, `met1` metronome, `crashfade`) each with its own `sleep` grid; the cue pane doubles as a live mixer readout.
- **`line(...).mirror` + `.look` parameter LFOs** — `c = (line 80, 110, …).mirror` then `cutoff: c.look` = triangle-wave filter sweep; same idiom drives rate (`0.25→0.5`) and pan (`-0.25→0.25`). `tick`/`look` advance one step per loop pass. Log confirms the cutoff actually walking (94.7 → 100.1).
- **Shuffled-scale arp** — `notes = (scale <root>, <mode>).shuffle` then `play notes.look` on a `sleep 0.25` grid: a random-but-repeating 16th-note melody (same spirit as Strudel's `irand…rib` acid line in the Switch Angel lesson).
- **Hybrid stems + generative drums** — full bounced stems of her own production (`synth.wav`, `bassbounce.wav`, `chops.wav` triggered every 16/32/64 beats) layered under algorithmically patterned one-shot drums. This is the signature DJ_Dave workflow: the song's harmonic core is a DAW export; Sonic Pi does rhythm, texture, and arrangement.
- **Random vox resampler** — pick a random slice index, compute `start:`/`finish:` as fractions, replay every half beat: `slice = rand_i(n); s = slice*slice_size; f = s+slice_size; sample vox, start: s, finish: f`. Instant vocal-chop IDM out of one wav.
- **Commented-out `stop` as arrangement switch** — `##| stop` sits inside almost every loop; uncommenting kills that layer on its next pass. Cheap per-layer mute = how she sculpts sections live (same role as Strudel's `_$:`).
- **`sleep 0.5 #[0.5, 1].choose`** — a humanize option left commented in place: swap the literal for the `.choose` to randomize chop timing. Shows her habit of keeping performance variations parked in comments.
- **Cross-track sample reuse** — the Castles set pulls `hho.wav`/`crashfade` from her *still miss u* bank and hats/kick from a *kisses* bank (incl. a commercial Zenhiser kick), all under `~/Desktop/dj_dave/samples/<track>/` plus an external drive `/Volumes/dave/DJ_DAVE/<track>/` for big stems. A personal, per-song-organized sample library is part of the instrument.
- **lpf: 130 on drums** — a wide-open lowpass on every drum sample (130 ≈ 9.4 kHz+ in Sonic Pi's note-based cutoff scale); likely a template default she pulls *down* for filter moves.
- **Visualizer aesthetic** — the "visualizer" is the editor itself: screen recordings of the real performance datamoshed/halftoned in sync with the track. Code-as-set-dressing, destruction synced to energy.

## Still Miss U (Live Coded Video)

### Code: not recoverable — and why

This is a narrative music video, not a screencast. Shot in a dark school
hallway: title card ("DJ_DAVE — still miss u / live_coded/2021", pink
terminal-style lowercase), her performing on a MacBook on a small desk, Sonic
Pi projected onto the lockers/her hoodie, mirrored twin shots, and a final
walk-away down the locker corridor with a backpack. The code exists only as a
projector texture on non-flat surfaces at extreme angles — even the sharpest
frames yield fragments, not lines. The laptop screen (~0:32) shows the
unmistakable Sonic Pi layout (green/white code left, waveform strip right) but
is far too small to read.

Legible fragments (with timestamps), all consistent with the same Sonic Pi
idioms recovered from Castles:

- [0:24] `live_loop`, repeated sample-path walls: `"/Users/sarah/Desktop…`, `sample a,`, `amp:` (many), `e c,`, `d,`, and `:ubebass, sync: :me…` — almost certainly **`:subbass, sync: :met1`** (a bass loop synced to her metronome loop; `met1` is confirmed as a loop name in Castles' cue pane).
- [0:40] `live_lo…`, `a =`, `samp…`, `sleep`, `mi…`, and `cmaster2` (a with_fx or loop label — "master2" bus?).
- [0:48] Cue-pane projection: `loop/hhc` repeated, `/live_loop/hhc` — same hat-loop naming as Castles.
- [1:28] Log-pane projection: `"shaker.wav", {amp: 2, lpf: 13…}` and `{run: 45, time: 157.1538, thread: :live_loo…}` └ `sample "~/Desktop/dj_dave/samples/stil…"`, `"hho.wav", {amp: 3, pan: 0.3…}`; cue rows `/live_loop/met1`, `/live_loop/kick`, `/live_loop/hhc`. Also `….5].choose` and `b, c, d].choose, … am,` — i.e. `[a, b, c, d].choose`-style random selection from lettered variables.
- [1:44] Sample paths: `…amples/still miss u/leadvox.wa…`, `/still miss u/moonbass1_1.wav`, `/still miss u/moonbass1_2.wav`, `/still miss u/moonbass2_1.wav`, (a fourth `moonbass2_2.wav` row clipped).

So the *program* is lost, but the *parts list* survives: kick, hhc, hho,
shaker, met1 metronome, a synced `:subbass`, four `moonbass` stem variants,
`leadvox` + `vox1–vox4` chop sources (vox1–4 visible at 1:44/1:52 as
`…iss u/vox1.wav` … `vox4.wav`), and `.choose` randomization — the same
stems-plus-generative-drums architecture as Castles, one year earlier.

### Timeline

1. [0:00] Black. [0:08] Title card: pink highlight bar `DJ_DAVE — still miss u`, cursor line `live_coded/2021`.
2. [0:16] Her at a laptop in the dark, lit yellow/pink, code projection raking across her hoodie.
3. [0:24] Camera on the lockers: dense Sonic Pi buffer projected — sample-path walls, `live_loop`, `amp:` columns (fragments above).
4. [0:32–0:40] Over-shoulder shots: MacBook screen showing the real Sonic Pi session; projected `cmaster2` / `sleep` fragments on the wall behind.
5. [0:48] Wide: she sits mid-corridor, cue-pane (`/live_loop/hhc…`) projected around her — the room is inside the log output.
6. [0:56–1:20] Beauty shots: extreme-CU of projected glyphs (letters as pure texture), green scan-smear transition, her dancing, feet + cables on the floor.
7. [1:28] Clearest log projection: `shaker.wav {amp: 2…}`, run 45 at t≈157s — again, a real performance capture, projected.
8. [1:36] Mirrored twin composition, both selves at the laptop.
9. [1:44] Sample-bank projection: `leadvox`, `moonbass1_1/1_2/2_1…` on the lockers.
10. [1:52–2:24] She packs up; final shot walking away down the locker hallway wearing a backpack, giant glitch letters on the far wall. Video-as-song-credits.

### Techniques (what the video reveals despite unreadable code)

- **Confirmed early instance of her stem+loop system** — named per-drum live_loops (`kick`, `hhc`, `hho`, `shaker`, `met1`), a `sync:`'d subbass, multi-variant bounced bass stems (`moonbass1_1`…`moonbass2_2` = section A/B in two flavors), and dedicated vox chop files (`vox1–4`, `leadvox`). The two-videos-one-system picture: this is a stable personal architecture, not per-track improvisation.
- **`sync: :met1`** — she runs a dedicated metronome loop and `sync:`s melodic loops to it, keeping stem entrances phase-locked; `met1` appears in both videos' cue panes.
- **`[a, b, c, d].choose`** — random pick among pre-assigned variables (sample variants or note sets) per pass; her go-to variation device, seen commented in Castles (`#[0.5, 1].choose`) and live here.
- **amp/pan/lpf opts as the whole mix** — every visible log line is `{amp:…, lpf:…}` or `{amp:…, pan:…}`: mixing happens in sample opts, no fx-chain complexity on drums.
- **Performance-as-video aesthetic** — the "live coded video" treatment is projection mapping of the actual session (editor, log, cue pane) onto a physical set while she performs in it; the log/cue panes are treated as first-class visual material. For an AI DJ: rendering the *runtime telemetry* (what fired when) is itself the show.

## Vocabulary

Sonic Pi (Ruby-based) — complements the Strudel vocab in the Switch Angel lessons:

- `live_loop :name do … end` — a named, hot-swappable infinite loop; the unit of arrangement. Thread appears as `:live_loop_name` in the log, and each pass emits a `/live_loop/name` cue.
- `sync: :met1` — make a loop wait for another loop's cue before starting its pass; phase-locks layers to a metronome loop.
- `sample "path", opt: v, …` — play a wav (full path or bank dir + name); opts seen: `amp:`, `rate:` (0.6/0.7 = pitched-down hats), `lpf:` (cutoff as MIDI-style note number; 130 ≈ wide open), `pan:`, `start:`/`finish:` (0–1 fractional slice window), `cutoff:`.
- `synth :saw` / `use_synth` — choose the built-in synth; `play note, amp:, cutoff:, release:` then sounds it.
- `play notes.look, …` — play the current element of a ring without advancing it.
- `tick` / `.look` — advance the loop's tick counter / read at the current tick.
- `(scale root, mode)` — ring of scale notes; `.shuffle` randomizes order once (stable thereafter — a frozen random melody).
- `(line from, to, steps: n)` — ring interpolating from→to; `.mirror` appends the reverse (triangle LFO); indexed with `.look` per pass.
- `rand_i(n)` — random integer 0…n-1 (her slice picker).
- `[a, b].choose` — random element per evaluation (chop lengths, sample variants).
- `sleep t` — advance loop time by t beats; the rhythmic grid (0.25 = 16ths; 16/32/64 = stem re-trigger spans).
- `stop` / `##| stop` — kill the loop / Sonic Pi's comment syntax keeping a kill-switch parked one uncomment away.
- `with_fx :name, opt: v do … end` — wrap loops in an fx bus (names washed out in these captures; opts like 0.3/0.4/1 visible).
- Log pane / cue pane — right-side panels showing every triggered sound with resolved opts, and every loop-pass cue; her (and our) ground truth for what a performance actually played.
