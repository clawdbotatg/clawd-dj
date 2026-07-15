---
source: https://www.youtube.com/watch?v=E1K6Sv-oIb0
creator: DJ_Dave
genre: live-coded electro-pop / club (jersey club, house, electro)
software: strudel
---

# DJ_Dave — Hybrid Set for 808 on Twitch Week (~58 min, her biggest set video)

**What this is:** a four-song, ~58-minute continuous live set of DJ_Dave originals —
**Hello World (HW) → Heartbeat Pt. 2 (HB2) → Hard Refresh (HR) → Give It 2 Me (GI2M)** —
performed from ONE giant Strudel file. Every song lives in the file simultaneously as
named pattern blocks (`HW_*`, `HEARTBEAT2_*`, `HARD_REFRESH_*`, `GI2M_*`); the set is
performed by muting/unmuting blocks, toggling comment lines, sweeping sliders, and
editing two global consts. No transcript existed for this corpus (music only, no
narration) — everything below is read from the on-screen code across ~60 frames.

**The rig split ("hybrid"):** laptop running Strudel (all visible musical content) +
a Pioneer-style 2-deck DJ controller/mixer on the desk in front of her. Her hands are
on the laptop for most code moves and periodically on the mixer. Fidelity flag: audio
routing is not observable from frames — whether the controller plays stems under the
code or is used as mixer/FX for Strudel's output can't be confirmed. All song
structure visible in this video is code.

## The file architecture (this is the set's engine)

Header (verbatim, seen at [6:00] and [48:00]):

```js
samples('github:algorave-dave/samples')      // her own sample repo: hw, heartbeat2, silence, giveittome, swpad...
samples('github:switchangel/pad')            // Switch Angel's pad samples ("swpad")
samples('github:tidalcycles/dirt-samples')
samples('shabda/speech/en-US/f:hello,world,disko,kina')   // TTS vocal stabs

// DJ_DAVE  (ascii-art banner)

setCps(140/60/4)

// 140 - HW
// 130 - GI2M
// 150 - HR, HB2

const Structures = [
  "{~}",                                        // 0 - off
  "x*4",                                        // 1 - 4otF (four on the floor)
  "{x ~!6 x ~ ~ x ~!3 x ~}%16",                 // 2 - HR main
  "{x ~!3 x ~!3 x ~!2 x ~!2 x ~}%16",           // 3 - jersey club
  "{x ~!9 x ~!5 x ~ x ~!7 x ~!3 < ~ x > ~}%16"  // 4 - GI2M
]

const PG = [                                    // postgain (sidechain-ish pump) patterns, indexed by beat
  "{0.8}",
  "0.3 0.8".fast(4),
  "{0.3 0.8!6 0.3 0.8!2 0.3 0.8!3 0.3 1}",
  "{0.3 0.8!3 0.3 0.8!3 0.3 0.8!2 0.3 0.8!2 0.3 0.8}%16",
  "{0.4 1!9 0.4 1!5 0.4 1 0.4 1!7 0.4 1!3 <1 0.4> 1}%16"
]

const beat = 0
//0 - off
//1 - 4otF
//2 - HR main
//3 - jersey club
//4 - GI2M

const energy = slider(2276.8, 400,5000)
```

Three master controls drive the whole set:

1. **`const beat = N`** — one integer selects the kick structure (`struct(pick(Structures, beat))`
   on the kick) AND the pump/gain pattern (`postgain(pick(PG, beat))` sprinkled on
   nearly every melodic part). Changing one digit re-arranges the entire mix: kick
   pattern and the gain-ducking feel of every layer flip together. `beat = 0` = kick
   off + flat gain = instant breakdown.
2. **`const energy = slider(x, 400, 5000)`** — a global filter-cutoff macro; melodic
   parts carry `.lpf(energy)`. One on-screen slider opens/closes the brightness of the
   whole set — her version of the DJ's master filter knob.
3. **The DRUMS stack** — one shared `DRUMS: stack(...)` with a `tech:5` kick
   (structure-picked) plus a commented **bank of drum lines per song**: a
   `// HELLO_WORLD + HEARTBEAT2 + HARD_REFRESH` section (three songs share one drum
   kit: KorgDDM110 claps, RolandTR808 hats, breaks165, "psr" perc) and a separate
   `// GIVE_IT_2_ME` section (KorgDDM110+dmx rims, TR808 sh/hh). Transition = comment
   one set out, uncomment the other.

