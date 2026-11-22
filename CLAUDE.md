# Working on this repository

Notes for Claude Code (and anyone else) working on the Kaiserslautern
weather scene. Which Home Assistant it runs on, and how to reach it, is in
the owner's private notes, not here.

## Ground rules

- **Start with `git pull` on `dev`.** The owner works from more than one
  computer. Work on `dev`; don't merge to `main`, tag or release unless asked.
- **Public repository**: no addresses, hostnames, tokens or personal data;
  screenshots come from the gallery's made-up scenes only.
- **One change = one commit with everything it needs**: the drawing in
  `art/`, the rebuilt `www/weather/`, the card (`scripts/card.py`), the
  README and screenshots if something visible changed, and a CHANGELOG line
  (*Unreleased* until a version is asked for).
- **Never edit `www/weather/` or `card/weather-card.yaml` by hand** — they are
  built (`python3 art/build.py`, `python3 scripts/card.py`); the check fails
  otherwise. `art/kl-windows.svg` is the one hand-drawn file.
- **A changed picture needs a new `?v=`** in `card/layers.js` (browsers
  cache `/local/` for a month), then `scripts/card.py`.
- **`card/layers.js` must not contain backticks**: Bubble Card evaluates the
  styles as a template literal.

## Checking a change

- `python3 art/gallery.py`, open `gallery.html` and look at the scenes that
  changed (a screenshot with Playwright is fine); `scripts/screenshots.js`
  redoes the README pictures.
- Python checks: venv outside the repo (`~/.venvs/kaiserslautern-weather-scene`:
  `pyyaml`, `ruff`), `ruff check art scripts`.
- After pushing, watch the *Check* workflow (`gh run list --branch dev`).

## Deploying

`HOST=<ha ssh host> scripts/deploy.sh` copies the committed `www/weather/`,
the package and the macros, then runs `ha core check`. Then reload template
entities and custom templates; if `card/` changed, put
`card/weather-card.yaml` into the dashboard card.
