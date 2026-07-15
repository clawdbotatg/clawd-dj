---
source: https://www.youtube.com/watch?v=MnmGjI8MmOE
creator: DJ_Dave
genre: live-coded dance pop (algorave)
software: strudel
---

# DJ_Dave — Live at Elsewhere (full ~48 min headline set, Brooklyn)

Her first-ever headline show (sold out, Elsewhere, NYC — stated on mic at 16:37).
This is a SET study: how a live coder structures a ~47-minute original-music set
for a paying club crowd — song order, energy arc, transition mechanics, stagecraft —
not a code transcription. Code was only legibly on camera twice (2:00, 2:40);
everything else is inferred from the room, the LED walls, and the mic.

**Framing quote (0:39):** "Before we really get into it, it's important that
everybody knows that every sound, every drum sequence, every instrument,
everything that you hear tonight is produced live with Code."

## Rig

- MacBook Pro on a plain white table, center stage. No controllers, no decks —
  keyboard only.
- A second angled display (tablet / portable monitor) to the left of the laptop,
  facing her — shows the same editor + pattern visuals; it reads as colored
  block-grids (pianoroll-ish) from the audience side all night.
- Small red USB audio interface on the table (Focusrite-red box; model
  unverified).
- Wired handheld vocal mic — she **sings live** over the coded backing on most
  songs, and uses the same mic for banter.
- Closed-back headphones (Audio-Technica-style), on/off constantly: on = building,
  off = performing/singing. A visible tell for what mode she's in.
- Venue LED video walls (3 panels behind stage) mirror the code/visuals; QSC K.8
  wedges; disco ball.
- Printed paper notes/setlist on the table (visible ~36:00) — she consults a
  sheet while building songs. Prepared set, live-typed execution.
- Software: **Strudel** — evidence: `note()` mini-notation, `.seg()`, `.clip()`,
  `.slice()`, `.decay()`, labeled patterns, `_`-prefix muting, and Strudel's
  signature boxed highlight around the currently-sounding event tokens (`c4`
  `a3` boxed in frame t00120/t00160). Custom fullscreen dark theme with huge
  font — the editor IS the stage visual.

## Set timeline

Songs are separated by on-mic talking; timestamps from transcript + frames.
Repeated "Heat / Heat up here" lines throughout the transcript are almost
certainly a recurring chopped-vocal sample mis-heard by the captioner (see the
`_chops` / `slice(16, …)` line in the code fragments), not lyrics — it appears
in nearly every song.

