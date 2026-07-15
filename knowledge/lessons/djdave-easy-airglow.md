---
source: https://www.youtube.com/watch?v=JiQHclg_648, https://www.youtube.com/watch?v=ure6OT0LwtM
creator: DJ_Dave
genre: electronic pop / melodic dance (live-coded)
software: Sonic Pi (Easy), Strudel (Airglow)
---

# DJ_Dave — "Easy" (Live Coded Video, 2021) + "Airglow" (Visualizer, 2025)

Two finished-track videos, four years apart, that bookend DJ_Dave's toolchain
evolution: **"Easy" is Sonic Pi** (Ruby `live_loop`s, sample paths on disk,
`define`d pattern helper) performed live in a warehouse with the editor + log
projected on the walls; **"Airglow" is Strudel** (labeled `$name:`-style
patterns, `pick`/`slider` performance macros, punchcard visuals) captured as a
screen-recording visualizer with liquid-metal graphics compositing over the
REPL. Neither video has narration ("Easy" is instrumental captions-only;
"Airglow"'s transcript is just the song lyric), so everything below is read
from frames.

## Easy (Live Coded Video) — Sonic Pi

### Code (fragments — full file not recoverable)

The video is a music-video-style shoot: the Sonic Pi editor, log pane, and cue
list are projector-mapped onto the walls and the artist, often out of focus,
warped by wall texture, or crossing through the beam. No single frame shows
the whole file, so the code below is stitched from partial close-ups and is
flagged per-fragment. What IS unambiguous: it's Sonic Pi (Ruby syntax,
`live_loop`/`sleep`/`sample`/`synth :saw`, log lines `{run: N, time: T,
thread: :live_loop_X}`).

```ruby
# Projected cue list / log names the running loops (verbatim from frames):
#   :live_loop_kick  :live_loop_hhc  :live_loop_hho  :live_loop_cowbell
#   :live_loop_met1  :live_loop_arpeggiator  :live_loop_sampleslicer
#   :live_loop_clap  :live_loop_fuzzvox  (+ vocal/chorus + crashfade loops)

# Pattern helper (t00016 + t00168, high confidence — her signature idiom):
define :pattern do |pattern|          # name of define not fully legible
  return pattern.ring.tick == "x"
end

# Kick loop (t00128 close-up + t00168/t00224 wide, high confidence):
live_loop :kick, sync: :met1 do       # loop name from cue list; sync from siblings
  ##| stop
  a = 3
  kick = "/Users/sarah/Desktop/dj_dave/samples/easy/kick.wav"
  sample kick, amp: a, cutoff: cmaster1 if pattern "x--x--x--x--..."  # exact x/- string illegible
  sleep 0.25
end

# Crashfade loop (t00168/t00224, medium confidence):
live_loop :crashfade, sync: :met1 do
  stop
  a = 0.5
  cf = "/Users/sarah/Desktop/dj_dave/samples/easy/crashfade.wav"
  sample cf, amp: a                   # args partly hidden
  sleep 32
end

# Closed-hat loop (t00168/t00224, medium confidence):
live_loop :hhc, sync: :met1 do
  ##| stop
  a = 2
  hhc = "/Users/sarah/Desktop/dj_dave/samples/easy/hhc.wav"
  sample hhc, amp: a, ...             # trailing args illegible (log shows lpf: 120)
  sleep 0.25
end

# Vocal / chorus arrangement loop (t00232, medium confidence):
live_loop :vox, sync: :met1 do        # loop name guessed
  stop
  a = 1.5                             # could be .5
  v1     = "/Users/sarah/Desktop/dj_dave/samples/easy/v1.wav"
  chorus = "/Users/sarah/Desktop/dj_dave/samples/easy/chorus2.wav"
  v2     = "/Users/sarah/Desktop/dj_dave/samples/easy/v2andchorus.wav"
  sample v1, amp: a
  sleep 32
  sample chorus, amp: a, start: 0.0015
  sleep 65                            # digits blurry
  sample v2, amp: a, start: 0.0003
  sleep 31                            # digits blurry
end

# Fuzz-vox one-shot loop (t00232, medium confidence):
live_loop :fuzzvox, sync: :met1 do    # name from log thread :live_loop_fuzzvox
  stop
  a = 1
  fuzz = "/Users/sarah/Desktop/dj_dave/samples/easy/..."  # filename cut off
  sample fuzz, amp: a
  sleep 16
end

# Sample slicer (t00232, the most interesting fragment — low/medium confidence):
with_fx :..., ... do                  # fx name illegible
  live_loop :sampleslicer, sync: :met1 do
    ##| stop
    c = 110
    a = (line 0, 1.4, steps: 64).mirror   # read as "[/ line 0, 1.4, steps: 64].mirror"
    s = [-0.5, 0.5].choose                # a speed/rate flip? assignment target blurry
    vox = "/Users/sarah/Desktop/dj_dave/samples/easy/..."   # path cut off
    tick = rand_i(32)
    slice_size = 0.125/2/2
    s = tick * slice_size                 # line read as "s = slice * slice_size"
    f = s + slice_size
    sample vox, start: s, finish: f, ...  # keyword args mostly hidden
    sleep 0.5
  end
end
```

