#!/usr/bin/env python3
"""Build the weather card's scene gallery: one self-contained HTML page.

Run:  python3 art/gallery.py [svg dir] [layers.js] [out.html]
  svg dir      the built scene files (default: www/weather)
  layers.js    the card's layer function (default: card/layers.js), the same
               code as in the card's styles (`background: ${...}`)
  out.html     default: gallery.html (not committed)
Every SVG is inlined as a data: URI, and the card's own layer function picks
the layers for each scene, so the gallery shows exactly what the card does.
"""
import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
args = sys.argv[1:] + [None] * 3
svg_dir = Path(args[0] or ROOT / "www" / "weather")
js_path = Path(args[1] or ROOT / "card" / "layers.js")
out = Path(args[2] or ROOT / "gallery.html")

js = js_path.read_text().strip()
u_line = re.search(r'const u = \(f\) => .*?;\n', js).group(0)
js = js.replace(u_line, 'const u = (f) => "var(--f-" + f.replace(".svg", "") + ")";\n')
assert "/local/weather" not in js

files = sorted(svg_dir.glob("kl-*.svg"))
svg_vars = "\n".join(
    f'  --f-{f.stem}: url("data:image/svg+xml,{urllib.parse.quote(f.read_text(), safe=" =:/,;-_.!~*()")}");'
    for f in files)

SKY = """
  --sky-night: linear-gradient(180deg, #0b1430, #1d2b55 70%, #3a4a78);
  --sky-night-grey: linear-gradient(180deg, #141a27, #262e40 70%, #3c4458);
  --sky-twilight: linear-gradient(180deg, #2b3a6b, #b0627a 65%, #f0a868);
  --sky-twilight-grey: linear-gradient(180deg, #3a4060, #7a6878 65%, #a88f88);
  --sky-clear: linear-gradient(180deg, #2f7fc8, #79b8e8 70%, #c4e2f6);
  --sky-partly: linear-gradient(180deg, #4f86b8, #97bad8 70%, #cfdde9);
  --sky-cloudy: linear-gradient(180deg, #66778a, #9eabb8 75%, #c1cad3);
  --sky-fog: linear-gradient(180deg, #8f99a3, #b9c0c7 70%, #d5dadf);
  --sky-rain: linear-gradient(180deg, #3f4c5a, #6f7d8b 75%, #8e9aa6);
  --sky-storm: linear-gradient(180deg, #23283a, #48506a 70%, #6a6f86);
  --sky-snow: linear-gradient(180deg, #8a9bb0, #c3cfdc 70%, #e8eef4);"""

W = ["clear", "partly", "cloudy", "fog", "rain", "pour", "hail", "sleet", "snow", "lightning", "storm"]
NAMES = {"clear": "Clear", "partly": "Partly cloudy", "cloudy": "Cloudy", "fog": "Fog", "rain": "Rain",
         "pour": "Downpour", "hail": "Hail", "sleet": "Sleet", "snow": "Snow", "lightning": "Lightning",
         "storm": "Thunderstorm"}
ICON = {"clear": "☀", "partly": "⛅", "cloudy": "☁", "fog": "≋", "rain": "☂", "pour": "☔", "hail": "❄",
        "sleet": "❄", "snow": "❄", "lightning": "ϟ", "storm": "ϟ"}


def sky_state(t, w):
    if t != "day":
        return t + ("" if w in ("clear", "partly") else "-grey")
    return {"pour": "rain", "hail": "rain", "sleet": "snow", "lightning": "storm"}.get(w, w)


SUN = {"day": (.72, 22), "twilight": (.86, 2), "night": (.9, -20)}


def scene(t, w, **over):
    sx, se = SUN[t]
    a = {"time": t, "weather": w, "windy": False, "drift": 0, "moon": 3, "moon_up": t == "night",
         "moon_x": .78, "moon_y": .26, "sun_x": sx, "sun_elev": se,
         "sun_y": round(min(max(.72 - se / 65 * .6, .1), .8), 3),
         "lights": t != "day" or w in ("storm", "lightning"), "snow_cover": w in ("snow", "sleet"),
         "season": "summer", "xmas": False, "match": False}
    a.update(over)
    return {"state": sky_state(t, a["weather"]), "attributes": a}


def card(title, st, note=""):
    w = st["attributes"]["weather"]
    lights = " · windows lit" if st["attributes"]["lights"] else ""
    return (f'<figure class="scene"><div class="card" data-s=\'{json.dumps(st)}\'>'
            f'<span class="ic">{ICON[w]}</span><span class="nm">{NAMES[w]}</span>'
            f'<span class="tp">3.4 °C</span><span class="chips">80 % · 1011 hPa · ↓1.2 · ↑5.0</span></div>'
            f'<figcaption><b>{title}</b><code>{st["state"]}</code>{note or lights}</figcaption></figure>')


sections = []
for t, title, sub in [("day", "Day", "sun above 6°"), ("twilight", "Twilight", "sun between −6° and 6°, low sun when clear"),
                      ("night", "Night", "sun below −6°, moon in its phase")]:
    sections.append((title, sub, [card(NAMES[w], scene(t, w)) for w in W]))

