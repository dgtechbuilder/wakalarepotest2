# Free-play test: road walking, tasks, spray with kit, misses, unlocks, settings.
import asyncio, json, os
from playwright.async_api import async_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', '')+'free/'; os.makedirs(OUT,exist_ok=True)
URL='file://' + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'index.html'))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**({'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}))
    pg=await b.new_page(viewport={'width':874,'height':402}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    n=[0]
    async def shot(name): n[0]+=1; await pg.locator('#stage').screenshot(path=f'{OUT}{n[0]:02d}-{name}.png')
    async def tap(x,y):
      box=await pg.locator('#stage').bounding_box(); await pg.mouse.click(box['x']+x*box['width']/874, box['y']+y*box['height']/402)
    async def S(): return await pg.evaluate("JSON.parse(localStorage.getItem('wakala-save-v3'))")
    # fast-forward through the first session with the fs flow
    await pg.goto(URL); await pg.wait_for_timeout(300)
    await pg.click('[data-n="Amani"]'); await pg.click('[data-act="createDone"]')
    async def walk(t):
      for i in range(60):
        await tap(*t); await pg.wait_for_timeout(500)
        if await pg.evaluate("!!document.querySelector('.rpanel')"): break
    async def review(field, call):
      for pt in ['crops','signs','land','layout']:
        await pg.click(f'.part[data-p="{pt}"]'); await pg.click('.zoomfull .btn[data-act="unzoom"]')
      if field is None: await pg.click('[data-f="none"]')
      else: await pg.click(f'.fieldbtn[data-f="{field}"]')
      await pg.click(f'.call[data-c="{call}"]'); await pg.wait_for_timeout(300)
    await walk((630,226)); await review(1,'water'); await pg.click('[data-act="rvContinue"]')
    await pg.click('.call:has-text("Water morning and evening")'); await pg.click('[data-act="startCare"]')
    await pg.locator('.holdbtn').focus(); 
    for i in range(3): await pg.keyboard.press('Space')
    await pg.wait_for_timeout(300); await pg.click('[data-act="careContinue"]'); await pg.wait_for_timeout(2700)
    await walk((664,117)); await review(0,'pest'); await pg.click('[data-act="rvContinue"]')
    await pg.click('.call:has-text("lambda-cyhalothrin")'); await pg.click('.rpanel [data-act="rvContinue"]'); await pg.click('[data-act="hookDone"]')
    await pg.wait_for_timeout(300); await shot('free-home')
    # tap-to-walk on roads
    await tap(470, 300); await pg.wait_for_timeout(200); await shot('walk-route'); await pg.wait_for_timeout(5000)
    s=await S(); print('pos after walk', s['pos'])
    await tap(120, 150); await pg.wait_for_timeout(300); await shot('walk-route2'); await pg.wait_for_timeout(1000)
    await tap(800, 150); await pg.wait_for_timeout(300); await shot('reroute'); await pg.wait_for_timeout(9000)
    print('pos after reroute', (await S())['pos'])
    # task screen
    await pg.click('#btnTask'); await pg.wait_for_timeout(300); await shot('tasks')
    # do the spray task: walk there, kit, product
    await pg.click('[data-act="doTask"]'); await pg.wait_for_timeout(300); await shot('walk-to-task')
    for i in range(40):
      await pg.wait_for_timeout(500)
      if await pg.evaluate("!!document.querySelector('.kit')"): break
    await shot('spray-kit')
    for k in ['gloves','mask','boots']: await pg.click(f'[data-k="{k}"]')
    await shot('spray-product'); await pg.click('[data-k="glyphosate"]'); await shot('spray-wrong'); await pg.click('[data-k="lambda"]')
    hb=await pg.locator('.holdbtn').bounding_box(); await pg.mouse.move(hb['x']+30,hb['y']+20); await pg.mouse.down(); await pg.wait_for_timeout(1900); await pg.mouse.up(); await pg.wait_for_timeout(1900)
    await shot('spray-done'); await pg.click('[data-act="careContinue"]'); await pg.wait_for_timeout(300)
    # skip time: evening water window passes (missed) -> task screen
    await pg.click('[data-v="settings"]'); await pg.wait_for_timeout(200); await shot('settings')
    await pg.click('[data-act="credits"]'); await pg.wait_for_timeout(200); await shot('credits'); await pg.click('[data-act="closeOverlay"]')
    for i in range(6): await pg.click('[data-act="skipTime"]')
    await pg.wait_for_timeout(200)
    await pg.click('[data-act="back"]'); await pg.click('#btnTask'); await pg.wait_for_timeout(300); await shot('tasks-after-skip')
    s=await S(); print('routines', [(r['farm'], r['status'], r['streak'], [x['st'] for x in r['steps']]) for r in s['care']])
    # unlock new problems and review all farms
    await pg.click('[data-act="back"]'); await pg.click('[data-v="settings"]'); await pg.click('[data-act="unlockNow"]')
    await pg.click('[data-act="back"]'); await pg.wait_for_timeout(300); await shot('home-unlocked')
    probs=await pg.evaluate("""(()=>{const s=JSON.parse(localStorage.getItem('wakala-save-v3'));return s.rv})()""")
    print('rv', json.dumps(probs)[:300])
    # review farm 1 (Mark) and screenshot the judge with 5 calls
    await pg.click('.flabel[data-farm="1"]')
    for i in range(40):
      await pg.wait_for_timeout(500)
      if await pg.evaluate("!!document.querySelector('.rpanel')"): break
    await shot('mark-look')
    for pt in ['crops','signs','land','layout']:
      await pg.click(f'.part[data-p="{pt}"]')
      if pt=='signs': await shot('mark-signs')
      await pg.click('.zoomfull .btn[data-act="unzoom"]')
    await shot('mark-spot')
    print('errors', errs); await b.close()
asyncio.run(main())
