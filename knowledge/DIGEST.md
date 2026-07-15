# DJ brain digest — the cheat sheet carried into every composition prompt

Distilled from `knowledge/lessons/` (11 studied builds) + `knowledge/patterns.md`
+ verified API research. Keep this tight: it rides along in every brain call.

## Hard rules (violations = silence or crash)

- **Always label patterns `$:` or `$name:`** — `all()`/the master fader only see
  labeled patterns. Mute a line by prefixing `_$:`.
- **Only these sounds exist** (whitelist — never invent names):
  - synths: `sawtooth square triangle pulse supersaw sbd white pink brown`
  - dirt-samples: `bd sd hh oh cp rim cr rd lt mt ht misc perc amencutup breaks165 breath east jvbass`
  - drum machines (need `samples('https://strudel.b-cdn.net/tidal-drum-machines.json')`
    first): `.bank("RolandTR808")`, `.bank("RolandTR909")`, `.bank("RolandTR707")` on `bd sd hh oh cp rim`
- `setcps(BPM/60/4)` — e.g. 140 techno, 120 house, 170 dnb, 90 hiphop.
- Numbers to `note()` need `.scale("c:minor")` or letter names (`"c2 eb2 g2"`).
- Keep one program = whole track: every layer its own `$:` line.

## Build recipes (from the studied DJs)

- **Switch Angel acid** (140): `$: s("sbd!4").duck("2:3:4").duckattack(.2).duckdepth(.8)`
  kick ducks melodic orbits; bass = `n(irand(10).sub(7).seg(16)).scale("c:minor").rib(46,1)`
  `.s("sawtooth").lpf(200).lpenv(<sweep 0-8>).lpq(12).distort("2.2:.3").orbit(2)`;
  rare stab `s("supersaw").detune(1).rel(5).beat(2,32).slow(2).fm("2").fmh(2.04).room(1).roomsize(6)`;
  riser `s("pulse").seg(16).dec(.1).fm(time).fmh(time)`.
- **Switch Angel trance/dnb**: trancegate a sustained supersaw; clone the bass
  chain, `.add(7)` + `.add("<5 4 0 <0 2>>")` = lead that follows; `.scrub(rand.seg(16).rib(46,2))`
  chops any sample into a tape loop; collapse drums to a pulse with `.rib(0,1/4)` for breaks.
- **Glossing house** (124): `.duck(5)` sidechain; offbeat hats `"[~ hh]*4"`;
  pad = stacked chord `.clip(1)` on its own orbit; degrees-not-notes bass:
  `set("<0 3 5 7>*8").as("n").scale("C1:minor").s("sawtooth").lpf(rand.range(400,900)).sometimesBy(.125, x=>x.ply("2"))`.
- **Aviara hard techno** (150): TWO kicks — `s("bd:3!4").bank("RolandTR808").shape(.6).hpf(80)`
  under a syncopated `s("<[sbd!3 [sbd sbd]] [sbd!2 [sbd sbd] sbd]>").lpf(742)`;
  noise hats `s("white!8").decay(.07).lpf(2000).sometimesBy(.3, x=>x.s("oh | hh"))`;
  perlin everything: `.lpf(perlin.range(200,1000).slow(4))`, `.velocity(perlin.range(.5,1.5))`;
  panned tom bus with shared `.delay(.3)`; euclid bass `note("e1(5,8)").s("supersaw").jux(rev)`.
- **DJ_Dave template**: const arrays of pattern strings selected by ONE integer via
  `pick()` — change one number, whole arrangement moves; sidechain as a *composed*
  postgain pattern (`"[.75 2.5]*4"`-ish, dip on kick, boost between); an `energy`
  value feeding `.lpenv` on several synths at once.

## Set-level craft (from DJ_Dave's 6-song GitHub Universe set + Cycles collab)

- A set = pre-written songs performed by *mutation*: keep whole-track programs
  ready, mix by muting/unmuting layers (`_$:`), swapping pattern variants
  (kick → kick2 → kick3 as commented alternates), and riding one or two
  master macros (a shared lpf "bus" value = her `cmaster`; an `energy` value
  feeding several `.lpenv`s at once).
- Hold ONE tempo across neighboring songs (her whole set ran 125) — tempo
  changes only at hard-cut moments.
- Two transition types, both legal: overlap-crossfade (new song's kick+bass in
  while old melodics fade) and hard cut on a phrase boundary. Strip the old
  track to its bones before bringing the new one in.
- One-integer arrangement: arrays of pattern variants selected by a single
  `pick(PG, beat)` index — change `beat`, the whole track moves sections.

## Arrangement moves (how the humans run a set)

- Layer in one element at a time, ~8-16 cycles apart. Start: kick alone or kick+bass.
- Breakdown: mute the kick (`_$:`), let pads/riser carry 8 cycles, drop kick back.
- Riser into every drop: `s("pulse").seg(16).dec(.1).fm(time).fmh(time)` (kill after drop).
- Filter as transition: sweep a shared `.lpf` down before a swap, open after.
- Peak = maximum lpenv/lpq aggression; outro = strip to bass+kick, then bass alone.
- Silence is legal: a 1-cycle full stop before a drop hits hard.

## Sound-safety notes

- First trigger of any sample downloads it (lazy) — a brand-new sound may skip
  its first hit. Reuse sounds already heard in the set when possible, or accept it.
- `.gain` beats `.postgain` for balance; keep every layer .3-.9, kick loudest.
- `room/roomsize` on sparse elements only (washy on hats).
- Never `hush()`/`silence` as a whole program unless you mean total stop.
