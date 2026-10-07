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
.card{background:rgba(20,15,10,.55);border:2px solid rgba(242,199,102,.55);border-radius:36px;padding:56px 48px;backdrop-filter:blur(6px)}
.uz{font-size:50px;font-weight:600;line-height:1.3;margin-top:30px}
.src{font-size:36px;font-weight:600;color:#fff;opacity:.92}
.num{display:inline-block;width:84px;height:84px;line-height:84px;border-radius:50%;background:#F2C766;color:#2a1d08;font-size:44px;font-weight:800;margin-bottom:36px}
`;
function html(c) {
  let body = '';
  switch (c.type) {
    case 'hook':
      body = `<div class="box" style="top:560px"><div class="rule"></div><div class="main" style="font-size:112px">${hl(c.main)}</div></div>`; break;
    case 'title':
      body = `<div class="box" style="top:640px">${c.small ? `<div class="small">${c.small}</div>` : ''}<div class="rule"></div><div class="main" style="font-size:96px">${hl(c.main)}</div></div>`; break;
    case 'list':
      body = `<div class="box" style="top:600px"><div class="num">${c.n}</div><div class="main" style="font-size:98px">${hl(c.main)}</div></div>`; break;
    case 'hadith':
      body = `<div class="box" style="top:300px"><div class="small">Hadis</div><div class="card"><div class="ar">${c.arabic}</div><div class="uz">${c.uz}</div></div></div>
              <div class="box src" style="top:1170px">${c.source}</div>`; break;
    case 'closing':
      body = `<div class="box" style="top:480px"><div class="rule"></div><div class="main" style="font-size:90px">${hl(c.main)}</div><div style="font-size:48px;font-weight:600;margin-top:60px;opacity:.95">${c.sub}</div></div>`; break;
  }
  return `<html><head><meta charset="utf-8"><style>${css}</style></head><body><div class="scrim"></div>${body}</body></html>`;
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const s of cfg.scenes) for (const [i, c] of s.cards.entries()) {
    await p.setContent(html(c)); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(root, 'assets/cards', `${s.id}_${i + 1}.png`), omitBackground: true });
  }
  await b.close(); console.log('kartalar tayyor');
})();
