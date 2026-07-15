// Headless verification of dj/index.html — drives the real page + real CDN
// bundle and asserts the window.dj API works end-to-end.
// Run: node dj/probe.mjs   (uses clawd-harness tools' playwright-core)
import { chromium } from '/Users/austingriffith/clawd/clawd-harness/tools/node_modules/playwright-core/index.mjs';
import { createServer } from 'http';
import { readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(here, 'index.html'));
const srv = createServer((req, res) => {
  res.setHeader('content-type', 'text/html');
  res.end(html);
});
await new Promise((r) => srv.listen(8932, r));

const browser = await chromium.launch({
  headless: true,
  executablePath:
    '/Users/austingriffith/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell',
  args: ['--autoplay-policy=no-user-gesture-required'],
});
const page = await browser.newPage();
const errors = [];
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
page.on('pageerror', (e) => errors.push('PAGEERROR: ' + e.message));

await page.goto('http://127.0.0.1:8932/');
await page.waitForFunction('!!window.__replPromise', null, { timeout: 30000 });
await page.evaluate('window.__replPromise.then(() => (window.__ready = true))');
await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
await page.mouse.click(200, 200); // audio unlock path parity with real use

const result = await page.evaluate(async () => {
  const out = {};
  const A = 'setcps(1)\n$: s("bd*4")\n$: s("hh*8").gain(.4)';
  const B = '$: s("bd sd bd sd")\n$: n("0 3 7").scale("c2:minor").s("sawtooth").lpf(500)';
  const BAD = '$: s("bd*4").thisFunctionDoesNotExist(3)';

  out.playOk = await dj.play(A);
  await new Promise((r) => setTimeout(r, 1500));
  const s1 = dj.state();
  out.playing = s1.started && s1.cycle > 0;
  out.cps = s1.cps;

  const cycleBefore = dj.state().cycle;
  out.cutOk = await dj.cut(B);
  out.clockContinuous = dj.state().cycle >= cycleBefore; // no reset across swap

  out.fadeOk = await dj.fade(A, 2); // 2s fade round-trip
  out.faderBackUp = Math.abs(dj.state().fader - 1) < 0.01;

  out.badEvalOk = await dj.play(BAD); // must be false, not a throw
  out.lastEvalErr = dj.state().lastEval.msg.slice(0, 80);
  out.recoveredOk = await dj.play(A); // deck still usable after an error

  await dj.silence();
  out.silencedStillRunning = dj.state().started;
  await dj.stop();
  out.stopped = !dj.state().started;
  out.logTail = dj.log().slice(-4);
  return out;
});

console.log(JSON.stringify({ result, errors: errors.slice(0, 8) }, null, 2));
const pass =
  result.playOk && result.playing && result.cutOk && result.clockContinuous &&
  result.fadeOk && result.faderBackUp && result.badEvalOk === false &&
  result.recoveredOk && result.silencedStillRunning && result.stopped;
console.log(pass ? 'PROBE PASS' : 'PROBE FAIL');
await browser.close();
srv.close();
process.exit(pass ? 0 : 1);
