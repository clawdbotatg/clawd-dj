# Pattern repertoire — known-good, complete Strudel patterns

Collected 2026-07-15 from official Strudel featured tunes/workshop/recipes and
community repos. These are the DJ brain's starting repertoire: known-good code
to play verbatim, mutate, or transition between. Notes:

- Default tempo is 0.5 cps when no `setcps` appears; the `setcps` line is ground truth.
- `useRNG('legacy')` lines are part of the verbatim source (newer RNG changed
  randomness) — keep them.
- froos patterns are **CC BY-NC-SA 4.0** (non-commercial share-alike) — fine for
  a free event, attribute on screen.
- The old strudel.cc `?xxxx=` share-link DB is dead post-Codeberg-migration —
  don't scrape those.
- williamzujkowski/live-coding-music-mcp "genre examples" are AI-generated
  stubs — excluded on quality.

---

## 1. "acidic tooth" — acid techno · eddyflux · ~120 (setcps(1))
Source: strudel.cc/workshop/getting-started/ (featured)

```js
// "acidic tooth" @by eddyflux
// @version 1.0
  setcps(1)
  stack(
    note("[<g1 f1>/8](<3 5>,8)")
    .clip(perlin.range(.15,1.5))
    .release(.1)
    .s("sawtooth")
    .lpf(sine.range(400,800).slow(16))
    .lpq(cosine.range(6,14).slow(3))
    .lpenv(sine.mul(4).slow(4))
    .lpd(.2).lpa(.02)
    .ftype('24db')
    .rarely(add(note(12)))
    .room(.2).shape(.3).postgain(.5)
    .superimpose(x=>x.add(note(12)).delay(.5).bpf(1000))
    .gain("[.2 1@3]*2") // fake sidechain
    ,
    stack(
      s("bd*2").mask("<0@4 1@16>"),
      s("hh*8").gain(saw.mul(saw.fast(2))).clip(sine)
      .mask("<0@8 1@16>")
    ).bank('RolandTR909')
  )
```

## 2. "Flatrave" — rave/techno TR909 · Felix Roos (CC BY-NC-SA 4.0) · ~120–130
Source: strudel.cc/examples/ (tunes.mjs)

```js
// "Flatrave"
// @license CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
// @by Felix Roos

useRNG('legacy')

stack(
  s("bd*2,~ [cp,sd]").bank('RolandTR909'),

  s("hh:1*4").sometimes(fast("2"))
  .rarely(x=>x.speed(".5").delay(.5))
  .end(perlin.range(0.02,.05).slow(8))
  .bank('RolandTR909').room(.5)
  .gain("0.4,0.4(5,8,-1)"),

  note("<0 2 5 3>".scale('G1 minor')).struct("x(5,8,-1)")
  .s('sawtooth').decay(.1).sustain(0)
  .lpa(.1).lpenv(-4).lpf(800).lpq(8),

  note("<G4 A4 Bb4 A4>,Bb3,D3").struct("~ x*2").s('square').clip(1)
  .cutoff(sine.range(500,4000).slow(16)).resonance(10)
  .decay(sine.slow(15).range(.05,.2)).sustain(0)
  .room(.5).gain(.3).delay(.2).mask("<0 1@3>/8"),

  "0 5 3 2".sometimes(slow(2)).off(1/8,add(5)).scale('G4 minor').note()
  .decay(.05).sustain(0).delay(.2).degradeBy(.5).mask("<0 1>/16")
)
```

## 3. "coastline" — chill/deep-lofi house · eddyflux · ~90 (setcps(.75))
Source: strudel.cc/workshop/getting-started/ (flagship demo). Needs `github:eddyflux/crate`.

