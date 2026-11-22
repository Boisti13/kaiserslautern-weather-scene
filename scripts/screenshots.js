// Screenshots for the README, from the gallery (python3 art/gallery.py first).
// Run:  NODE_PATH=<dir with playwright> node scripts/screenshots.js
const { chromium } = require('playwright');
const path = require('path');
const root = path.resolve(__dirname, '..');
const shots = {  // file name -> card caption in the gallery
  'day-partly': ['Day', 'Partly cloudy'], 'day-pour': ['Day', 'Downpour'], 'day-storm': ['Day', 'Thunderstorm'],
  'day-fog': ['Day', 'Fog'], 'twilight-clear': ['Twilight', 'Clear'], 'night-clear': ['Night', 'Clear'],
  'night-snow': ['Night', 'Snow'], 'match-night': ['Specials', 'Match night'], 'christmas': ['Specials', 'Christmas evening'],
  'snow-roofs': ['Specials', 'Snow on the roofs'], 'autumn': ['Specials', 'Autumn'], 'sunset': ['Specials', 'Sunset'],
};
(async () => {
  const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const p = await b.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(root, 'gallery.html'));
  await p.waitForTimeout(3000);
  for (const [name, [group, title]] of Object.entries(shots)) {
    const card = p.locator('section', { has: p.locator('h2', { hasText: new RegExp('^' + group + '$') }) })
      .locator('figure', { has: p.locator('figcaption b', { hasText: new RegExp('^' + title + '$') }) }).locator('.card');
    await card.screenshot({ path: path.join(root, 'docs', 'screenshots', name + '.png') });
    console.log('docs/screenshots/' + name + '.png');
  }
  await b.close();
})();
