// Renders duel.html to a 1080x1920 MP4, frame by frame.
// Usage: node render.js [outDir]   (needs playwright and ffmpeg)
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const out = path.resolve(process.argv[2] || path.join(__dirname, 'out'));
const frames = path.join(out, 'frames');

(async () => {
  fs.rmSync(frames, { recursive: true, force: true });
  fs.mkdirSync(frames, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, 'duel.html') + '?rec=1');
  await page.waitForFunction(() => !!(window.__ready && window.__tl));
  const total = await page.evaluate(() => window.__tl.duration());
  const n = Math.ceil(total * FPS);
  for (let f = 0; f <= n; f++) {
    await page.evaluate(t => { window.__tl.time(t, false); }, f / FPS);
    await page.screenshot({ path: path.join(frames, String(f).padStart(4, '0') + '.jpg'), quality: 92 });
  }
  await browser.close();
  const mp4 = path.join(out, 'haboydem-duel.mp4');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(frames, '%04d.jpg'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', mp4]);
  console.log('frames', n + 1, 'seconds', total.toFixed(1), '->', mp4);
})();
