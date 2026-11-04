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

- **Click a farm to visit it.** Click a farm or its label on the Home screen or the Map, and your agent walks there along the roads (about 270 px/s on the 874 px-wide stage, three times the original pace; change `WALK_X` in `index.html` to tune it). The review opens when you arrive. There is no timer: you can walk to any farm at any time and check it.
- **Seven rounds per farm, back to back.** Every farm has 7 written rounds. You can play them in any order, on one farm after another or several in a row on the same farm. After round 7, rounds are random.
- **Five problems to spot:** needs water, pests and healthy fields from the start. Low nutrients and weeds are added from round 5 on any farm (or 2 hours after you start).
- **Care routines on a game clock.** One game day is one real hour, with a morning and an evening window. Tasks are hands-on: hold to water or spray, tap off caterpillars, hoe out weeds, add CAN fertilizer and water it in, or mulch. Missed tasks set a field back, and three misses in a row bring the problem back.
- **Tasks and reminders.** The Task screen lists what is due now, later and missed. Reminders appear in the game, and as browser notifications while the game is open in a background tab (turn them on in Settings).
- **Tractor jobs.** Each farm has three tractor stages through the season (before planting, planting and harvest), opened after your 2nd review of that farm (see below).
- **Grow the business.** Sell inputs, arrange loans, book training and upgrade storage from the bottom menu.

## Tractor jobs: the farm season

Every farm has three tractor stages, played in order through the season: **before planting**, **planting** and **harvest**. Each stage needs a different implement, and how well you prepare and plant shows up later in the harvest.

| Farm | Before planting | Planting | Harvest |
| --- | --- | --- | --- |
| Mark, maize, 1 acre, on a slope | Disc plough: turn in old stalks, across the slope | Maize planter | Maize harvester |
| June, maize, 2 acres, dry | Ridger: dig furrows from the water channel down the field (water then runs down the furrows you dug) | Maize planter | Maize harvester |
| Brian, maize, 1.5 acres | Disc harrow: break the clods into a fine seedbed | Maize planter, around a wet patch that slows you down | Maize harvester |
| Vincent, beans, 3 acres | Disc plough | Seed drill (beans need close rows) | Bean harvester |

**Every job starts with a short onboarding:**

1. **Briefing.** The farmer says what they need, with the task, the time limit, the field size and a warning about rocks and fallen trunks.
2. **Choose a tractor.** Compact (35 hp: cheap, light on the soil, slow and weak with heavy implements), Standard (60 hp: an all-rounder) or Large (100 hp: fast and strong, but wide turns, more diesel and heavier on the soil).
3. **Choose an implement** from eight: disc plough, disc harrow, ridger, maize planter, seed drill, boom sprayer, maize harvester and bean harvester. Nothing is pre-selected. You can pick the wrong one: it does a poor job (or none of it), and the summary explains what was needed.
4. **Ready check.** Hitch the implement and fill up with diesel (15 coins; the first fill is free). A reminder of the controls.
5. **Drive.** Every job has a time limit, and every field has rocks and fallen trunks to steer around. The sidebar shows how much is done, time left, fuel, overlap and hits, plus across the slope (ploughing and planting on a slope), along the rows and the grain tank (harvest). At harvest, unload at the trailer when the tank is full.
6. **Summary.** An overall score out of 100 with 0 to 3 stars, and four parts:
    - **Job done:** how much of the field got the right work, times how well the chosen implement does this job.
    - **Efficiency:** work done for the time used, and how little ground was covered twice.
    - **Climate:** diesel burned against the ideal for the work done (with the CO₂ in kg), minus soil packing from a heavy tractor, erosion from ploughing down the slope, and overlap.
    - **Cost saving:** the money saved against doing the same work by hand, in Kenyan shillings, with the person-days of hand work it replaced. A bad job can cost more than doing it by hand.
    - At harvest: bags gathered out of the farm's best possible, and their value.

**Getting there.** On the Home screen, the **Tractor** button above Map opens a job straight away: the nearest farm that still has stars to earn. It is dimmed until a farm's first stage is open (after your 2nd review of that farm). A farm with an open stage also shows a tractor button beside its label: tap it and the agent walks to the farm. The Task screen lists each farm's next stage, and the Support Farm screen (Map, then Support Farm) starts the selected farm's next stage. Planting opens once you have tried the before-planting job, and harvest once you have tried planting, however well they went.

**Driving.** Tap where to drive and hold to keep steering, or use the arrow keys / WASD. Slow turns tighter; Fast saves time but burns more diesel. Autopilot drives a planned route around the obstacles; autopilot jobs earn up to 2 stars.

**Rewards.** Coins (1.5 per score point), +5 farm score per star above your best, and gems the first time a stage gets 3 stars. A poor job never lowers the farm's score. June's furrows also count as her due watering task.

