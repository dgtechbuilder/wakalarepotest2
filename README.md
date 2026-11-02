# Wakala Agent

A browser game where you play a *wakala*, the Swahili word for an agent: someone who visits smallholder farms, reads what is wrong with a field, and helps the farmer fix it. It is a playable recreation of the **29 Oct Wakala Game** Figma design, extended with farm reviews, care routines, real farm photos and a game clock.

**Play it:** https://dgtechbuilder.github.io/wakalarepotest2/

**Design files**

- Figma, the source design: [29 Oct Wakala Game](https://www.figma.com/design/X7DzMjqtbBFsKSKGNjGxUY/29-Oct-Wakala-Game?node-id=0-1) (whether you can open it depends on the file's sharing settings in Figma)
- Every screen, panel and icon in this repo was rebuilt from that file. The art in `assets/` was exported from it.

> **Status: draft.** This is a working prototype for playtesting. The rules, numbers and farm advice are placeholders until an agronomist and the team review them (see "Open questions" below).

## Why this game matters

Village-based agents are often the closest source of farm advice and supplies for smallholder farmers. A good agent notices problems early, recommends the right fix and follows up until the crop recovers. A poor call can waste a farmer's money on the wrong product, or miss a problem until it is too late to save the harvest.

Those skills are learned in the field, slowly, and the cost of a mistake is real. This game is meant to give agents and would-be agents a safe place to practise the same habits:

- **Look before you judge.** Every review makes you check the crops, a leaf up close, the soil and water, and the whole farm before you decide.
- **Listen to the farmer, but check for yourself.** Farmers describe what they have seen. From round 4 they sometimes guess wrong, as real farmers do.
- **Know the right fix, not just the problem.** After a correct diagnosis you choose the treatment. Wrong treatments cost coins and come with a one-line lesson, for example why a weed killer would also kill the maize.
- **Follow through.** Care plans run over game days, and missed tasks set the field back. Recovery comes from steady work, not one visit.
- **Work safely.** Spraying asks you to put on the safety kit first, every time.

The game also models the business side of the agent's role from the Figma design: selling inputs, arranging loans, booking training and upgrading storage. Helping farms succeed raises their success score, which is the game's main goal.

## How to play

**First session (about 2.5 minutes at a normal pace)**

1. **Create your agent:** pick a name and a character (Girl or Boy).
2. **Walk to June's farm** along the dirt roads. Everything else is under a fog until you finish your first review.
3. **Review the farm:** June tells you what she has noticed. Look at the four pictures, tap the field that looks wrong and say what it needs.
4. **Plan the care and do the first task:** choose the right fix, then hold the button to water.
5. **Review Vincent's beans**, plan their care, and see when June's maize needs water again.

If your first call is wrong, you walk to Brian's farm and try again, so no one is stuck.

**After the first session**

- **Click a farm to visit it.** Click a farm or its label on the Home screen or the Map, and your agent walks there along the roads. The review opens when you arrive. If the farm isn't ready yet, your agent waits and the review starts on its own.
- **Seven rounds per farm, back to back.** Every farm has 7 written rounds and can be checked again 30 seconds after a review, so you can move from farm to farm without waiting. After round 7, rounds are random.
- **Five problems to spot:** needs water, pests and healthy fields from the start. Low nutrients and weeds are added from round 5 on any farm (or 2 hours after you start).
- **Care routines on a game clock.** One game day is one real hour, with a morning and an evening window. Tasks are hands-on: hold to water or spray, tap off caterpillars, hoe out weeds, add CAN fertilizer and water it in, or mulch. Missed tasks set a field back, and three misses in a row bring the problem back.
- **Tasks and reminders.** The Task screen lists what is due now, later and missed. Reminders appear in the game, and as browser notifications while the game is open in a background tab (turn them on in Settings).
- **Grow the business.** Sell inputs, arrange loans, book training and upgrade storage from the bottom menu.

## How it is built

The game is a single `index.html` file with plain HTML, CSS and JavaScript. It has no framework and no build step.

- **Fixed stage.** Everything is laid out on an 874 × 402 landscape stage, matching the Figma frame, and scaled to fit the window. On an upright phone the stage turns sideways to fill the screen.
- **Drawn farm pictures.** The review pictures are drawn in code from each round's data (crop, problem, how visible it is, and which field), so a new round needs no new art. Real photos are laid on top where a good one exists.
- **Real photos.** Photos come from Wikimedia Commons and load straight from their servers. If one can't load, the drawn picture shows instead. Authors and licences are listed under Settings, Photo credits.
- **Roads.** The dirt roads on the home map are traced as a small graph of points, and the agent always takes the shortest route. Open the game with `?dev` to see the graph and print the coordinates of any tap.
- **Game clock and care.** Care plans are lists of tasks with time windows on the game clock. A timer checks every second for tasks that are due, missed or complete.
- **Saving.** Progress is saved in the browser's local storage on this device, under `wakala-save-v3`. Settings has a Restart button that clears it.
- **Event log.** Key moments, such as the first move, each review and each care task, are logged with timings. Type `wakalaEvents()` in the browser console to read them during a playtest.

## Project structure

| Path | What it is |
| --- | --- |
| `index.html` | The whole game |
| `assets/` | Art exported from the Figma file. `agent-girl.png` and `agent-boy.png` are the two player characters |
| `tools/build_standalone.py` | Builds a single-file copy with every image embedded (`dist/wakala-game.html`) |
| `tools/playtest/` | Automated Playwright playtests |
| `404.html`, `.nojekyll` | GitHub Pages support files |

## Run it locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Playtesting

Settings has three playtest buttons: make all farms ready, skip 2 game hours, and unlock the new problems.

The automated playtests need `pip install playwright` and a Chromium browser. Set `CHROME=/path/to/chrome` to use your own.

```sh
python3 tools/playtest/fs.py right      # first session, right answers (HUMAN=1 for human pacing)
python3 tools/playtest/fs.py wrong      # first session with a wrong call and the retry
python3 tools/playtest/free.py          # road walking, tasks, spraying, misses, settings
python3 tools/playtest/rounds.py        # all 7 rounds on every farm, back to back
python3 tools/playtest/clicks.py        # click each farm on Home, Map and a hub map
```

Screenshots are saved to `tools/playtest/out/`.

## Deployment

GitHub Pages publishes the `main` branch from the root folder. Every push to `main` goes live within about a minute, and there is no staging step. To review changes before players see them, work on a separate branch and merge it into `main` when it is approved.

## Open questions

- **Farm advice.** The product names are generic active ingredients (for example emamectin benzoate for armyworm, and lambda-cyhalothrin for bean pests). The bean product is a placeholder until an agronomist confirms it.
- **Care plans with fast rounds.** Care plans run on game days while rounds come every 30 seconds, so tasks can pile up during long sessions. One option is a single "fix it now" action within each round.
- **Missing photos.** Low nutrients and dry bean leaves still use the drawn pictures.
- **Reminders with the game closed** need a push service, which isn't built yet.
- **Hub maps** (after a storage upgrade) have no traced roads, so the agent walks straight to each farm there.

## Credits

- Design: the 29 Oct Wakala Game Figma file (linked above).
- Photos: Wikimedia Commons contributors, under CC BY, CC BY-SA and CC0 licences. The full list with links is in the game under Settings, Photo credits. Photos are cropped and zoomed for the game.
