# Changelog

All notable changes, newest first.

## Unreleased

### Added
- The animated Kaiserslautern weather scene for Home Assistant, moved here
  from the owner's Home Assistant (first built 2026-11-04, reworked 2026-11-22):
  - hand-drawn skyline with daylight, overcast, snow, dusk and night colours,
    window grids, large church and rose windows, lit windows at night
  - 11 weather types with drifting clouds, rain, downpour, hail, sleet, snow,
    fog and lightning; rain and snow slant with the wind
  - sun and moon placed from their real positions, moon phases, stars
  - snow on the roofs, seasons, Christmas tree and lights
  - FCK home match days: floodlights, flags and a shield on the stand,
    fixtures from OpenLigaDB
  - a C-17 and a C-5 crossing the sky with their lights on
- `card/weather-card.yaml`, made by `scripts/card.py` from the template and
  `card/layers.js`.
- `ha/packages/weather_scene.yaml` and `ha/custom_templates/overview_sky.jinja`.
- `art/gallery.py` (every scene on one page), `scripts/deploy.sh`,
  `scripts/screenshots.js`.

### Changed
- The card title shows only the weather ("Cloudy", "Snowy" …) instead of
  "Outside · Cloudy"; without a forecast it shows the last known weather.

### Under the hood
- GitHub check: rebuilds the pictures and the card and compares them with
  the committed files; ruff for the Python scripts.