**Where the money figures come from.** Diesel is KSh 228 a litre (EPRA's Nairobi cap for 15 October to 14 November 2026, [Techish](https://tech-ish.com/2026/10/14/petrol-rises-to-kes-226-96-in-nairobi-and-kerosene-jumps-kes-28-49/)). Tractor ploughing is KSh 3,000 an acre and harrowing KSh 1,500 ([Beyond Forest, 2026](https://www.beyondforest.org/post/ploughing-cost-per-acre-in-kenya-2026-guide-virgin-vs-uncultivated-land-explained)). Hand ploughing takes about 24 person-days an acre at KSh 300 to 500 a day; the game uses KSh 400 ([FarmBiz Africa](https://farmbizafrica.com/tractors-services-increase-farmer-earnings-lower-production-costs/)). Maize yields 20 to 25 bags of 90 kg an acre at about KSh 4,500 a bag; the game uses 22 ([Graduate Farmer, 2025](https://graduatefarmer.co.ke/2025/05/06/how-to-grow-maize-in-kenya-step-by-step-for-maximum-profit/)). The rest are game estimates to check: hire rates for ridging (KSh 2,000), planting (KSh 2,000) and harvesting (KSh 3,000 to 3,500 an acre); hand-work days for harrowing (10), ridging (16), planting (6) and harvesting (10 to 12); diesel per acre for each implement; and beans at 7 bags an acre and KSh 9,000 a bag. CO₂ uses 2.68 kg per litre of diesel.

## How it is built

The game is a single `index.html` file with plain HTML, CSS and JavaScript. It has no framework and no build step.

- **Fixed stage.** Everything is laid out on an 874 × 402 landscape stage, matching the Figma frame, and scaled to fit the window. On an upright phone the stage turns sideways to fill the screen.
- **Drawn farm pictures.** The review pictures are drawn in code from each round's data (crop, problem, how visible it is, and which field), so a new round needs no new art. Real photos are laid on top where a good one exists.
- **Real photos.** Photos come from Wikimedia Commons and load straight from their servers. If one can't load, the drawn picture shows instead. Authors and licences are listed under Settings, Photo credits.
- **Roads.** The dirt roads on the home map are traced as a small graph of points, and the agent always takes the shortest route. Open the game with `?dev` to see the graph and print the coordinates of any tap.
- **Game clock and care.** Care plans are lists of tasks with time windows on the game clock. A timer checks every second for tasks that are due, missed or complete.
- **Saving.** Progress is saved in the browser's local storage on this device, under `wakala-save-v3`. Settings has a Restart button that clears it.
- **Tractor jobs.** Each farm's field, obstacles and three stage jobs are data, and so are the tractors and implements. The field is a grid of 2.5 px cells: the implement marks cells as it passes, and every score is counted from the grid. Autopilot follows a planned route that steps around obstacles, and takes a clear path to and from the trailer at harvest. Open the game with `?dev` to get `wakalaDebug` in the console (live state, and `wakalaDebug.open(farm, stage)`).
- **Compact pop-ups.** Every pop-up (review, zoom, care, hook, tractor job, Farms, Crop, Stats, Route) is a small centred panel (`.panel`, scaled with `--pz`, default .88) so the map and the agent stay visible behind it. Pop-ups tied to one farm start with a name plate (`fhead()`): farmer face, farm number, farmer's name, crop and acres. The Shop, Training, Storage, Task, Settings and Sell screens are not about one farm and have no plate.
- **Music and sound effects.** Everything is synthesised with the Web Audio API in the `SND` module, so there are no audio files. A soft looping pad-and-pluck tune plays in the background, and buttons, wrong taps, coins, unlocks and tractor hits each have their own short effect. Browsers only allow sound after a first tap or key press, so the audio starts then. The speaker button in the top corner and Settings, Sound mute and unmute it; the choice is saved under `wakala-sound`. Type `wakalaSound` in the console to inspect it (`on`, `state`, `play('coin')`).
- **Event log.** Key moments, such as the first move, each review, each care task and each tractor job, are logged with timings. Type `wakalaEvents()` in the browser console to read them during a playtest.

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

Settings has three playtest buttons: skip 2 game hours, unlock every tractor job, and unlock the new problems.

The automated playtests need `pip install playwright` and a Chromium browser. Set `CHROME=/path/to/chrome` to use your own.

```sh
python3 tools/playtest/fs.py right      # first session, right answers (HUMAN=1 for human pacing)
python3 tools/playtest/fs.py wrong      # first session with a wrong call and the retry
python3 tools/playtest/free.py          # road walking, tasks, spraying, misses, settings
python3 tools/playtest/rounds.py        # all 7 rounds on each farm, back to back
python3 tools/playtest/clicks.py        # click each farm on Home, Map and a hub map
python3 tools/playtest/tractor.py 1234 x # every farm's three stages through the onboarding on autopilot; x adds a wrong implement, a time-out, tap and key steering and the Home button
```

Screenshots are saved to `tools/playtest/out/`.

## Deployment

GitHub Pages publishes the `main` branch from the root folder. Every push to `main` goes live within about a minute, and there is no staging step. To review changes before players see them, work on a separate branch and merge it into `main` when it is approved.

## Open questions

- **Farm advice.** The product names are generic active ingredients (for example emamectin benzoate for armyworm, and lambda-cyhalothrin for bean pests). The bean product is a placeholder until an agronomist confirms it.
- **Care plans with fast rounds.** Care plans run on game days while rounds can be played back to back, so tasks can pile up during long sessions. One option is a single "fix it now" action within each round.
- **Missing photos.** Low nutrients and dry bean leaves still use the drawn pictures.
- **Reminders with the game closed** need a push service, which isn't built yet.
- **Hub maps** (after a storage upgrade) have no traced roads, so the agent walks straight to each farm there.
- **Tractor jobs.** The tractor and implement art is drawn in code until it is designed in Figma. The score weights, time limits and the money estimates listed above are first guesses for playtesting. Spraying is no longer a tractor job (it was Vincent's job before the season stages); the boom sprayer is still offered as an implement. The Farm 5 delivery job from the plan is not built.

## Credits

- Design: the 29 Oct Wakala Game Figma file (linked above).
- Photos: Wikimedia Commons contributors, under CC BY, CC BY-SA and CC0 licences. The full list with links is in the game under Settings, Photo credits. Photos are cropped and zoomed for the game.