```js
// "coastline" @by eddyflux
// @version 1.0
samples('github:eddyflux/crate')
setcps(.75)
let chords = chord("<Bbm9 Fm9>/4").dict('ireal')
stack(
  stack( // DRUMS
    s("bd").struct("<[x*<1 2> [~@3 x]] x>"),
    s("~ [rim, sd:<2 3>]").room("<0 .2>"),
    n("[0 <1 3>]*<2!3 4>").s("hh"),
    s("rd:<1!3 2>*2").mask("<0 0 1 1>/16").gain(.5)
  ).bank('crate')
  .mask("<[0 1] 1 1 1>/16".early(.5))
  , // CHORDS
  chords.offset(-1).voicing().s("gm_epiano1:1")
  .phaser(4).room(.5)
  , // MELODY
  n("<0!3 1*2>").set(chords).mode("root:g2")
  .voicing().s("gm_acoustic_bass"),
  chords.n("[0 <4 3 <2 5>>*2](<3 5>,8)")
  .anchor("D5").voicing()
  .segment(4).clip(rand.range(.4,.8))
  .room(.75).shape(.3).delay(.25)
  .fm(sine.range(3,8).slow(8))
  .lpf(sine.range(500,1000).slow(8)).lpq(5)
  .rarely(ply("2")).chunk(4, fast(2))
  .gain(perlin.range(.6, .9))
  .mask("<0 1 1 0>/16")
)
.late("[0 .01]*4").late("[0 .01]*2").size(4)
```

## 4. "Caverave" — dark rave/house · Felix Roos (CC BY-NC-SA 4.0) · ~120 · default sounds only
Source: strudel.cc/examples/ (tunes.mjs)

```js
// "Caverave"
// @license CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
// @by Felix Roos

const keys = x => x.s('sawtooth').cutoff(1200).gain(.5)
  .attack(0).decay(.16).sustain(.3).release(.1);

const drums = stack(
  s("bd*2").mask("<x@7 ~>/8").gain(.8),
  s("~ <sd!7 [sd@3 ~]>").mask("<x@7 ~>/4").gain(.5),
  s("[~ hh]*2").delay(.3).delayfeedback(.5).delaytime(.125).gain(.4)
);

const synths = stack(

  "<eb4 d4 c4 b3>/2"
  .scale("<C:minor!3 C:melodic:minor>/2")
  .struct("[~ x]*2")
  .layer(
    x=>x.scaleTranspose(0).early(0),
    x=>x.scaleTranspose(2).early(1/8),
    x=>x.scaleTranspose(7).early(1/4),
    x=>x.scaleTranspose(8).early(3/8)
  ).note().apply(keys).mask("<~ x>/16")
  .color('darkseagreen'),

  note("<C2 Bb1 Ab1 [G1 [G2 G1]]>/2")
  .struct("[x [~ x] <[~ [~ x]]!3 [x x]>@2]/2".fast(2))
  .s('sawtooth').attack(0.001).decay(0.2).sustain(1).cutoff(500)
  .color('brown'),
  chord("<Cm7 Bb7 Fm7 G7b13>/2")
  .struct("~ [x@0.2 ~]".fast(2))
  .dict('lefthand').voicing()
  .every(2, early(1/8))
  .apply(keys).sustain(0)
  .delay(.4).delaytime(.12)
  .mask("<x@7 ~>/8".early(1/4))
).add(note("<-1 0>/8"))
stack(
  drums.fast(2).color('tomato'),
  synths
).slow(2)
```

## 5. "Amensister" — jungle/amen DnB · Felix Roos (CC BY-NC-SA 4.0) · ~165–170
Source: strudel.cc/examples/ (tunes.mjs). Needs dirt-samples.