Log-pane lines (verbatim, these ARE readable and confirm runtime params):

- `sample "~/Desktop/dj_dave/samples/easy/kick.wav", {amp: 3, lpf: 100}` (also seen `{amp: 2, lpf: 120}` earlier — she changes kick amp/lpf mid-set)
- `sample ".../easy/hho.wav", {amp: 0.85, lpf: 100}` and `hho2.wav, {amp: 2, ...}`
- `sample ".../easy/hhc.wav", {amp: 2, lpf: 120}`
- `sample ".../easy/cowbell.wav", {amp: ...}`
- `sample ".../easy/clap.wav", {amp: 1.5, lpf: 12x}`
- `synth :saw, {note: 94.0, amp: 0.6, release: 0.06}` / `{note: 91.0, ...}` / `{note: 78.0, amp: 0.6, release: 0.06}` from `:live_loop_arpeggiator` — a fast saw arpeggio, very short release
- sample paths reference `synth_sine_intro` / `synth_sine.wav`, `synthbass.wav` / `synthbass2.wav` / `v1_synthbass.wav`, `sub2.wav {amp: 0.9}`, `v1.wav`, `chorus2.wav`, `v2andchorus.wav`, `crashfade.wav`, `metl.wav`

### Timeline

1. [0:00–0:15] Cold open: blue macro shot of a cable, then the empty rig — table, MacBook, RGB keyboard, projector beams. Track fades in.
2. [0:16–0:40] First wide shots of the room: full Sonic Pi buffer projected across two walls, log scrolling on the right wall, cue list (`/live_loop/kick`, `/live_loop/hho`, `/live_loop/cowbell`, `/live_loop/hhc`, `/live_loop/sampleslicer`…) racing at bottom right. Code readable in patches: `cmaster1 if pattern "x--x--..."`, sample paths under `~/Desktop/dj_dave/samples/easy/`.
3. [0:40–1:00] Close-ups: sample-path lines (`.../samples/easy/synth_sine...`, `chorus2.wav`, `v2...wav`) projected over her shirt; hands on both the RGB keyboard and the MacBook — she performs standing, typing on the laptop.
4. [1:04] Zoomed log close-up: `{amp: 2, lpf: 120}` and `{amp: 0.85, lpf: ...}` sample calls — the projected log doubles as a live mix readout.
5. [1:20–2:00] Full-room shots through fog; log shows kick at `{amp: 3, lpf: 100}` and the `:live_loop_arpeggiator` saw notes streaming — the build section.
6. [2:08] Hard close-up of the kick loop source (the verbatim `a = 3 / kick = "/Users/sarah/..." / sample kick, amp: a, ... / sleep 0.25 / end` fragment above).
7. [2:16–2:40] `synth :saw` log lines dominate (arpeggio section); `clap.wav {amp: 1.5}` enters — drop/peak of the track.
8. [2:48–3:12] Wide + close alternation; left wall shows the whole buffer as a column of `live_loop`s (kick, crashfade, hhc…), right wall the log; `synced ...` messages visible — loops are being cued/re-synced live.
9. [3:44–3:52] Long buffer shots reveal the vocal-arrangement loop (v1 → chorus2 → v2andchorus with `sleep 32/65/31`) and the `with_fx`-wrapped sampleslicer loop with `rand_i(32)` slice math.
10. [3:56] End: track resolves, room shots fade.

### Techniques

