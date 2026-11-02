# Wakala Agent

A playable web recreation of the **29 Oct Wakala Game** Figma design: a farm-agent game where you inspect farms, advise farmers, trade inputs, take loans, book training and upgrade storage.

**Play:** https://dgtechbuilder.github.io/wakalarepotest2/

## What's in it

- `index.html`: the whole game (HTML, CSS and vanilla JavaScript, no build step)
- `assets/`: art exported from the Figma file (backgrounds, icons, characters)
  - `agent-girl.png` and `agent-boy.png` are the two player characters
- `tools/build_standalone.py`: builds a single-file copy with every asset embedded (`dist/wakala-game.html`)
- `tools/playtest/`: Playwright playtests (see below)

## Run locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

## How to play

**First session (about 2.5 minutes)**

1. **Create your agent:** pick a name and a character (Girl or Boy).
2. **Walk to June's farm** along the dirt roads.
3. **Review the farm:** June tells you what she has noticed. Look at the crops, a leaf up close, the soil and water, and the whole farm from above. Spot the field that looks wrong and say what it needs.
4. **Plan the care and do the first task:** pick the right fix (a wrong pick costs coins and teaches a lesson), then hold to water.
5. **Review Vincent's beans**, plan their care, and see when June's maize needs water again.

**After that**

- **Click a farm to visit it.** Click any farm (or its label) on the Home screen or the Map, and the agent walks there along the roads and the farm's review opens on arrival. If the farm's next round isn't ready yet, the agent waits there and the review starts on its own (never more than 30 seconds). The Task and Farms screens' Review buttons do the same. On the Map the agent walks on the map itself, so the farm actions stay in reach.
- **7 rounds per farm, back to back.** Every farm has 7 written rounds and can be checked again 30 seconds after a review. Labels count down; if you arrive early, the agent waits and the round starts on its own. After round 7, rounds are random.
- **Problems to spot:** needs water, pests and healthy fields from the start; low nutrients and weeds from round 5 on any farm (or 2 hours after you start).
- **Farmers talk:** on arrival the farmer sums up what they have seen, and comments on each picture. From round 4 they sometimes guess wrong.
- **Care routines on a game clock:** 1 game day = 1 real hour, with morning and evening windows. Tasks are hands-on: hold to water or spray, tap off pests, hoe weeds, add CAN fertilizer, mulch. Spraying needs the safety kit and the right product (generic names: emamectin benzoate, lambda-cyhalothrin). Missed tasks set a field back; 3 misses in a row bring the problem back. The Task screen lists Due now, Later and Missed.
- **Walking:** tap anywhere on the Home map to walk the roads (shortest route); a new tap changes course. Open with `?dev` to see the traced road graph. After a storage upgrade the hub maps have no traced roads, so the agent walks straight to the farm there.
- **Reminders:** messages in the game, and browser notifications while the game is open in a background tab (turn on in Settings).
- **Real photos:** reviews use photos from Wikimedia Commons, with the drawn picture as a fallback. Credits are in Settings.

## Playtesting

- `wakalaEvents()` in the browser console lists the session events with timings.
- Settings has playtest buttons: make all farms ready, skip 2 game hours, unlock new problems.
- Automated playtests (needs `pip install playwright` and a Chromium; set `CHROME=/path/to/chrome` to use your own):

```sh
python3 tools/playtest/fs.py right      # first session, right answers (HUMAN=1 for human pacing)
python3 tools/playtest/fs.py wrong      # first session with a wrong call and the retry
python3 tools/playtest/free.py          # road walking, tasks, spraying, misses, settings
python3 tools/playtest/rounds.py        # all 7 rounds on every farm, back to back
python3 tools/playtest/clicks.py        # click each farm on Home, Map and a hub map: the agent walks there and the review opens
```

Screenshots go to `tools/playtest/out/`.

Progress is saved in the browser on this device. Settings (the cog) has your name, reminders, photo credits and Restart.