## Set timeline

- **[0:00] Hello World, already running** (set starts mid-groove, 140 BPM). Visible:
  `HW_NOTES` square-wave chord stabs picking from a `const notesss` chord bank,
  `.hpf(slider(1580,0,2000))` being ridden, `.lpf(energy)`, `.room("[0.5|1]".fast(4))`,
  `.postgain(pick(PG, beat))`.
- **[1:20] Vocal layers up:** `HW_MAIN_VOCALS: s("hw:2").chop(64).cut(1).loopAt(16)`
  with an lpf slider mid-sweep (3433 of 8000); `_HW_VERSE_CHOPS` (hw:1 sliced
  "1|2|4|5|9|10|11|12|13") sitting muted below. `HW_SPEECH` = TTS "disko kina"
  with `.echo(8,0.25,0.75)`.
- **[2:40–5:20] Verse/chorus alternation via filter, not drums:** `beat = 0` the whole
  time (no structured kick); `energy` ridden 2276 → 533 [4:00] → 2626 [5:20]. Tension
  is managed almost entirely with the global lpf macro.
- **[6:40] First kick drop:** `beat = 3` (**jersey club** structure) + `energy = 5000`
  (wide open). Peak of Hello World.
- **[8:00] Kick yanked:** `beat = 0`, energy stays 5000 — breakdown with bright synths.
- **[9:20] `beat = 1`** — four-on-the-floor kick in. A different drop feel from the
  same material, one digit later.
- **[10:20] Full drum kit:** the shared HW/HB2/HR drum lines all uncommented (claps,
  808 hats, breaks165 loop, psr perc). Punchcard visualizer running under the code.
- **[11:40] Transition begins (HW → HB2):** `energy` slammed to 400 (macro filter
  nearly closed). Below the still-playing HW blocks, `_HEARTBEAT2_MAIN` and
  `_HEARTBEAT2_CHOPS` are **already typed but muted** (underscore prefix) — she writes
  the next song ahead of time while the current one plays.
- **[12:20–13:20] HW dismantled line by line:** drum lines re-commented one at a time
  until only the offbeat `s("~ hh")` hat remains; HW vocal blocks muted. The set
  breathes through a near-empty bar.
- **[14:40] Heartbeat Pt. 2 in:** `HEARTBEAT2_CHOPS: s("heartbeat2:<0>").slow(2)`
  (sliced "2|3|4|5|6|7|9|13|14", `.chop(2).phaser(8)`) and `HEARTBEAT2_BASSLINE`
  active — the bassline block carries BOTH songs' note lines, one commented:
  `//note("f#2@16 a2@16 c#3@16 d3@16".slow(8)) // hard refresh` vs the active
  `note("g2@16 a#2@16 d3@16 d#3@16".slow(8)) // hb2`. (Tempo moves 140→150 for HB2
  per the header map; the actual setCps edit happened off-frame — inferred.)
- **[17:20] HB2 full groove:** the shared drum section fully uncommented again — the
  same drum kit legitimately serves HW, HB2, and HR, so drums never have to "transition."