- **`define`-d pattern gate** — drum hits written as x/- step strings: `sample kick, ... if pattern "x--x--..."`, with `define :pattern do |pattern| return pattern.ring.tick == "x" end`. One `sleep 0.25` loop + a string = a step sequencer. This is the Sonic Pi ancestor of Strudel mini-notation `struct("x ~ x ~")`.
- **`cmaster1` master-cutoff variable** — a shared variable (set near the top, `~120`) passed as `cutoff:` into many sample calls: one number to open/close the filter on the whole kit. Poor-coder's master filter macro.
- **Amp variable per loop (`a = 3`)** — every loop names its level `a` at the top, so the level is always the first thing at hand to live-edit; the log confirms she changes kick from amp 2 → 3 and lpf 120 → 100 mid-set.
- **Samples as absolute file paths in variables** — `kick = "/Users/sarah/Desktop/dj_dave/samples/easy/kick.wav"; sample kick, ...`. The track is stems + one-shots on disk; the code is the arrangement.
- **Long-`sleep` arrangement loops** — vocals arranged inside one loop with `sleep 32` / `sleep 65` between `sample` calls: the loop IS the song structure, letting whole verse/chorus stems fire on a timeline while drum loops tick at 0.25.
- **`stop` / `##| stop` as mute switches** — a `stop` (or commented `##| stop`) as first statement in a loop is the on/off switch; commenting/uncommenting it is how sections are brought in and out. (Same role as Strudel's `_$:` mute.)
- **`sync: :met1` metronome loop** — every loop syncs to a dedicated `met1` loop, so re-run loops always join on-grid.
- **Random sample slicer** — pick a random 32nd (`tick = rand_i(32)`), compute `start`/`finish` from a fixed `slice_size = 0.125/2/2`, fire it every `sleep 0.5`, wrapped in `with_fx`: a glitch/stutter texture from one vocal file, with a `(line 0, 1.4, steps: 64).mirror` ramp riding a parameter up and down over time.
- **The projected-editor stage** — the performance/production insight: editor + log + cue list ARE the light show. The log pane (every `sample`/`synth` call with its args) is the equivalent of a mixer readout for the audience; fog + projector turn scrolling text into scenography. Camera cuts to code close-ups on musical hits.

## Airglow (Visualizer) — Strudel

### Code

Screen capture of a Strudel REPL with `_punchcard()` bars rendering behind
chrome-liquid 3D blobs. Most of the buffer is readable across frames; the
reconstruction below is high-confidence except where flagged. Layer labels are
`airglow_VOX` / `airglow_CHOPS` / `airglow_NOTES` / `airglow_BASSLINE` /
`airglow_PAD` / `DRUMS`, and mute state (leading `_`) varies frame to frame —
shown here as of the fullest views (t00008–t00048).

```js
// Top of file (t00032/t00112, partial): a gain-pattern bank + two globals.
// PG's declaration line is never fully visible; its last row reads:
//   "{0.3 0.8!3 0.3 0.8!3 0.3 0.8!2 0.3 0.8!2 0.3 0.8}%16"
// ]
const beat = 0        // off / on  — she edits this to 3 mid-video
const energy = slider(400, 400, 3500)   // swept live: 400 → ~1767 → ~500

airglow_VOX: s("airglow:< - 0 1 1 - - 0 1 1 - ... >")   // tail of pattern cut off
// s("airglow:< 0 1 1 ~ ~ 0 1>")                        // her commented alt take
  .fit()
  .chop(128).cut(1).loopAt(16)
  // .rarely(x=>x.clip("0.5|1"))
  // .almostNever(x=>x.ply("4|2"))
  .lpf(slider(8000,300,8000))//.room(1)
  .postgain(pick(PG, beat)).gain(1)
  ._scope({width: 1200})

airglow_CHOPS: s("hw:4")
  .slice(16, "0|5|6|7|10".fast(4)).cut(1).ply("2").speed("[-1|1]".fast(4))
  .rarely(x=>x.clip("0.5|0"))
  .ply("2|1").rarely(x=>x.ply(4))
  .lpf(slider(8000,300,8000))//.room(1)
  .gain(2)
  .mask("{1!13 0!3}%4")
  ._scope({width: 1200})

const notesss = [
  "{f3 c4 ~}%2",
  "{a3 e4 ~}%2",
  "{d3 a3 ~ }%2",
  "{e3 b3 ~ }%2"
]

airglow_NOTES: note(pick("<0!8 1!8 2!8 3!8>", notesss)).fast(8)
  // .ply("<2 4>".slow(2))
  .sound("square")
  .transpose("[0]")//.sometimes(x=>x.transpose("[0, 12]"))
  .lpf(2000)
  // .crush(7)
  // .sometimes(x=>x.ply(1.5))
  .decay(0.5).rarely(x=>x.decay("[0.2|0.3|0.4]"))
  .lpf(energy)
  .room("[0.5|1]".fast(4))
  .postgain(pick(PG, beat))

airglow_BASSLINE: n(irand("<1!7 <8>>".fast(2)))          // irand arg partly occluded
  .scale("<?2 a2 d2 e2>:minor:pentatonic")               // first root illegible (f2/d2?)
  .sound("[gm_synth_bass_1, square]")
  .transpose("[0, -12]")
  // .struct("x")//.room(1)
  .struct("x*16").decay(0.3).hpf(200).room(0.5)
  .lpf(energy)
  .postgain(pick(PG, beat)).gain(0.7)

airglow_PAD: note("g1".slow(2).add("<2 6 6 4>")).s("swpad:1".slow(2))
  .scrub("0*8".add("<.1>"))
  .att("0")//.lpf(slider(1357.5,300, 5000))
  .lpf(energy)
  .postgain(pick(PG, beat)).gain(1).room(2)

DRUMS: stack(
  s("tech:5").postgain(5).pcurve(2)/*…*/.hpf(75).struct(pick(structures, beat)),  // mid-chain occluded; `structures` array never fully visible
  // s(" [~ cp]").bank("KorgDDM110").speed(…).rest?(2).postgain(…)…(3000),
  s("hh").struct("[x!3 ~!2 x!10 ~]").postgain(0.5)/*…*/.gain(0.6).jux(rev),      // struct string per t00040/t00120, digits uncertain
  s("~ hh").bank("RolandTR808").room(0.2).speed(0.75)/*…*/(1.25).room(sine.range(0.1, 0.4))/*…*/.clip(0.15),
  s("breaks165").gain(0.6).loopAt(1).chop(16).fit()/*…*/.postgain(pick(PG, beat)),
  s("psr:[2|12|24|25]".fast(4)).struct("x!7 ~ x!3 ~ x!3 ~"/*…*/).jux(rev).hpf(1000).postgain(pick(PG,
beat)).speed(0.5).gain(0.4)
)
// (several DRUMS rows flip between commented/uncommented across the video)

  ._punchcard().color("b…")     // punchcard visualizer, color arg cut off
// all(x ⇒ x.hpf(mous…          // commented global: hpf on mouse — tail cut off
```

Notes on fidelity:

- `PG` is inferred as the name of the gain-pattern array from `.postgain(pick(PG, beat))` used by every layer; the array's own declaration and all but its final `"{0.3 0.8!3 …}%16"` row are never on screen.
- `structures` (in the DRUMS kick row `struct(pick(structures, beat))`) is likewise referenced but never shown — same pick-by-`beat` design as PG.
- The label is spelled `aigrlow_VOX` in at least one frame (t00112) — either her typo or projector-warp misread; transcribed as `airglow_` throughout.
- Mid-chain segments of the DRUMS rows are consistently occluded by the 3D blob graphics; occlusions are marked `/*…*/`. Everything else in DRUMS matches across ≥2 frames.
- Slider values are live: `energy` reads 400 (t00032), ~1767 (t00072), 500 (t00112); the two `lpf(slider(8000,300,8000))` widgets sit at max in most frames.

### Timeline

1. [0:00] Opens on the full buffer: NOTES + BASSLINE visible, `notesss` array, punchcard bars already running. Lyric "Fazed to forget you" starts — the *song* is playing; the code view is the visualizer.
2. [0:08–0:16] Scroll to VOX + CHOPS. `_airglow_CHOPS` is muted (leading `_`); VOX pattern `"airglow:< - 0 1 1 - - 0 1 1 - …>"` is being edited (its commented predecessor `< 0 1 1 ~ ~ 0 1>` above it). Cursor visible.
3. [0:24] NOTES + BASSLINE + PAD in view; boxed widget chips around pattern strings (`[0]`, `square`, `minor:pentatonic`, `d2`) show active mini-notation values.
4. [0:32] Top of file: `const beat = 0 // off / on`, `const energy = slider(400,400,3500)` with mouse on the slider — the performance macros.
5. [0:40–0:48] DRUMS stack in view; most rows commented (`// s("~ hh")…`, `// s("breaks165")…`, `// s("psr:…")…`), `s("tech:5")` kick and `s("hh")` running — first-verse groove.
6. [0:56–1:04] CHOPS unmuted (`airglow_CHOPS:` now no underscore, its `_scope` wave drawn above); energy slider swept up past ~1767 — chorus 1 lift ("It's hard enough to feel the afterglow").
7. [1:52] `const beat = 3` — the pick-index macro flipped: every `.postgain(pick(PG, beat))` and the kick's `struct(pick(structures, beat))` jump to their 4th pattern simultaneously. Verse 2 arrangement change with a one-character edit.
8. [2:00–2:16] DRUMS rows now uncommented (TR808 hats with `room(sine.range(0.1,0.4))`, `breaks165` chopped loop, `psr` percussion with `jux(rev)`) — fullest groove of the song.
9. [2:24–2:56] Graphics take over (blobs fill frame, code occluded) through chorus 2; brief flashes show BASSLINE unmuted/active and PAD edits.
10. [3:12–3:44] Color scheme shifts (pink/orange/red as the punchcard density peaks) — bridge/final chorus; readable flashes show the same buffer, CHOPS `mask("{1!13 0!3}%4")` still gating.
11. [4:40–4:48] Back to the clean blue buffer, NOTES + BASSLINE fullest view (the verbatim block above); track outro, "Woo!" at 4:50.

### Techniques

- **`pick(ARRAY, beat)` as a one-integer arrangement macro** — every layer ends `.postgain(pick(PG, beat))`, and the kick's step pattern is `struct(pick(structures, beat))`; editing `const beat = 0` → `3` re-patterns gains AND drum structure across the whole set at once. Section changes become a single keystroke. (Her Intercell-era `arr()` idea distilled to stock Strudel.)
- **`energy` slider bussed to every filter** — `const energy = slider(400,400,3500)` feeds `.lpf(energy)` on NOTES, BASSLINE, and PAD: one on-screen slider is a master brightness/intensity fader for all melodic layers. Named macro > per-layer knobs.
- **Vocal stem as a patterned instrument** — the whole song vocal lives in a sample bank and is played as `s("airglow:< - 0 1 1 - … >").fit().chop(128).cut(1).loopAt(16)`: `fit()`+`loopAt` pin stems to the cycle grid, `chop(128)` makes them granular, `cut(1)` chokes overlaps, and the `< >` slot-sequence chooses which stem section plays per cycle. The visualizer video is the track *being arranged* this way.
- **Chopped-and-reversed vocal glitch layer** — CHOPS: `.slice(16, "0|5|6|7|10".fast(4)).ply("2").speed("[-1|1]".fast(4))` — random-choice slice indices, doubled hits, per-hit direction flips, then `.mask("{1!13 0!3}%4")` to gate the chaos into a 13-on/3-off window so it breathes.
- **`rarely`/`sometimes`/`almostNever` as controlled chaos** — humanization via probability combinators on decay (`.rarely(x=>x.decay("[0.2|0.3|0.4]"))`), clip, ply — the pattern stays deterministic-feeling but never static.
- **Melody = pick over a phrase bank** — `note(pick("<0!8 1!8 2!8 3!8>", notesss)).fast(8)`: four two-note cell patterns in an array, selected in 8-cycle blocks by a slot sequence. Writing the *sequence of phrases* rather than notes.
- **Random-walk bass quantized to a moving root** — `n(irand(…)).scale("<… a2 d2 e2>:minor:pentatonic")` with the scale root itself a `< >` sequence: the chord progression lives inside the scale string; `.sound("[gm_synth_bass_1, square]")` layers two synths in one pattern; `.transpose("[0, -12]")` doubles it an octave down.
- **Pad by scrubbing** — `note("g1".slow(2).add("<2 6 6 4>")).s("swpad:1").scrub("0*8".add("<.1>"))` — a sampled pad played through `scrub` (position-scanning the sample 8x per cycle with a slowly shifting offset), attack zeroed. Sample-as-wavetable movement.
- **Mute-by-underscore arrangement** — `_airglow_CHOPS:` → `airglow_CHOPS:` and comment-toggling DRUMS stack rows are the section switches, same grammar as her Intercell sets.
- **Comments as a mixing desk** — alternates and disabled processors (`// .crush(7)`, `// .sometimes(x=>x.ply(1.5))`, `//.room(1)`, commented drum rows, a commented `all(x => x.hpf(mouse…))`) are left inline: the buffer carries its own undo history and "what to try live" menu.
- **Production style** — the "visualizer" is the Strudel screen itself: `_punchcard()` bars + `_scope` waveforms as the graphic bed, hue-cycled per song section, with 3D chrome blobs composited on top. The code display doubles as the release artwork, exactly like the projected editor in "Easy" four years earlier.

## Vocabulary

Sonic Pi ("Easy"):

- `live_loop :name, sync: :met1 do … end` — a named, hot-swappable loop; `sync:` joins it to a metronome loop's cue grid.
- `sleep 0.25` — advance loop time (seconds at current BPM); the loop's step size.
- `sample path_or_var, amp:, cutoff:, lpf:, start:, finish:` — play a wav (absolute path string works); `start`/`finish` are 0–1 positions for slicing.
- `synth :saw, note:, amp:, release:` — built-in synth voice (her arpeggio: saw, release 0.06).
- `stop` / `##| stop` — halt this loop (first-line mute switch); `##|` is Sonic Pi's block-comment marker.
- `define :name do |arg| … end` — user function; her `pattern` helper gates events on x/- strings.
- `.ring.tick` — turn an array/string into a ring and read the next element each call — the step-sequencer cursor.
- `rand_i(32)` — random integer 0–31 (slice index).
- `(line 0, 1.4, steps: 64).mirror` — a stepped ramp up then back down (parameter LFO).
- `[-0.5, 0.5].choose` — random pick from a list.
- `with_fx :name do … end` — wrap loops in an FX bus.

Strudel ("Airglow") — beyond the switchangel-deep-acid vocabulary:

- `label:` / `_label:` — named pattern line; leading underscore mutes it (same as `$:`/`_$:`).
- `pick("<0!8 1!8 …>", array)` — index into an array of patterns with a pattern/number; her arrangement primitive (used with both a slot-sequence and a plain `const beat`).
- `const x = slider(v,min,max)` — bind a UI slider to a name so many chains can share one macro (`.lpf(energy)`).
- `s("bank:< - 0 1 1 …>")` — slot-sequence choosing which sample index of a bank plays per cycle (`-` = silence).
- `.fit()` — stretch a sample to fit its event duration.
- `.loopAt(16)` — loop a sample over N cycles at matching speed (stem playback).
- `.chop(128)` — granulate a sample into N sequential pieces.
- `.slice(16, "0|5|6|7|10")` — cut into N slices and play them by index pattern (`|` = random choice).
- `.cut(1)` — choke group: new hits cut the previous one's tail.
- `.ply("2|1")` — repeat each event N times.
- `.speed("[-1|1]")` — playback rate; negative = reversed (random flip per event).
- `.mask("{1!13 0!3}%4")` — binary gate pattern multiplied onto events (windowing chaos).
- `.rarely(fn)` / `.sometimes(fn)` / `.almostNever(fn)` — apply a transform with fixed probability.
- `.scrub("0*8".add("<.1>"))` — pattern the playhead position within a sample (wavetable-ish pad motion).
- `.att("0")` — amplitude attack time.
- `.postgain(x)` — gain after FX (her per-section level lane, always `pick(PG, beat)`).
- `.pcurve(2)` — pitch-envelope curve on the kick.
- `.jux(rev)` — run a reversed copy in the opposite stereo channel.
- `.bank("RolandTR808")` / `.bank("KorgDDM110")` — choose drum-machine sample banks.
- `sine.range(0.1, 0.4)` — continuous LFO mapped into a param range (`.room(...)` breathing).
- `irand(n)` — continuous random integers (bass note walk), here with a patterned argument.
- `.scale("<a2 d2 e2>:minor:pentatonic")` — scale quantization where the root is itself a sequence = chord progression in one string.
- `n("…")` vs `note("…")` — scale-degree numbers vs literal note names.
- `._punchcard()` — grid visualizer of pattern events (the video's main graphic).
- `all(x => x.hpf(…))` — apply a transform to every playing pattern (seen commented, mouse-mapped).
