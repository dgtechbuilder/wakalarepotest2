# Wakala Agent

A playable web recreation of the **29 Oct Wakala Game** Figma design: a farm-agent game where you inspect farms, advise farmers, trade inputs, take loans, book training and upgrade storage.

**Play:** https://dgtechbuilder.github.io/wakalarepotest2/

## What's in it

- `index.html`: the whole game (HTML, CSS and vanilla JavaScript, no build step)
- `assets/`: art exported from the Figma file (backgrounds, icons, characters)

## Run locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

Progress is saved in the browser's local storage. Tap the settings cog twice to start a new game.
