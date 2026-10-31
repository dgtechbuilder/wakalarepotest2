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

Your first session:

1. **Create your agent:** pick a name and a look.
2. **Walk to June's farm:** tap the path to walk.
3. **Review the farm:** look at the crops, a leaf up close, the soil and water, and the whole farm from above. Spot the field that looks wrong and choose what it needs: healthy, needs water, or pest problem.
4. **Next review:** the map opens and Vincent's beans need you. One farm will be ready to check tomorrow.

Every review uses the same four steps (Look, Spot, Judge, Result). The pictures are drawn in code from each farm's data, so new reviews need no new artwork.

For playtesting, `wakalaEvents()` in the browser console lists the first-session events with timings, and Settings has "make all farms ready now".

Progress is saved in the browser on this device. Settings (the cog) has your name, How to play, and Restart.
