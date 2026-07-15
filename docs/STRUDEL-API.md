# Strudel programmatic control — verified research (2026-07-15)

Everything below was verified live (headless Chromium driving the real CDN
bundle), not just read from docs. Source ground truth is
**codeberg.org/uzu/strudel** (the GitHub `tidalcycles/strudel` repo is an
archived mirror). npm names unchanged.

## Use `@strudel/web` (1.3.0). Not `@strudel/embed`.

`@strudel/embed` is just a web component wrapping an iframe of strudel.cc with
the code base64'd into the URL — **no inbound postMessage exists** in the REPL,
so changing code means reloading the iframe (audio stops, cross-origin play
button). It's for blog posts. `@strudel/web` runs the whole engine in-page.

Verified CDN: `https://unpkg.com/@strudel/web@1.3.0` (IIFE; also
`/dist/index.mjs` for ESM, or `cdn.jsdelivr.net/npm/@strudel/web@1.3.0/dist/index.min.js`).

```html
<script src="https://unpkg.com/@strudel/web@1.3.0"></script>
<script>
  const replPromise = initStrudel({
    prebake: () => samples('github:tidalcycles/dirt-samples'),
    onUpdateState: (st) => {/* reactive: started, evalError, ... */},
  });
  // after first user gesture (or --autoplay-policy=no-user-gesture-required):
  const repl = await replPromise;
  await evaluate('setcps(140/60/4); $: s("bd*4")');  // play
  await evaluate('$: s("hh*8").gain(.5)');           // swap mid-flight
  repl.stop();                                        // stop
</script>
```

After `initStrudel()` resolves, the whole API is on `globalThis`: `evaluate`,
`hush`, `samples`, `setcps`, `xfade`, `ref`, `all`, `stack`, `silence`,
`getCps`, `getIsStarted`, ...

## Gotchas (all verified)

1. **`hush()` doesn't stop playback after the first `evaluate()`** — each
   evaluate overwrites the global `hush` with a repl-internal one that clears
   the `$:` registry but leaves the scheduler running. **Use `repl.stop()`**,
   or `evaluate('silence')` to go quiet while keeping the clock.
2. **`all()`/`each()` only see `$:`/`d1:`-labeled patterns** — an unlabeled
   pattern in a program that also calls `all()` produces silence. The DJ brain
   must always emit `$:`-labeled patterns (the YouTube lessons all do).
3. **Sample buffers are lazy** — `samples('github:owner/repo')` fetches only a
   name→URL manifest (`raw.githubusercontent.com/.../main/strudel.json`, at
   call time, network required); audio downloads+decodes on *first trigger*,
   so a sound's first hit can be late/dropped. Warm up by playing the upcoming
   pattern once at `.gain(0)`. `{prebake:true}` does NOT pre-download.
4. **`@strudel/web`'s default prebake is synths only** — the strudel.cc REPL's
   default banks (piano, VCSL, tidal-drum-machines, EmuSP12, uzu-drumkit,
   `.bank('tr909')`...) come from `strudel.b-cdn.net/*.json`; mirror the
   `samples()` calls from `website/src/repl/prebake.mjs` in the strudel repo
   if lesson code references them.
5. **Autoplay**: `initStrudel` binds a one-time document `mousedown` to unlock
   audio; one gesture is enough forever (kiosk: launch Chromium with
   `--autoplay-policy=no-user-gesture-required`). Explicit: call `initAudio()`
   in your own gesture handler.

## Clock / transitions (the DJ moves)

- Scheduler: `repl.scheduler.now()` = current cycle as a float; `.cps`,
  `.started`, `.pattern` readable. `repl.state` = `{started, code, activeCode,
  evalError, schedulerError, pending, ...}`. Upcoming events:
  `repl.state.pattern.queryArc(begin, end)`.
- **Re-evaluating mid-cycle does not glitch or reset the clock** (verified:
  cycle counter continuous across a swap). New pattern is queried from the next
  tick at the same absolute cycle number → **swaps are beat-aligned free**.
  It's a hard cut; scheduled notes (~0.1s lookahead + tails) ring out.
- Cut exactly on the next cycle boundary:
  `const now = repl.scheduler.now(); setTimeout(() => evaluate(next), ((Math.ceil(now) - now) / repl.scheduler.cps) * 1000)`
- **`xfade(a, pos, b)`** exists in core (pos 0 = all a, 1 = all b; gain-domain
  linear, not equal-power). Method form `patA.xfade(pos, patB)`.
- **`ref()` is the crossfader primitive**: `xfade(a, ref(() => window.mix), b)`
  — then animate `window.mix` from plain JS, **no re-evaluation needed**.
  Same trick works anywhere a value goes: `all(x => x.gain(ref(() => window.fade)))`
  = a master fader JS can ride. (xfade wraps *pattern expressions*; for
  arbitrary multi-statement programs, fade master down → cut → fade up.)
- `setcps(x)` inside evaluated code, `repl.setCps(x)` from JS; tempo changes
  re-anchor phase smoothly.

## Working reference implementation

`dj/index.html` in this repo (and the original probe pair
`dj-test.html`/`probe.mjs` in the research scratchpad) — drive it headless with
playwright-core + `--autoplay-policy=no-user-gesture-required`.
