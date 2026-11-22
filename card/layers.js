(() => {
  const s = hass.states['sensor.overview_sky'];
  const a = (s && s.attributes) || {};
  const t = a.time || 'day', w = a.weather || 'cloudy', dark = t !== 'day';
  const u = (f) => "url('/local/weather/" + f + "?v=14')";
  const cover = (f, pos) => u(f) + ' ' + (pos || 'center') + ' / cover no-repeat';
  const city = (f) => u(f) + ' center bottom / 100% auto no-repeat';
  const at = (f, x, y, sw, sh) => u(f) + ' calc(' + (x * 100).toFixed(1) + '% + ' + (sw * x - sw / 2).toFixed(1) + 'px) ' + (y * 184 - sh / 2).toFixed(1) + 'px / ' + sw + 'px ' + sh + 'px no-repeat';
  const d = a.drift || 0, dn = (d < 0 ? 'm' : 'p') + Math.abs(d);
  const clear = ['clear', 'partly'].includes(w);
  const L = ['linear-gradient(0deg, rgba(0, 0, 0, .5), rgba(0, 0, 0, .16) 22%, transparent 40%)'];
  const precip = {rain: 'rain', pour: 'pour', storm: 'pour', hail: 'hail', sleet: 'sleet', snow: 'snow'}[w];
  if (precip) L.push(u('kl-' + precip + '-' + dn + '.svg') + ' 0 0 / 180px 180px repeat');
  if (w === 'fog') L.push(cover('kl-fog-' + (dark ? 'night' : 'day') + '.svg', 'center bottom'));
  if (a.xmas) L.push(city('kl-xmas-' + (dark ? 'night' : 'day') + '.svg'));
  if (a.snow_cover) L.push(city('kl-snowcap-' + t + '.svg'));
  if (a.match) L.push(city('kl-match-' + (dark ? 'night' : 'day') + '.svg'));
  if (a.lights) L.push(city('kl-windows.svg'));
  const pal = dark ? t : a.snow_cover ? 'snow' : clear ? 'day' : 'grey';
  L.push(city('kl-skyline-' + pal + '-' + (a.season || 'summer') + '.svg'));
  if (['storm', 'lightning'].includes(w)) L.push(cover('kl-lightning.svg'));
  L.push(cover('kl-planes-' + t + '.svg'));
  const speed = a.windy ? 'windy' : 'calm', dir = d < 0 ? 'l' : 'r';
  if (w === 'partly') L.push(cover('kl-clouds-partly-' + t + '-' + speed + '-' + dir + '.svg'));
  else if (w !== 'clear') {
    const cp = dark ? t : ['storm', 'lightning'].includes(w) ? 'storm' : ['rain', 'pour', 'hail', 'sleet'].includes(w) ? 'dark' : 'light';
    L.push(cover('kl-clouds-overcast-' + cp + '-' + speed + '-' + dir + '.svg'));
  }
  if (clear) {
    if (typeof a.sun_elev === 'number' && a.sun_elev > -3) L.push(at(a.sun_elev < 6 ? 'kl-sunlow.svg' : 'kl-sunball.svg', a.sun_x, a.sun_y, 120, 120));
    if (dark && a.moon && a.moon_up) L.push(at('kl-moon-' + a.moon + '.svg', a.moon_x, a.moon_y, 90, 90));
    if (t === 'night') L.push(cover('kl-stars.svg'));
  }
  L.push('var(--sky-' + ((s && s.state) || 'cloudy') + ')');
  return L.join(', ');
})()
