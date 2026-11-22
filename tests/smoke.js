// Duman testi: oyunu tarayıcıda açar, otomatik bir oyuncuyla birkaç gün oynatır.
// Sayfada hata çıkarsa ya da gün bitmezse başarısız olur.
//   node tests/smoke.js            (Playwright ve Chromium kurulu olmalı)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const file = 'file://' + path.resolve(__dirname, '..', 'index.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 400, height: 860 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.goto(file);
  await page.waitForTimeout(400);
  await page.click('[data-act="toMorning"]');
  const days = await page.evaluate(() => {
    const g = window.__bakkal, out = [];
    const tapShelf = i => { if (i < 9) g.tap(30 + (i % 3) * 120 + 50, [142, 262, 382][Math.floor(i / 3)] + 10); else g.tap(348, 470 + (i - 9) * 40); };
    for (let d = 0; d < 5; d++) {
      g.act('open'); g.act('closeModal');
      let guard = 0;
      while (g.state.phase === 'day' && guard++ < 30000) {
        const S = g.state, t = S.player.task && S.player.task.type, busy = t === 'stock' || t === 'sign';
        if (S.deliveries.some(x => x.status === 'waiting') && t !== 'sign') g.tap(330, 60);
        else if (!busy && S.queue.length && t !== 'register') g.tap(70, 617);
        else if (!busy && !S.queue.length) { const i = S.shelves.findIndex((q, k) => k < 6 && q <= 3 && S.depot[k] > 0); if (i >= 0) tapShelf(i); }
        g.step(0.3);
      }
      if (g.state.phase !== 'report') return { error: 'gün bitmedi: ' + g.state.phase };
      const r = g.state.report;
      out.push(`gün ${r.day}: ${r.buyers}/${r.visitors} müşteri, ciro ${r.revenue}, kasa ${Math.round(g.state.money)}`);
      if (g.state.money < 0) break;
      g.act('toMorning');
      g.state.orders = [2, 2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0];
    }
    return { out };
  });
  await browser.close();
  if (days.error) errors.push(days.error);
  (days.out || []).forEach(l => console.log(l));
  if (errors.length) { console.error('BAŞARISIZ\n' + errors.join('\n')); process.exit(1); }
  console.log('Tamam: hata yok.');
})();