```js
// "Amensister"
// @license CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
// @by Felix Roos

samples('github:tidalcycles/dirt-samples')

useRNG('legacy')

stack(
  // amen
  n("0 1 2 3 4 5 6 7")
  .sometimes(x=>x.ply(2))
  .rarely(x=>x.speed("2 | -2"))
  .sometimesBy(.4, x=>x.delay(".5"))
  .s("amencutup")
  .slow(2)
  .room(.5)
  ,
  // bass
  sine.add(saw.slow(4)).range(0,7).segment(8)
  .superimpose(x=>x.add(.1))
  .scale('G0 minor').note()
  .s("sawtooth")
  .gain(.4).decay(.1).sustain(0)
  .lpa(.1).lpenv(-4).lpq(10)
  .cutoff(perlin.range(300,3000).slow(8))
  .degradeBy("0 0.1 .5 .1")
  .rarely(add(note("12")))
  ,
  // chord
  note("Bb3,D4".superimpose(x=>x.add(.2)))
  .s('sawtooth').lpf(1000).struct("<~@3 [~ x]>")
  .decay(.05).sustain(.0).delay(.8).delaytime(.125).room(.8)
  ,
  // alien
  s("breath").room(1).shape(.6).chop(16).rev().mask("<x ~@7>")
  ,
  n("0 1").s("east").delay(.5).degradeBy(.8).speed(rand.range(.5,1.5))
).reset("<x@7 x(5,8,-1)>")
```

## 6. "broken cut 1" — breaks/broken beat · froos · setcps(1.25)
Source: strudel.cc/workshop/getting-started/ (featured). Needs dirt-samples + freesound URLs.

```js
// "broken cut 1" @by froos
// @version 1.0

samples('github:tidalcycles/dirt-samples')
samples({
  'slap': 'https://cdn.freesound.org/previews/495/495416_10350281-lq.mp3',
  'whirl': 'https://cdn.freesound.org/previews/495/495313_10350281-lq.mp3',
  'attack': 'https://cdn.freesound.org/previews/494/494947_10350281-lq.mp3'
})

setcps(1.25)

note("[c2 ~](3,8)*2,eb,g,bb,d").s("sawtooth")
  .noise(0.3)
  .lpf(perlin.range(800,2000).mul(0.6))
  .lpenv(perlin.range(1,5)).lpa(.25).lpd(.1).lps(0)
  .add.mix(note("<0!3 [1 <4!3 12>]>")).late(.5)
  .vib("4:.2")
  .room(1).roomsize(4).slow(4)
  .stack(
    s("bd").late("<0.01 .251>"),
    s("breaks165:1/2").fit()
    .chop(4).sometimesBy(.4, ply("2"))
    .sometimesBy(.1, ply("4")).release(.01)
    .gain(1.5).sometimes(mul(speed("1.05"))).cut(1)
    ,
    s("<whirl attack>?").delay(".8:.1:.8").room(2).slow(8).cut(2),
  ).reset("<x@30 [x*[8 [8 [16 32]]]]@2>".late(2))
```

## 7. Minimal amen chop — jungle building block · Strudel docs recipe
Source: strudel.cc/recipes/recipes/ ("Chopping breaks"). Needs `github:yaxu/clean-breaks`.

```js
samples('github:yaxu/clean-breaks')
s("amen/4").fit().chop(16).cut(1)
.sometimesBy(.5, ply("2"))
.sometimesBy(.25, mul(speed("-1")))
```

## 8. Lofi hip-hop full track — CodingWCal · setcps(.39), swung, `arrange()` sections
Source: github.com/CodingWCal/strudel-lofi. The only full *arranged* track here —
the intro→groove→sparkle→drop structure is the set-arrangement reference.

