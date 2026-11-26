// Renders every page in social/src/manifest.json to social/posts/<name>.png and <name>@2x.png.
// Fonts load from assets/fonts over a local server, so the text is the real brand type.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const OUT = path.join(ROOT, 'social/posts');
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'social/src/manifest.json'), 'utf8'));

const types = { '.html': 'text/html', '.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(ROOT) || !fs.existsSync(p)) return res.writeHead(404).end();
  res.writeHead(200, { 'content-type': types[path.extname(p)] ?? 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise((ok) => server.listen(0, '127.0.0.1', ok));
const base = `http://127.0.0.1:${server.address().port}/social/src/`;

const browser = await chromium.launch();
fs.mkdirSync(OUT, { recursive: true });
for (const scale of [1, 2]) {
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  for (const { file } of manifest) {
    await page.goto(base + file + '.html', { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const check = await page.evaluate(() => ({
      fonts: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family + f.weight),
      overflow: [...document.querySelectorAll('.post *')].some((e) => {
        const r = e.getBoundingClientRect();
        return r.right > 1081 || r.bottom > 1351;
      }),
    }));
    await page.screenshot({ path: path.join(OUT, `${file}${scale === 2 ? '@2x' : ''}.png`), clip: { x: 0, y: 0, width: 1080, height: 1350 } });
    if (scale === 1) console.log(file, 'fonts:', check.fonts.length, check.overflow ? 'OVERFLOW' : 'ok');
  }
  await ctx.close();
}
await browser.close();
server.close();
