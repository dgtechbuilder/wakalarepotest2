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

## How to play

1. **Inspect** five areas of a farm. Each one shows what you see in the field; rate it Good, Fair or Poor.
2. **Advise** the farmer on every area that isn't good.
3. **Submit** the report. Accurate ratings earn coins, gems and water, and your advice raises the farm's success score.

Goal: get all four farms to a success score of 80 or more. The orange **Next** bar always shows your next step.

Progress is saved in the browser on this device. Settings (the cog) has your name, How to play, and Restart.