- **[0:00–1:04] Cold open in darkness.** Room lights fully down; the only light
  is the laptop screen and one strip on the back wall. Short hello ("How we
  doing Elsewhere?"), the "everything is produced live with Code" manifesto,
  then she starts typing. Pattern label on screen at 2:00: `hiii_elsewhere:` —
  she names the opener pattern for the venue.
- **[1:04–~9:30] Song 1 (opener).** Built from silence, layer by layer, in the
  dark: melody line first (`note("f3 c4 a3 e4 d3 a3 e3 b3")`), with a vocal-chop
  layer and a bass line staged MUTED (`_chops:`, `// bass:`) to be flipped on
  later. First vocal-chop section ~3:34. A "break it / break you" chop section
  ~5:00–5:42, and **the LED walls fire for the first time at ~5:40, at the
  drop** — the visual reveal is saved for the first climax, ~5.5 minutes in.
  Sung verse ~5:42–6:16 ("It's time to forget you… I hold up the mirror against
  you… I find ways to thrive").
- **[~9:30–11:50] Instrumental trough / rebuild.** No vocals, no captions;
  frames show her head-down typing, walls on soft white-block patterns. This is
  the transition-as-content zone: the old groove keeps running while she
  rewrites it into the next song.
- **[11:52–15:32] Song 2.** Chops return, then a sung song ("It's really hard
  for me to watch another person who makes mistakes… hope another time you will
  come around"). Green lighting era begins around here (walls/pods go green
  ~19:00 per frames; lighting color tracks song identity all night).
- **[16:37–17:11] SPEECH #1 (reset).** Music drops to a bed; she introduces
  herself, thanks the crowd, "my first ever headline show… you sold it out two
  weeks ago… it would not be right if this wasn't New York." Placed right after
  a song ends — the emotional beat doubles as a breather before the next build.
- **[17:32–~23:30] Song 3.** "Hey, hey, hey" chops at 17:32, headphones on at
  17:40 building over a quiet base (side screen shows a sparse dark pattern),
  long chop-driven groove with big crowd-motion peaks ~20:30–22:40. Walls:
  white/blue blocks, then pink/red by ~22:40.
- **[24:10–24:29] SPEECH #2 → "Cycles."** "This next song I wrote with my friend
  Switch Angel. And she's in the house right now." Song intro doubles as a
  shout-out; the groove is already ticking underneath.
- **[24:29–~28:45] Song 4: "Cycles" (w/ Switch Angel).** Sung ballad-leaning
  song ("Stuck, stuck, stuck, carried away… if you're falling, I'm falling with
  you"). She steps away from the laptop and fronts the stage to sing (~26:40
  frame: she's off the keyboard entirely — the code plays itself while she
  performs). Ends in chops ~28:35.
- **[29:07–30:26] BREAK: merch toss + crowd census.** Pants falling down because
  "I have like six mouse pads in my pants… I'm going to chuck them." Then: "How
  many of you — is this your first Algorave? Have you ever seen a live code show
  before?… Welcome to your first Algorave." A full comedic reset at the set's
  2/3 point, music still looping underneath.
- **[30:26–31:58] Narrated transition.** "Okay, I got to transition to the next
  song now, you know what I mean?" — she says the transition out loud, puts
  headphones on, and rebuilds **while the old loop plays** (31:00 frame: hands
  on keyboard, walls going red). "Do some people know this song?" [30:48] →
  "Beautiful" [31:00] as it lands.
- **[31:58–~36:30] Song 5: "World's Hardest Games."** Named on mic. Walls full
  red/pink — the strongest color-shift of the night marks the highest-energy
  song. Sung ("Together we're closer than we've ever been… will you love us?"),
  big "Let's go. Let's go." peak ~34:18, crowd loudest here (34:54 "Oh my god").
- **[36:39–37:19] SPEECH #3 (one-liner) → Song 6.** "This next song's like my
  favorite." + "If you've been here since this song, wow." Minimal talk this
  time — energy is high, so the reset is kept to seconds.
- **[37:19–~41:30] Song 6.** Sung ("I found you in heartbreak… when I'm with
  you, I'm concrete, baby… you're really hard to forget"). Walls back to
  white/blue blocks. She reads the paper notes at ~36:00 while prepping it.
- **[41:56–42:35] SPEECH #4 (finale setup).** "This next song is going to be my
  last of the night, but it is really long." + gratitude ("I've been going to
  this room to see other artists since I was 18… thank you for supporting live
  coding, and congrats on your first algorave.")
- **[42:53–47:00] Song 7 (finale).** At 42:53 she narrates a live edit: **"And I
  changed the color to blue"** — and the frames confirm the walls snap to deep
  blue at exactly this window. One long multi-phase closer ("Give me a small
  distance… who can break the walls…"), ends 47:00 with thanks and "I'll be in
  the courtyard after this." Crowd chants "DJ K" (captioner's hearing of
  "DJ Dave").

## Transition mechanics

- **Loop-carries-the-room:** the core move. A finished song's groove (or a
  reduced version of it) keeps cycling while she talks or rebuilds; the crowd
  never stands in silence mid-set. Every speech (16:37, 24:10, 29:07, 41:56)
  has music audibly running under it per the transcript's interleaved [music]
  tags.
- **Stage-muted, flip later:** patterns for the NEXT section are typed in
  advance but muted — both styles visible on screen: `_chops:` (underscore
  mute) and `// bass:` (comment mute). The transition itself is then just
  unmuting + re-eval, which is fast and safe in front of 300 people.
- **Rebuild-in-place:** for the 30:26 transition she doesn't clear the screen —
  she edits the running song into the next one over ~90 seconds, headphones on,
  narrating it ("I got to transition to the next song now"). Transition time is
  treated as performable content, not dead air.
- **Talk as a crossfade:** speeches are placed exactly where a DJ would put a
  breakdown — after peaks (post-Cycles merch toss), before the finale — so the
  energy dip is intentional and social rather than technical.
- **Visual color = song identity:** each song gets an LED-wall color scheme
  (dark/nothing → white-blue → green → red/pink for the peak song → deep blue
  finale), and it's live-coded — she narrates "and I changed the color to blue"
  mid-verse in the finale. Color change reads to the crowd as a track change.
- **Delayed visual reveal:** walls stay OFF for the first ~5.5 minutes; they
  ignite at the first drop. Saving the biggest visual for the first climax makes
  a typed build feel like an arrival.
- **Headphones as a state flag:** on = cueing/building the next thing, off =
  singing/performing this thing. The audience can literally see the "DJ is
  mixing" state.
- **Sung toplines over coded backing:** she fronts the stage with a wired mic
  and performs verses while the code self-plays, then returns to the keyboard
  between vocal sections — alternating musician-mode and coder-mode inside one
  song.

## Code fragments

Only two frames show readable code (both early in song 1, from the projected
screen). Everything is Strudel. Fidelity flags inline.

From t00120 (~2:00):

```js
hiii_elsewhere: note("f3 c4 a3 e4 d3 a3 e3 b3").decay(0.1   // right edge cut; "hiii" prefix inferred from t00160, left edge cut here
_chops: ("airglow:1").clip(1).slice(16, "14 [14|14!8|1      // right edge cut; a function name before ("airglow:1") — likely s(…) — may be cropped
ss: |                                                        // cursor mid-typing; almost certainly "bass:" (full line visible 40s later)
```

From t00160 (~2:40):

```js
const lpf = |                                                // being typed; value never visible
hiii_elsewhere: note("f3 c4 a3 e4 d3 a3 e3 b3").decay(0     // c4 and a3 are boxed = Strudel's active-event highlight, not syntax
// _chops: ("airglow:1").clip(1).slice(16, "14 [14|14!8    // now comment-muted (was _-muted 40s earlier)
// bass: note("f2 a2 e2 d2").seg(16).sound(synthbass).l    // right edge cut; ".l…" likely .lpf(…); synthbass is unquoted → a JS const she defined off-screen
```

Fidelity notes:
- Every line is truncated by the camera crop on at least one side; arguments
  after `.decay(0`, the full `slice` pattern, and the `const lpf` value were
  never on screen.
- `sound(synthbass)` unquoted and `const lpf =` imply a personal prelude of JS
  consts used as macros/presets — she types short names live and the constants
  carry the sound design. None of the const definitions were visible.
- `("airglow:1")` — a sliced sample (`airglow`, variant 1) chopped into 16
  pieces and re-sequenced by a mini-notation index pattern (`"14 [14|14!8|…"`):
  this is the vocal-chop engine that the captioner heard as "heat up here" all
  set. The function call the parens belong to is cropped; `s(…)` unverified.
- Pattern labels are plain `name:` form (`hiii_elsewhere:`, `chops:`, `bass:`),
  muted either by `_` prefix or `//` — both appear within 40 seconds of each
  other, so both are in her muscle memory.

## Techniques

- **Name the opener for the room** — the first pattern label is a greeting
  (`hiii_elsewhere:`) projected 20 feet tall; the code doubles as a marquee.
- **Manifesto before the first sound** — one sentence ("everything you hear
  tonight is produced live with Code") converts the laptop-on-a-table optics
  into the show's premise. Do this before playing a note.
- **Stage builds dark, reveal at the drop** — no wall visuals until the first
  climax (~5:40). The reveal is a transition tool as much as a light cue.
- **Pre-typed muted layers** — write the next section's patterns muted
  (`_name:` / `// name:`) during the current one; transitions become single
  unmute edits. This is the live-coding equivalent of beatmatching in the
  headphones.
- **Consts as sound presets** — `const lpf = …`, `sound(synthbass)`: sound
  design is frontloaded into JS constants so live typing stays terse and
  low-risk.
- **Sliced vocal chops as set glue** — one recognizable chopped vocal
  (`slice(16, …)` re-sequencing) recurs across multiple songs, tying original
  songs into one set identity.
- **Sing the topline, code the band** — alternate between keyboard (build) and
  handheld mic at the front of the stage (perform) within each song; the
  running patterns free her to be a frontwoman.
- **Narrate the mechanics** — "I got to transition to the next song now," "and
  I changed the color to blue": exposing the seams is charming in algorave
  culture and buys time for the edit. Transitions don't need to be hidden,
  they need to be OWNED.
- **Speech placement = energy management** — talk after peaks and before the
  finale; keep it to one line when energy is high (36:39), let it breathe when
  the crowd needs recovery (29:07 merch toss).
- **Color-per-song on the visuals** — live-coded wall color is the set's
  track-ID system; the crowd feels a "new song" when the room changes hue.
- **Announce the finale's length** — "my last song… but it is really long"
  reframes one long multi-phase closer as generosity, and licenses an extended
  final build.
- **Paper notes on the table** — even a fully live-typed set runs on a written
  plan; consult it openly between sections.

## Vocabulary

- `name:` — Strudel labeled pattern statement (`hiii_elsewhere:`, `chops:`,
  `bass:`); the label registers/replaces that voice on re-eval.
- `_name:` — underscore prefix mutes the labeled pattern in place.
- `// …` — comment-mute; same effect, survives as visible staged code.
- `note("f3 c4 a3 e4 …")` — mini-notation melody of note names, one event each
  per cycle step.
- `.decay(0.1)` — envelope decay (short = plucky).
- `.seg(16)` — sample a pattern/signal into 16 events per cycle (16th-note
  stepper).
- `.sound(x)` / `s(x)` — assign the synth/sample; unquoted `x` = JS constant
  preset.
- `("airglow:1")` — sample name:variant reference (function cropped off-frame).
- `.clip(1)` — trim/fit each event's playback to its slot duration.
- `.slice(16, "14 [14|14!8|…")` — cut a sample into 16 slices and re-order them
  by an index pattern; `[a|b]` = random choice, `!8` = repeat 8×. The chop
  engine.
- `const lpf = …` — plain JS constant in the buffer; Strudel buffers are JS, so
  presets/macros are just variables.
- Boxed token (e.g. `c4` in a box) — Strudel's live highlight of the event
  currently sounding; a readability/performance feature, not syntax.
- "Algorave" — the scene term she uses on mic for a live-coded dance show
  ("welcome to your first Algorave").