- **[18:40] HB2 melodic layers:** `HEARTBEAT2_NOTES` (random square arp:
  `n(irand("7").slow(2)).struct("x*2")` in `<d5 g4>:minor:pentatonic`),
  `HEARTBEAT2_SPEECH` — TTS lyric via
  `samples('shabda/speech/en-US/f:I,can,hear,your,heart,when,youre,near')` →
  `s("<I can hear your heart when youre near>")`, and `HEARTBEAT2_PAD` on `swpad:1`
  (Switch Angel's pad bank).
- **[20:00] Mid-song breakdown:** `beat = 0`, `energy = 400`. Same two-const move as [11:40].
- **[21:20] Drop back:** HEARTBEAT2_MAIN lpf slider at 10000 (fully open).
- **[22:40–26:40] Long HB2 arc:** drums stripped to one hat [22:40], NOTES filter low
  (~670) while punchcard stays busy [24:00 area], full kit back [25:20], then MAIN
  vocal filter swept down to 769 while CHOPS slider sits at 9000 [26:40] — she
  constantly trades which layer is bright.
- **[30:40–32:40] Beatless interlude:** drums commented; `HEARTBEAT2_PAD` alone with
  lpf ~840 [31:40]; by [32:40] the file header shows the reset state `beat = 0`,
  `energy = 400`. The deepest valley of the set.
- **[33:40] Transition by mutation (HB2 → HR):** the HB2 arp block is **renamed
  `HR_NOTES`** and its scale swapped to the hard-refresh line
  (`"<c#5 f#4>:minor:pentatonic"` — previously sitting there as a comment). Meanwhile
  `HW_NOTES` reappears with `.transpose("<1 0 2 [5 <7 0> -2]>") //HARD REFRESH` —
  instruments from songs 1 and 2 are morphed into song 3's harmony instead of being
  rebuilt.
- **[34:40] Hard Refresh vocals:** `HARD_REFRESH_MAIN_VOCALS: s("silence:<1 0 ~ ~ 2>")`
  `.chop(128).cut(1).loopAt(16)` (vocals stored in a bank named "silence") and
  `_HARD_REFRESH_CHORUS_CHOPS: s("heartbeat:0")` — HR chorus chops are built from the
  *heartbeat* sample bank. `energy` climbing (722).
- **[38:40–40:00] HR verse/build:** vocals cycling `silence:<0>`/`<1>`, energy 400 →
  2667.
- **[41:20] HR peak:** shared drum section fully uncommented again; `beat` on the HR
  structure per the bank comment (//2 - HR main).
- **[44:20] HR post-chorus:** `HARD_REFRESH_POSTCHORUS_CHOPS: s("heartbeat:<1 0>")`
  `.striate("<4 8>").phaser(8).cut(1).clip(2)` + `HARD_REFRESH_BASSLINE` full melody:
  `note("f#3@8 c#3@3 d3@5 a3@8 c#3@3 d3@5 f#2@8 c#3@3 d3@5 d2@8 d3@3 c#3@5".slow(8))`
  on `"[square, sawtooth]"`.
- **[47:00] Transition with a typed message (HR → GI2M):** she types
  `time for a new song` / `// almost time for a new song` directly into the editor —
  the code doubles as chat. Shared drums ALL commented out, GI2M drum lines
  uncommented — a hard drum-kit cut, not an overlap.
- **[48:00] Live retempo:** `setCps(130/60/4)` — cursor visible mid-edit, 150 → 130.
  The one true "DJ tempo move" of the set, done as a text edit.
- **[48:20] Give It 2 Me:** `GI2M_REPEAT: s("giveittome:0")` with
  `.scrub("0@3 0.48!13".slow(2)).mul(speed(1)).rfade(30)`,
  `_GI2M_MAIN_VOX: note("c2").s("giveittome:1").chop(32).loopAt(8).fit()` with an
  extreme filter ride `.lpf(slider(0.266).mul(100).pow(2)).lpq(5)`, and
  `_GI2M_ARP: note("{d4 e4 g4}%16")` on `gm_pad_halo`. `energy = 5000`.
- **[51:00–53:40] GI2M layers:** `GI2M_MAIN_CHOPS` scrubbing
  `"{[0.49 ~]|3 0.187@1 0.97514}%4"`, `GI2M_PAD` (swpad:1 again,
  `.scrub("0*8".add("<.12>"))`), `GI2M_NOTES` (irand square arp in
  `e2:minor:pentatonic`, patterned `.decay("<0.1 0.1 0.2 0.3>")`), and `GI2M_BASS:`
  `note("e1!3 b1 f#1!1.5 g1!4 b1!0.5 d2!0.5 d1!0.5".slow(4))` on
  `s("square,supersaw,white:0:.1")` with `.lpf(slider(...).mul(100).pow(2)).lpenv(0)`
  and `.pitchwheel({circle: 1, hapRadius: 10})`.
- **[55:00] GI2M peak:** NOTES lpf ~3988 (open), punchcard saturated.
- **[56:20] Outro:** `// THANK YOU GUYS FOR JOINING!!!!` typed at the top of the file;
  final frames [57:40] show GI2M filters easing back down (~1739) as the set lands.

## Transition mechanics (the crown section)

Observable moves between songs, in the order she deploys them:

1. **Write-ahead muted blocks.** The next song's patterns are typed *while the current
   song plays*, prefixed `_` (muted): `_HEARTBEAT2_MAIN` exists a full minute+ before
   it sounds [11:40 → 14:40]. Transition readiness is a text state, not a cue point.
2. **Two-const valley.** Every major transition passes through `beat = 0` +
   `energy = 400`: kick structure off, global lpf closed. That's her "eject both EQs"
   move — one digit and one slider.
3. **Line-by-line drum teardown.** Drum stack lines are re-commented one at a time
   (clap line, then breaks, then perc), leaving a single offbeat hat as connective
   tissue [12:20–13:20]. The inverse — mass-uncomment — is the drop.
4. **Shared drum kit across songs.** HW, HB2, and HR deliberately use ONE drum
   section, so those transitions never need drum crossfades; only melodic/vocal blocks
   swap. Only GI2M (different tempo, different feel) gets its own kit, and that
   transition is a hard comment-swap cut [47:00].
5. **Comment-variant morphing.** Blocks carry both songs' parameters as adjacent
   lines, one commented: the bassline block holds `// hard refresh` and `// hb2` note
   lines; HEARTBEAT2_NOTES holds two `.scale(...)` lines tagged `//hard refresh` and
   `//hb2`. The transition is swapping which line is commented — instrument voice and
   pattern shape persist, harmony changes. She even renames the block
   (`HEARTBEAT2_NOTES` → `HR_NOTES`) once it changes owner [33:40].
6. **Cross-song sample reuse as glue.** HR's chorus and post-chorus chops are built
   from the *heartbeat* bank; HW_NOTES gets a `//HARD REFRESH` transpose line. Old
   song's timbres carry into the new song's harmony, so the ear hears continuity
   through the cut.
7. **Retempo as a text edit.** `setCps(150/60/4)` → `setCps(130/60/4)` typed live at
   [48:00], immediately after the drum-kit swap and during a low-energy valley —
   tempo changes are hidden inside breakdowns, exactly like a DJ pitch-riding through
   an ambient gap. A tempo map comment (`// 140 - HW, 130 - GI2M, 150 - HR, HB2`)
   sits at the top of the file as the set plan.
8. **Slider rides as the crossfader.** Every prominent part has its own
   `.lpf(slider(...))`; transitions trade brightness between outgoing and incoming
   layers (e.g. MAIN vocal swept down to 769 while CHOPS sits at 9000 [26:40]).
   Overlap transitions are filter-for-filter, not volume-for-volume.
9. **Typed audience messages.** `time for a new song`, `// THANK YOU GUYS FOR
   JOINING!!!!` — the editor is also the mic. Announcing the transition is part of
   the transition.

## Code fragments (verbatim, with fidelity flags)

The shared drum engine (assembled from [10:20]/[17:20] frames; widget chips like
`hh`/`RolandTR808` render boxed in the REPL but transcribe as strings):

```js
DRUMS: stack(
  s("tech:5").postgain(5).pcurve(2).pdec(1).hpf(75).struct(pick(Structures, beat)),

// HELLO_WORLD + HEARTBEAT2 + HARD_REFRESH
  s(" [~ cp]").bank("KorgDDM110").speed(1).fast(2).postgain(0.2).lpf(3000),
  s("hh").struct("[x!3 ~!2 x!10 ~]").postgain(0.5).bank("RolandTR808").speed(1.25).room(sine.range(0.1, 0.4)).gain(0.6).jux(rev),
  s("~ hh").bank("RolandTR808").room(0.2).speed(0.75).gain(0.5).fast(4),//.clip(0.15),
  s("breaks165").gain(0.6).loopAt(1).chop(16).fit().postgain(pick(PG, beat)),
  s("psr:[2|12|24|25]".fast(4)).struct("x!7 ~ x!3 ~ x!3 ~").jux(rev).hpf(1000).postgain(pick(PG, beat)).speed(0.5).gain(0.4)

// GIVE_IT_2_ME
  // s("{~ ~ rim ~ cp ~ rim cp ~!2 rim  ~ cp ~ < rim ~ >!2}%8").bank("[KorgDDM110, dmx]").speed(1.2).fast(2).postgain(0.25),
  // s("sh").struct("[x!3 ~!2 x!10 ~]").postgain(0.5).lpf(7000).bank("RolandTR808").speed(0.8).jux(rev).room(sine.range(0.1, 0.4)).gain(0.5),
  // s("hh").struct("x*16").postgain(0.5).bank("RolandTR808").speed(1).jux(rev).room(sine.range(0.1, 0.4)).gain(1),
  // s("~ hh").bank("RolandTR808").room(0.3).speed(0.75).gain(1.2),fast(4),
  // s("psr:[2|5|6|7|8|9|12|24|25]").fast(16).almostNever(ply("0")).gain(0.5).hpf(1000).postgain(pick(PG, beat))
)
._punchcard({width: 1400, height: 200})
```

Hello World blocks ([0:00]–[9:20] frames):

```js
HW_NOTES: note(pick("<0!8 1!8 2!8 3!8>", notesss)).fast(8)
  // .ply("<2 4>".slow(2))
  .sound("square")
  .transpose("[0]")//.sometimes(x=>x.transpose("[0, 12]"))
  .lpf(2000)
  // .crush(7)
  .decay(0.5).rarely(x=>x.decay("[0.2|0.3|0.4]"))
  .lpf(energy)
  .room("[0.5|1]".fast(4))
  .postgain(pick(PG, beat))
  ._punchcard({width: 1400})

const notesss = [
  "{f3 c4 ~}%2",
  "{a3 e4 ~}%2",
  "{d3 a3 ~ }%2",
  "{e3 b3 ~ }%2"
]

_HW_SPEECH:
  // s("<hello world>").begin("<0.18 0.1>")
  s("<disko kina>").begin("0.09")
  // .note("f1")
  .room(0.5)
  .postgain("<0.6 1>")
  // .fast(8).cut(1)
  .slow(2)
  .echo(8,0.25,0.75)

HW_MAIN_VOCALS: s("hw:2")
  .chop(64).cut(1).loopAt(16)
  // .ply(4)
  .slice(16, "14 [14!8|14|13]").cut(1)      // toggled in/out across the opening
  .lpf(slider(8000,300,8000))//.room(1)
  .gain(2.5)//.postgain(pick(PG, beat))
  // .crush(7)
  ._scope({width: 1400})

_HW_VERSE_CHOPS: s("hw:1")
  .slice(16, "1|2|4|5|9|10|11|12|13".fast(4)).struct("x")//.ply(2)
  .chop(8)
  .clip(0.5).ply(2)
  .cut(1)
  .lpf(slider(7000,300,7000))
  .room(1).rfade(30)
  .postgain(pick(PG, beat)).gain(3)
  ._scope({width: 1400})
```

Heartbeat Pt. 2 blocks ([12:00]–[28:00] frames; the two-song comment variants are the
point):

```js
_HEARTBEAT2_MAIN: s("heartbeat2:<0>")
  // .note("b1")
  .chop(64).cut(1).loopAt(16).hpf(500)
  .gain(0.5)
  .lpf(slider(10000,600,10000))
  .postgain(1.25)
  // .crush(7)
  ._scope({width: 1400})

_HEARTBEAT2_CHOPS: s("heartbeat2:<0>".slow(2))
  .slice(16, "2|3|4|5|6|7|9|13|14".fast(2)).struct("x")//.ply(2)
  .chop(2).phaser(8).clip(0.85).cut(1)
  // .ply(2)
  .room(0.75).hpf(500)
  // .crush(4)
  .gain(1.5)
  .lpf(slider(9000,300,9000))
  .postgain(pick(PG, beat))
  // .mask("<1 0>")
  ._scope({width: 1400})

_HEARTBEAT2_BASSLINE: //note("f#2@16 a2@16 c#3@16 d3@16".slow(8)) // hard refresh
  note("g2@16 a#2@16 d3@16 d#3@16".slow(8)) // hb2
  .struct("x*16").detune(4)
  .sound("[square, sawtooth]")
  .transpose("[-12, 0]")
  // .transpose("[-9, 3]")
  .coarse(2)//.release(0.1)
  .decay(0.25)
  .gain(0.5).hpf(130)
  // .lpf(mouseX.segment(4).range(350,2000))
  .lpf(energy)
  .postgain(pick(PG, beat))
  ._punchcard({width: 1400})

HEARTBEAT2_NOTES: n(irand("7").slow(2)).struct("x*2")
  // .scale("<c#5 f#4>:minor:pentatonic".slow(2)) //hard refresh
  .scale("<d5 g4>:minor:pentatonic".slow(2)) //hb2
  .ply("<2 4>".slow(2))
  .sound("square")
  // .transpose("[-12, 0]")
  .lpf(2000)
  .crush(7)
  .gain(0.75)
  .decay(0.1)
  .lpf(energy)
  .lpf(slider(670, 400, 4000))
  .room(1)
  .striate("2")
  .postgain(pick(PG, beat))
  .punchcard({width: 1400})

samples('shabda/speech/en-US/f:I,can,hear,your,heart,when,youre,near')
_HEARTBEAT2_SPEECH: s("<I can hear your heart when youre near>")
  // .note("f1")
  .gain(1)
  // .fast(8).cut(1)
  .begin("0.15").room(0.5)
  .echo(4,0.25,0.75)
  .punchcard({labels: true, fill: 1, fillActive: 1}).color("blue").theme("eclipse")

_HEARTBEAT2_PAD: note("<g1 c2@2 f1>".slow(2).add(4)).s("swpad:1".slow(2))
  // .almostNever(x=> x.transpose("0, 12, 24"))
  .scrub("0*8".add("<.12>"))
  .lpf(slider(840,400, 2000)).gain(1.5)
  .postgain(pick(PG, beat))
```

Hard Refresh blocks ([33:40]–[44:20] frames):

```js
HR_NOTES: n(irand("7").slow(2)).struct("x*2").scale("<c#5 f#4>:minor:pentatonic".slow(2)).ply("<2 4>".slow(2))
  // ...same chain as HEARTBEAT2_NOTES, renamed + rescaled at [33:40]

HW_NOTES: note(pick("<0!8 1!8 2!8 3!8>", notesss)).fast(8)
  .transpose("<1 0 2 [5 <7 0> -2]>") //HARD REFRESH      <- song-1 instrument, song-3 harmony
  ...

HARD_REFRESH_MAIN_VOCALS: s("silence:<1 0 ~ ~ 2>")
  .chop(128).cut(1).loopAt(16)
  .gain("0.7".slow(2))
  .lpf(slider(8000,600,8000))
  .postgain(pick(PG, beat))
  // .crush(7)
  ._scope({width: 1400})

_HARD_REFRESH_CHORUS_CHOPS: s("heartbeat:0".slow(2))
  .note("g#1")
  .slice(8, "<5 8>".fast(2))
  .chop(3).cut(1).loopAt(4)//.clip(0.25).ply(2)
  .gain("<0.6 1.6>".slow(2)).room(2)
  .lpf(slider(4000,600,4000))
  .postgain(pick(PG, beat))
  ._scope({width: 1400})
// fidelity: slice/chop args on this block were partially obscured by the punchcard overlay

_HARD_REFRESH_POSTCHORUS_CHOPS: s("heartbeat:<1 0>".slow(2))
  .striate("<4 8>".slow(2))
  // .chop(4)
  .note("a1")            // fidelity: note arg partly obscured, "a1" best read
  .phaser(8)
  .cut(1).clip(2)
  .lpf(slider(3671.2,600,5000))
  .postgain(1.5)
  .room(1)
  ._punchcard({width: 1400})

HARD_REFRESH_BASSLINE: note("f#3@8 c#3@3 d3@5 a3@8 c#3@3 d3@5 f#2@8 c#3@3 d3@5 d2@8 d3@3 c#3@5".slow(8))
  .struct("x*16").detune(4)
  .sound("[square, sawtooth]")
  .transpose("[-12, 0]")
  // .transpose("[-9, 3]")
  .coarse(2)//.release(0.1)
  .decay(0.25)
  .gain(0.5).hpf(130)
  // .lpf(mouseX.segment(4).range(350,2000))
  .lpf(energy)
  .postgain(pick(PG, beat))
  ._punchcard({width: 1400})
```

Give It 2 Me blocks ([48:20]–[57:40] frames):

```js
GI2M_REPEAT: s("giveittome:0")
  // .loopAt(0.25)
  // .note("g#1").slow(2)).room(0.5).rfade(30).scrub("0.1@3*2 0.48!13".slow(2)).mul(speed(1))
  .note("<c2 a#1>".slow(2)).room(0.5).rfade(30).scrub("0@3 0.48!13".slow(2)).mul(speed(1))
  .echo(4, 0.125, 0.25)
  .lpf(slider(7000, 300, 7000)).hpf(300)
  ._punchcard({width: 1400})

_GI2M_MAIN_VOX: note("c2").s("giveittome:1")
  .chop(32).loopAt(8).fit()
  .postgain(1.1)
  .lpf(slider(0.266).mul(100).pow(2)).lpq(5)      // slider drives cutoff as (100x)^2 — huge exponential sweep range
  // .mask("[1 0]".slow(2))
  // .echo(4, 0.25, .15)
  ._scope({width: 1400})

_GI2M_ARP: note("{d4 e4 g4}%16")
  .sound("gm_pad_halo").transpose("-12")
  // ... (chain continues off-frame)

_GI2M_PAD: note("g2".slow(2).add(4)).s("swpad:1".slow(2))
  .scrub("0*8".add("<.12>"))
  .att("0").lpf(1000).gain(1.25)
  .postgain(pick(PG, beat))
  ._scope({width: 1400})

_GI2M_NOTES: n(irand("<12@2 14 18>")).struct("[x]*16").scale("e2:minor:pentatonic")
  .sound("square")
  .decay("<0.1 0.1 0.2 0.3>")
  .decay("[0.1|0.2|0.3]".fast(8)).coarse(2)
  // .room(2)//.rfade(50)
  .lpf(slider(1998.3, 300, 4000))
  // .sometimes(mask(0))
  .gain(0.6)
  .postgain(pick(PG, beat))
  ._punchcard({width: 1400})

_GI2M_BASS: note("e1!3 b1 f#1!1.5 g1!4 b1!0.5 d2!0.5 d1!0.5".slow(4))
  .struct("{x ~!2 x ~!2 x ~!2 x ~!2 x ~!2 x ~!2 x ~!2 x ~!2 x ~!2 x ~}%16")
  .transpose("[0, 12]")
  .s("square,supersaw,white:0:.1")
  .release(0.5).decay(0.2)
  .postgain(1.25)
  .lpf(slider(0.55,0.2, 0.55).mul(100).pow(2)).lpenv(0)
  .pitchwheel({circle: 1, hapRadius: 10})
// fidelity: release/decay/postgain lines were partially highlighted/obscured; values best-effort
```

Standby macro rack (kept commented at the bottom of the file all set — global
performance FX she can flip on over everything):

```js
// all(x => x.room(mouseX.segment(4).range(0,2)))
// all(x => x.lpf(mouseX.segment(8).range(4000,200)))
// all(x => x.lpf(500))
// all(x => x.hpf(mouseX.segment(3).range(0,1000)))
// all(x => x.cut(2))
// all(x => x.crush(mouseX.segment(4).range(12,1)))

// .theme("<archBtw bluescreen>".fast(2))
// .theme("archBtw")
```

General fidelity notes: frames are 20s apart and the punchcard/scope visualizers
frequently overlay the text, so mid-typing states and a few argument values are
best-effort (flagged inline). Block mute-states (`_` prefixes) shown above are as
captured in the most legible frame of each era and toggle constantly during the set.

## Techniques

- **The set as a single file / "everything always loaded":** all four songs coexist as
  named blocks; performance = changing which are audible. There is no "loading the
  next track" — the whole setlist is RAM-resident text.
- **One-integer arrangement state (`beat`):** kick structure AND every layer's pump
  pattern index off the same const via `pick(Structures, beat)` / `pick(PG, beat)`.
  Editing one digit is simultaneously "change the drum pattern" and "change the groove
  feel of the whole mix." beat=0 is a built-in breakdown button.
- **Global energy macro:** `const energy = slider(400..5000)` feeding `.lpf(energy)` on
  multiple parts = master brightness fader. Verse/chorus contrast inside a song is
  often ONLY this slider ([2:40–5:20]).
- **PG pump patterns instead of sidechain:** rhythmic `postgain` patterns
  (`"0.3 0.8".fast(4)` etc.) fake sidechain ducking, and because they're indexed by
  `beat` the ducking style changes with the drum pattern.
- **Vocal science:** full vocal stems in her own sample bank, played three ways —
  `chop(64/128).cut(1).loopAt(16)` for the intact lead; `slice(16, "index|pattern")`
  for stutter chops; `scrub("0@3 0.48!13")` for turntablist repeats of one phrase.
  `.cut(1)` everywhere keeps overlapping chops monophonic.
- **TTS as an instrument:** `samples('shabda/speech/en-US/f:...')` renders lyrics
  ("I can hear your heart when youre near") and ad-libs ("disko kina") as sample
  banks, echoed and pitched like any other sound.
- **Songs share DNA on purpose:** one drum kit for three songs; HR chops built from
  heartbeat samples; song-1 chord stabs transposed into song-3 harmony. The catalogue
  is written to be mixable — set-craft starts at production time.
- **Exponential filter sliders:** `.lpf(slider(0.266).mul(100).pow(2))` — sliding
  0→1 maps to (100x)^2 Hz, giving DJ-filter-like resolution at the bottom and huge
  sweeps at the top.
- **Retempo in the valley:** tempo changes (140/150/130) are typed during beatless
  breakdowns; a tempo-map comment at the top of the file is the set plan.
- **Visualizers as stage design:** `_punchcard`/`_scope` on nearly every block — by
  peak sections the entire screen strobes with pattern blocks; she also keeps
  `.theme(...)` switchers on standby for editor-wide color drops.
- **Editor as mic:** typed messages ("time for a new song", "THANK YOU GUYS FOR
  JOINING!!!!") communicate with the audience inside the performance surface.

## Vocabulary

(Beyond the switchangel-deep-acid lesson's basics; Strudel unless noted.)

- `samples('github:user/repo')` — load a sample pack from GitHub; her own is
  `algorave-dave/samples` (banks: `hw`, `heartbeat`, `heartbeat2`, `silence`,
  `giveittome`, `tech`, `breaks165`, `psr`...).
- `samples('shabda/speech/en-US/f:word1,word2')` — text-to-speech sample generation
  (voice `f`); words become a bank playable as `s("<word1 word2>")`.
- `setCps(140/60/4)` — tempo; retyped live to retempo the set.
- `pick("<0!8 1!8>", array)` / `pick(PG, beat)` — index into a JS array of
  mini-notation strings with a pattern or const; her core "state machine" primitive.
- `const x = slider(v, min, max)` — a named on-screen slider usable across many blocks.
- `.struct("x!7 ~ x!3 ~")` — impose a rhythm structure on a stream; `{...}%16` =
  sixteen-step grid notation; `x!3` repeat, `~` rest.
- `.bank("RolandTR808")` — choose drum machine bank for generic hit names
  (`hh`, `cp`, `sh`, `rim`).
- `.chop(n)` — cut a sample into n grains played in sequence; `.loopAt(n)` — stretch
  sample over n cycles (tempo-locks stems); `.fit()` — squeeze sample to its event
  span; combo `chop(64).cut(1).loopAt(16)` = tempo-locked full stem playback.
- `.slice(16, "1|2|4|5")` — chop into 16 numbered slices and play by index pattern
  (the stutter-edit workhorse).
- `.scrub("0@3 0.48!13")` — playhead-position pattern; jump/repeat inside a sample
  (turntablism-as-text).
- `.striate(n)` — interleaved granular slicing (vs chop's sequential).
- `.cut(1)` — choke group: new events cut still-ringing ones.
- `.jux(rev)` — run a reversed copy in the opposite stereo channel.
- `.ply(n)` — subdivide each event into n repeats; `.almostNever(fn)` / `.rarely(fn)`
  / `.sometimes(fn)` — probabilistic modifiers.
- `.postgain(pattern)` — post-FX gain, patterned for pump; distinct from `.gain()`.
- `.pcurve(2).pdec(1)` — pitch-envelope curve/decay on the kick (808-style drop).
- `.coarse(2)` — sample-rate reduction; `.crush(7)` — bit crush.
- `.echo(8, 0.25, 0.75)` — n repeats, time, feedback.
- `.rfade(30)` — reverb fade/tail length.
- `.begin(0.09)` — start playback fraction into the sample.
- `.detune(4)` — detune stacked oscillator voices.
- `.mask("<1 0>")` — gate a pattern on/off per cycle.
- `note("g2@16 a#2@16".slow(8))` — `@n` = hold duration weighting; long chord tones.
- `n(irand(7)).scale("<d5 g4>:minor:pentatonic")` — random degrees quantized to a
  scale whose root alternates per cycle (`<d5 g4>`) — melodic movement for free.
- `s("square,supersaw,white:0:.1")` — comma = layered synth stack in one voice.
- `.pitchwheel({circle:1, hapRadius:10})` — pitch-circle visualizer.
- `._punchcard({width, height})` / `._scope()` — event-grid / oscilloscope inline
  visuals; `.theme("archBtw")` — editor color theme as a performance visual.
- `mouseX.segment(n).range(a,b)` — mouse position as a control signal (kept on
  standby in her `all(...)` macro rack).
- `all(x => x.lpf(500))` — apply a transform to every playing pattern at once — the
  global FX/kill rack.
- `_` prefix on a block label — mute; removing it is the drop. Her block naming
  convention `SONG_PART:` (`HW_MAIN_VOCALS`, `GI2M_BASS`) is what makes a 4-song file
  navigable at speed.