```js
//CodingWCal - GitHub Strudel Lo Fi Beat
setcps(.39)
swing(.21)

let kick =
  s("bd ~ ~ ~ bd ~ ~ ")

let ghostKick =
  s("~ bd ~ ~ ~ bd ~ ~ ")
    .gain(.4)

let snare =
  stack(
    s("~ ~ sd ~ ~ ~ sd ~").gain(.7),
    s("~ ~ sd ~ ~ ~ sd ~").gain(.15).lpf(1200)
  )

let rim =
  s("~ ~ ~ ~ rim ~ ~ ~")
    .gain(.05)

let hats =
  s("hh*8")
    .gain(sine.range(.18,.28).slow(6))
    .hpf(3500)
    .late(sine.range(0,.015).slow(4))

let drums =
  stack(kick, snare, hats, ghostKick, rim)

let chords =
  note("<[f2,ab3,c4,eb4,ab4 f2*2] [db2,f3,ab3,c4, c4*4 db2*2] [ab2,c3,eb3,g3,c4,ab3 ab4*4] [c3,e3,g3,bb3] [ab3,c4,eb4,f4]>")
    .sound("piano")
    .slow(2)
    .room(.6)
    .delay(.22)
    .gain(.60)
    .lpf(sine.range(900,1400).slow(16))
    ._pianoroll()
let altChords =
  stack(
    note("<f3 db3 ab3 c4>")
      .sound("piano")
      .slow(2)
      .gain(.4),

    note("<[ab3,c4,eb4]*8 [f3,ab3,c4] [c4,eb4,g4]*8 [e4,g4,bb4]*2>")
      .sound("piano")
      .slow(2)
      .late(.126)
      .gain(.75)
  )
  .lpf(1200)
  .room(.4)
  ._pianoroll()


let bass =
  note("<~ f1 ab1 db1 ~ db1 c2 ~ ab1 ~ c2 db2>")
    .sound("bass")
    .slow(2)
    .lpf(350)
    .gain(.95)
    .late(.02)

let sub =
  note("<f0 ~ db0 ~ ab0 ~ c1 ~>")
    .sound("bass")
    .slow(2)
    .lpf(200)
    .gain(.4)


let arp =
  note("<f5 ab5*2 c6 eb6*8 ab5*2 c7*4>")
    .fast(2)
    .sound("piano")
    .gain(.60)
    .room(.4)
    .delay(.2)
    .lpf(1500)
    ._pianoroll()

let burst =
  note("<f7 f7 f7 eb7>")
    .fast(8)
    .sound("piano")
    .gain(.10)
    .room(.1)

let burst2 =
  note("<f4 ab3*4 c3 eb3 c3 ab4*2 eb4>")
    .fast(8)
    .sound("piano")
    .delay(.2)
    .gain(.10)
    .room(.1)
    ._pianoroll()

let topline =
  note("<c5 ~ eb5 ~ g5 ~ ab5 ~ ~ ~ ~ ~>")
    .sound("piano")
    .slow(2)
    .gain(.40)
    .room(.6)
    .delay(.25)
    ._pianoroll()

let texture =
  s("white")
    .gain(sine.range(.01,.03).slow(12))
    .hpf(6000)
    .slow(8)

let intro =
  stack(
    chords.gain(.3),
    texture
  )
let groove =
  stack(
    drums,
    bass,
    chords,
    texture
  )
let sparkle =
  stack(
    drums,
    bass,
    chords,
    altChords,
    topline,
    texture
  )

let drop =
  stack(
    drums,
    bass,
    sub,
    chords,
    arp,
    topline,
    burst.every(4, x => x),
    burst2.every(12, x => x),
    texture
  )

arrange(
  [4, intro],
  [8, groove],
  [8, sparkle],
  [8, drop]
)
```

## 9. "Holy flute" — ambient/pastoral drone · Felix Roos (CC BY-NC-SA 4.0) · beatless
Source: strudel.cc/examples/ (tunes.mjs). Default sounds only.

```js
// "Holy flute"
// @license CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
// @by Felix Roos

useRNG('legacy')

"c3 eb3(3,8) c4/2 g3*2"
.superimpose(
  x=>x.slow(2).add(12),
  x=>x.slow(4).sub(5)
).add("<0 1>/16")
.note().s('ocarina_vib').clip(1)
.release(.1).room(1).gain(.2)
.color("salmon | orange | darkseagreen")
.pianoroll({fold:0,autorange:0,vertical:0,cycles:12,smear:0,minMidi:40})
```

## 10. "Random bells" — ambient generative · Felix Roos (CC BY-NC-SA 4.0) · very slow
Source: strudel.cc/examples/ (tunes.mjs). Freesound URLs.

