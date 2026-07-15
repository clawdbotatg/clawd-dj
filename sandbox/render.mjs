// Render Strudel code to a WAV, headless — the sandbox's ears.
// Usage: node sandbox/render.mjs <code.strudel> <out.wav> [secs] [warmup]
import { chromium } from '/Users/austingriffith/clawd/clawd-harness/tools/node_modules/playwright-core/index.mjs';
import { createServer } from 'http';
import { readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const [codeFile, outWav, secsArg, warmupArg] = process.argv.slice(2);
if (!codeFile || !outWav) {
  console.error('usage: node sandbox/render.mjs <code.strudel> <out.wav> [secs=20] [warmup=3]');
  process.exit(2);
}
const secs = +(secsArg ?? 20);
const warmup = +(warmupArg ?? 3);
const code = readFileSync(codeFile, 'utf8');

const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(here, 'render-page.html'));
const srv = createServer((req, res) => { res.setHeader('content-type', 'text/html'); res.end(html); });
await new Promise((r) => srv.listen(8933, r));

const browser = await chromium.launch({
  headless: true,
  executablePath:
    '/Users/austingriffith/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell',
  args: ['--autoplay-policy=no-user-gesture-required'],
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
await page.goto('http://127.0.0.1:8933/');
await page.waitForFunction('!!window.__replPromise', null, { timeout: 30000 });
await page.evaluate('window.__replPromise.then(() => (window.__ready = true))');
await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
await page.mouse.click(10, 10);

const res = await page.evaluate(
  ([c, s, w]) => window.__render(c, s, w), [code, secs, warmup],
);
if (!res.ok) {
  console.error(JSON.stringify({ ok: false, msg: res.msg, errors: errors.slice(0, 5) }));
  await browser.close(); srv.close(); process.exit(1);
}
writeFileSync(outWav, Buffer.from(res.wavBase64, 'base64'));
console.log(JSON.stringify({
  ok: true, out: outWav, secs: +(res.frames / res.sampleRate).toFixed(2),
  sampleRate: res.sampleRate, cps: res.cps, errors: errors.slice(0, 5),
}));
await browser.close(); srv.close(); process.exit(0);
