#!/usr/bin/env bash
# Copy the built scene, the package and the macros to Home Assistant.
#   HOST=<ssh host of HA's Terminal & SSH app> scripts/deploy.sh   (default: ha)
# Ships the committed state of www/weather/ and ha/ (commit first).
# Afterwards: reload "Template entities" and "Custom Jinja2 templates"
# (Developer tools > YAML), and if card/ changed, paste card/weather-card.yaml
# into the dashboard. A changed picture needs a new ?v= in card/layers.js.
set -euo pipefail
cd "$(dirname "$0")/.."
HOST=${HOST:-ha}
if ! git diff --quiet HEAD -- www ha card; then
  echo "Uncommitted changes in www/, ha/ or card/ - commit first." >&2
  exit 1
fi
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
git archive HEAD www/weather ha | tar -x -C "$tmp"
ssh "$HOST" 'mkdir -p /config/www/weather /config/packages /config/custom_templates && rm -f /config/www/weather/kl-*.svg'
tar -C "$tmp/www/weather" -cf - . | ssh "$HOST" 'tar -xf - -C /config/www/weather'
tar -C "$tmp/ha" -cf - packages/weather_scene.yaml custom_templates/overview_sky.jinja | ssh "$HOST" 'tar -xf - -C /config'
ssh "$HOST" 'ls /config/www/weather/kl-*.svg | wc -l | sed "s/^/scene files on HA: /"; ha core check'
echo "Done. Reload template entities and custom templates in Home Assistant."