specials = [
    ("Morning sun", scene("day", "clear", sun_x=.18, sun_elev=10, sun_y=.63), " · sun low in the east (left)"),
    ("Midday sun", scene("day", "partly", sun_x=.5, sun_elev=21, sun_y=.53), " · winter noon, 21°"),
    ("Sunset", scene("twilight", "clear", sun_x=.82, sun_elev=1, sun_y=.71), " · low orange sun in the west"),
    ("Moonrise", scene("night", "clear", moon=5, moon_x=.12, moon_y=.6), " · waning moon low in the east"),
    ("Westerly gale", scene("day", "pour", drift=-3, windy=True), " · rain driven to the left"),
    ("Easterly snow", scene("day", "snow", drift=2, windy=True), " · snow blown to the right"),
    ("Snow on the roofs", scene("day", "clear", snow_cover=True, season="winter"), " · after snowfall, below 2 °C"),
    ("Snowy night", scene("night", "clear", snow_cover=True, season="winter", moon=4, moon_x=.6, moon_y=.2), " · full moon"),
    ("Spring", scene("day", "partly", season="spring"), " · blossom"),
    ("Autumn", scene("day", "partly", season="autumn"), " · coloured leaves"),
    ("Winter", scene("day", "cloudy", season="winter", lights=False), " · bare trees"),
    ("Christmas evening", scene("twilight", "partly", season="winter", xmas=True), " · tree and string lights"),
    ("Christmas night, snow", scene("night", "snow", season="winter", xmas=True), ""),
    ("Match day", scene("day", "cloudy", match=True, season="winter", lights=False), " · FCK home game: flags and crest"),
    ("Match night", scene("night", "partly", match=True, season="winter", moon=2, moon_x=.3, moon_y=.2), " · floodlights on"),
]
sections.append(("Specials", "the new layers: sun and moon position, wind, snow cover, seasons, Christmas, match day",
                 [card(*s) for s in specials]))

body = "".join(f'<section><header class="grp"><h2>{t}</h2><p>{sub}</p></header><div class="grid">{"".join(c)}</div></section>'
               for t, sub, c in sections)

page = f'''<meta charset="utf-8">
<title>Kaiserslautern Weather Scenes</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=Inter:wght@400;500;600&display=swap">
<style>
/* Layout: one band per group, scene cards at the dashboard's real card height in an auto-fill grid */
:root {{
  --bg: #eef1f5; --fg: #1b2430; --muted: #5b6778; --line: #d3d9e2; --accent: #b5654d; --code: #e2e7ee;
  --display: "Space Grotesk", system-ui, sans-serif; --body: "Inter", system-ui, sans-serif;
{svg_vars}
{SKY}
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #10151d; --fg: #e6ebf2; --muted: #93a0b2; --line: #263040; --accent: #e08a6f; --code: #1c2533; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg: #10151d; --fg: #e6ebf2; --muted: #93a0b2; --line: #263040; --accent: #e08a6f; --code: #1c2533; color-scheme: dark }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--body); padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 48px; }}
.wrap {{ max-width: 1480px; margin: 0 auto; display: grid; gap: 36px; }}
h1 {{ font-family: var(--display); font-size: clamp(26px, 4vw, 38px); margin: 0 0 6px; text-wrap: balance; letter-spacing: -.01em; }}
.lede {{ color: var(--muted); max-width: 72ch; margin: 0; line-height: 1.55; }}
.lede b {{ color: var(--accent); font-weight: 600; }}
section {{ display: grid; gap: 14px; }}
.grp {{ display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; border-bottom: 1px solid var(--line); padding-bottom: 8px; }}
.grp h2 {{ font-family: var(--display); font-size: 22px; margin: 0; }}
.grp p {{ margin: 0; color: var(--muted); font-size: 13px; letter-spacing: .02em; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr)); gap: 18px 16px; }}
.scene {{ margin: 0; display: grid; gap: 8px; min-width: 0; }}
.card {{ position: relative; height: 184px; border-radius: 12px; overflow: hidden; color: #fff; text-shadow: 0 1px 3px rgba(0,0,0,.55), 0 0 10px rgba(0,0,0,.25); }}
.ic {{ position: absolute; left: 14px; top: 22px; width: 48px; height: 48px; border-radius: 50%; background: rgba(255,255,255,.22); display: grid; place-items: center; font-size: 22px; }}
.nm {{ position: absolute; left: 76px; top: 26px; font-size: 14px; font-weight: 600; opacity: .92; }}
.tp {{ position: absolute; left: 76px; top: 44px; font-size: 30px; font-weight: 600; font-variant-numeric: tabular-nums; }}
.chips {{ position: absolute; left: 16px; bottom: 9px; font-size: 13px; font-variant-numeric: tabular-nums; }}
figcaption {{ display: flex; gap: 8px; align-items: baseline; font-size: 13px; color: var(--muted); flex-wrap: wrap; }}
figcaption b {{ color: var(--fg); font-weight: 600; }}
figcaption code {{ font-size: 12px; background: var(--code); padding: 1px 6px; border-radius: 4px; }}
</style>
<div class="wrap">
<header><h1>Kaiserslautern Weather Scenes</h1>
<p class="lede">Every scene the Overview weather card can paint: 11 weather types from the met.no forecast across day, twilight and night, then the special layers. All of it is animated: clouds drift with the wind, rain and snow slant with it, stars twinkle, lightning flashes, Christmas lights sparkle, the flags wave on match days, and a C-17 (every 2 minutes) and a C-5 (every 3 minutes) from Ramstein cross from left to right with their <b>lights blinking</b>. The view looks south, so the sun rises on the left. Grey code = the sky gradient (sensor state).</p></header>
{body}
</div>
<script>
const L = (hass) => {js};
document.querySelectorAll('.card').forEach(el => {{
  const hass = {{ states: {{ 'sensor.overview_sky': JSON.parse(el.dataset.s) }} }};
  el.style.background = L(hass);
}});
</script>'''
out.write_text(page)
print(f"{out}: {len(page) // 1024} KB, {len(files)} SVGs, {sum(len(c) for _, _, c in sections)} scenes")
