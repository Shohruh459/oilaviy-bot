// HTML/CSS -> shaffof PNG kartalar (1080x1920). Ishlatish: node render_cards.js
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'scenes.json')));
const hl = s => (s || '').replace(/\*(.+?)\*/g, '<b class="hl">$1</b>');
const css = `
*{margin:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;font-family:'Inter',sans-serif;color:#fff;overflow:hidden}
.scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,8,6,.55) 0%,rgba(10,8,6,.30) 35%,rgba(10,8,6,.30) 60%,rgba(10,8,6,.70) 100%)}
.box{position:absolute;left:80px;right:80px;text-align:center;text-shadow:0 4px 28px rgba(0,0,0,.55)}
.hl{color:#F2C766;font-weight:800}
.main{font-weight:800;line-height:1.18;letter-spacing:-.5px}
.rule{width:120px;height:6px;border-radius:3px;background:#F2C766;margin:0 auto 44px}
.small{font-size:44px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#F2C766;margin-bottom:28px}
.ar{font-family:'DejaVu Sans','FreeSerif',serif;direction:rtl;font-size:62px;line-height:1.55;color:#F2C766}
.qcard{background:rgba(255,249,236,.95);border:3px solid #C9A25A;border-radius:40px;padding:64px 52px 56px;color:#3a2a14;text-shadow:none;box-shadow:0 30px 80px rgba(60,35,10,.35)}
.qcard .label{font-size:34px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#9a7430;margin-bottom:34px}
.qcard .ar{font-family:'FreeSerif','DejaVu Sans',serif;direction:rtl;font-size:84px;line-height:1.7;color:#2b1d0a}
.qcard .sep{width:90px;height:4px;background:#C9A25A;margin:34px auto}
.qcard .uz{font-size:50px;font-weight:600;line-height:1.32;color:#3a2a14;margin-top:0}
.qcard .src{font-size:38px;font-weight:700;color:#9a7430;margin-top:40px;opacity:1}
.uz{font-size:50px;font-weight:600;line-height:1.3;margin-top:30px}
.src{font-size:36px;font-weight:600;color:#fff;opacity:.92}
.num{display:inline-block;width:84px;height:84px;line-height:84px;border-radius:50%;background:#F2C766;color:#2a1d08;font-size:44px;font-weight:800;margin-bottom:36px}
`;
function html(c) {
  let body = '';
  switch (c.type) {
    case 'hook':
      body = `<div class="box" style="top:${c.y??560}px"><div class="rule"></div><div class="main" style="font-size:${c.fs??112}px">${hl(c.main)}</div></div>`; break;
    case 'title':
      body = `<div class="box" style="top:${c.y??640}px">${c.small ? `<div class="small">${c.small}</div>` : ''}<div class="rule"></div><div class="main" style="font-size:${c.fs??96}px">${hl(c.main)}</div></div>`; break;
    case 'list':
      body = `<div class="box" style="top:${c.y??600}px"><div class="num">${c.n}</div><div class="main" style="font-size:${c.fs??98}px">${hl(c.main)}</div></div>`; break;
    case 'hadith':
      body = `<div class="box" style="top:250px"><div class="qcard"><div class="label">${c.label}</div><div class="ar">${c.arabic}</div><div class="sep"></div><div class="uz">${c.uz}</div><div class="src">${c.source}</div></div></div>`; break;
    case 'closing':
      body = `<div class="box" style="top:${c.y??480}px"><div class="rule"></div><div class="main" style="font-size:${c.fs??90}px">${hl(c.main)}</div>${c.sub?`<div style="font-size:48px;font-weight:600;margin-top:60px;opacity:.95">${c.sub}</div>`:''}</div>`; break;
  }
  return `<html><head><meta charset="utf-8"><style>${css}</style></head><body>${c.type==='hadith'?'':'<div class="scrim"></div>'}${body}</body></html>`;
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const s of cfg.scenes) for (const [i, c] of s.cards.entries()) {
    await p.setContent(html(c)); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(root, 'assets/cards', `${s.id}_${i + 1}.png`), omitBackground: true });
  }
  // S4 hadis kartasi foni: AI'siz, lokal SVG/CSS (assets/images/s4.png; foydalanuvchining s4.jpg bo'lsa u ustun)
  const girih = (() => { let l = ''; const R = 90;
    for (let y = -1; y < 24; y++) for (let x = -1; x < 14; x++) {
      const cx = x * R * 1.5 + (y % 2 ? R * .75 : 0), cy = y * R * .866 * 1;
      l += `<g transform="translate(${cx},${cy})"><polygon points="0,-40 11,-11 40,0 11,11 0,40 -11,11 -40,0 -11,-11" fill="none"/><polygon points="0,-40 28,-28 40,0 28,28 0,40 -28,28 -40,0 -28,-28" fill="none"/></g>`; }
    return l; })();
  const bgHtml = `<html><head><meta charset="utf-8"><style>*{margin:0}html,body{width:1080px;height:1920px;overflow:hidden}
    body{background:radial-gradient(ellipse at 50% 38%,#F6E7C6 0%,#E9CD96 55%,#C99B58 100%)}
    svg{position:absolute;inset:0;opacity:.13}svg *{stroke:#7a5524;stroke-width:1.6}
    .v{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 45%,rgba(55,30,8,.55) 100%),linear-gradient(180deg,rgba(0,0,0,0) 62%,rgba(40,22,6,.78) 100%)}</style></head>
    <body><svg width="1080" height="1920" viewBox="0 0 1080 1920">${girih}</svg><div class="v"></div></body></html>`;
  const p2 = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1.5 });
  await p2.setContent(bgHtml);
  await p2.screenshot({ path: path.join(root, 'assets/images/s4.png') });
  await b.close(); console.log('kartalar tayyor');
})();