```js
// "Random bells"
// @license CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
// @by Felix Roos

samples({
  bell: { c6: 'https://cdn.freesound.org/previews/411/411089_5121236-lq.mp3' },
  bass: { d2: 'https://cdn.freesound.org/previews/608/608286_13074022-lq.mp3' }
})

useRNG('legacy')

stack(
  // bells
  n("0").euclidLegato(3,8)
  .echo(3, 1/16, .5)
  .add(n(rand.range(0,12)))
  .scale("D:minor:pentatonic")
  .velocity(rand.range(.5,1))
  .s('bell').gain(.6).delay(.2).delaytime(1/3).delayfeedback(.8),
  // bass
  note("<D2 A2 G2 F2>").euclidLegatoRot(6,8,4).s('bass').clip(1).gain(.8)
)
  .slow(6)
  .pianoroll({vertical:1})
```

## 11. "Melting submarine" — electro-funk/breakbeat · Felix Roos (CC BY-NC-SA 4.0) · ~100–110
Source: strudel.cc/examples/ (tunes.mjs). Needs dirt-samples. Heavily commented — good teaching example.

```js
// "Melting submarine"
// @license CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
// @by Felix Roos

samples('github:tidalcycles/dirt-samples')
useRNG('legacy')

stack(
  s("bd:5,[~ <sd:1!3 sd:1(3,4,3)>],hh27(3,4,1)") // drums
  .speed(perlin.range(.7,.9)) // random sample speed variation
  //.hush()
  ,"<a1 b1*2 a1(3,8) e2>" // bassline
  .off(1/8,x=>x.add(12).degradeBy(.5)) // random octave jumps
  .add(perlin.range(0,.5)) // random pitch variation
  .superimpose(add(.05)) // add second, slightly detuned voice
  .note() // wrap in "note"
  .decay(.15).sustain(0) // make each note of equal length
  .s('sawtooth') // waveform
  .gain(.4) // turn down
  .cutoff(sine.slow(7).range(300,5000)) // automate cutoff
  .lpa(.1).lpenv(-2)
  //.hush()
  ,chord("<Am7!3 <Em7 E7b13 Em7 Ebm7b5>>")
  .dict('lefthand').voicing() // chords
  .add(note("0,.04")) // add second, slightly detuned voice
  .add(note(perlin.range(0,.5))) // random pitch variation
  .s('sawtooth') // waveform
  .gain(.16) // turn down
  .cutoff(500) // fixed cutoff
  .attack(1) // slowly fade in
  //.hush()
  ,"a4 c5 <e6 a6>".struct("x(5,8,-1)")
  .superimpose(x=>x.add(.04)) // add second, slightly detuned voice
  .add(perlin.range(0,.5)) // random pitch variation
  .note() // wrap in "note"
  .decay(.1).sustain(0) // make notes short
  .s('triangle') // waveform
  .degradeBy(perlin.range(0,.5)) // randomly controlled random removal :)
  .echoWith(4,.125,(x,n)=>x.gain(.15*1/(n+1))) // echo notes
  //.hush()
)
  .slow(3/2)
```

## 12. Dembow / latin-pop groove — official workshop final example · default sounds, `$:` style
Source: strudel.cc/workshop/first-effects/. Note: uses the `$:` label style the DJ harness needs for `all()`.

```js
$: note("[~ [<[d3,a3,f4]!2 [d3,bb3,g4]!2> ~]]*2")
.sound("gm_electric_guitar_muted").delay(.5)

$: sound("bd rim").bank("RolandTR707").delay(.5)

$: n("<4 [3@3 4] [<2 0> ~@16] ~>")
.scale("D4:minor").sound("gm_accordion:2")
.room(2).gain(.4)

$: n("[0 [~ 0] 4 [3 2] [0 ~] [0 ~] <0 2> ~]/2")
.scale("D2:minor")
.sound("sawtooth,triangle").lpf(800)
```
