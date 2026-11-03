# Tractor season: plays the first session, unlocks the tractor jobs, then plays each farm's stages
# (before planting, planting, harvest) through the onboarding: briefing, tractor, implement, ready check, drive, summary.
# Usage: python3 tools/playtest/tractor.py [farms] [extras]   e.g. "1234" (default) and "x" to also test a wrong
# implement, a timed-out job, the Home tractor button and steering by tapping and keys.
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'tractor', ''); os.makedirs(OUT, exist_ok=True)
URL='file://' + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'index.html'))
FARMS_=[int(c) for c in (sys.argv[1] if len(sys.argv) > 1 else '1234')]
EXTRAS='x' in (sys.argv[2] if len(sys.argv) > 2 else '')
RIGHT={1:['plough','planter','maizeH'], 2:['ridger','planter','maizeH'], 3:['harrow','planter','maizeH'], 4:['plough','drill','beanH']}
TRACTOR={1:'standard', 2:'compact', 3:'standard', 4:'large'}
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**({'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}))
    pg=await b.new_page(viewport={'width':874,'height':402}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    n=[0]
    async def shot(name): n[0]+=1; await pg.locator('#stage').screenshot(path=f'{OUT}{n[0]:02d}-{name}.png')
    async def tap(x,y):
      box=await pg.locator('#stage').bounding_box(); await pg.mouse.click(box['x']+x*box['width']/874, box['y']+y*box['height']/402)
    async def S(): return await pg.evaluate("JSON.parse(localStorage.getItem('wakala-save-v3'))")
    async def side(): return await pg.evaluate("document.querySelector('.tside').innerText.replace(/\\n+/g,' | ')")
    await pg.goto(URL); await pg.wait_for_timeout(300)
    await pg.click('[data-n="Amani"]'); await pg.click('[data-act="createDone"]')
    async def walk(t):
      for i in range(150):
        await tap(*t); await pg.wait_for_timeout(300)
        if await pg.evaluate("!!document.querySelector('.rpanel')"): break
    async def review(prob, field):
      for pt in ['crops','signs','land','layout']:
        await pg.click(f'.part[data-p="{pt}"]'); await pg.click('.zoomfull .btn[data-act="unzoom"]')
      await pg.click(f'.fieldbtn[data-f="{field}"]'); await pg.click(f'.call[data-c="{prob}"]'); await pg.wait_for_timeout(150)
    await walk((630,226)); await review('water',1)
    await pg.click('[data-act="rvContinue"]'); await pg.click('.call:has-text("Water morning and evening")'); await pg.click('[data-act="startCare"]')
    await pg.locator('.holdbtn').focus()
    for i in range(3): await pg.keyboard.press('Space')
    await pg.click('[data-act="careContinue"]'); await pg.wait_for_timeout(2700)
    await walk((664,117)); await review('pest',0); await pg.click('[data-act="rvContinue"]')
    await pg.click('.call:has-text("lambda-cyhalothrin")'); await pg.click('.rpanel button[data-act="rvContinue"] >> nth=-1'); await pg.click('[data-act="hookDone"]')
    await pg.wait_for_timeout(300)
    await pg.click('[data-v="settings"]'); await pg.click('[data-act="unlockJobs"]'); await pg.click('[data-act="back"]'); await pg.wait_for_timeout(300); await shot('home-badges')
    async def wait_for(sel, secs=40):
      for i in range(secs*4):
        if await pg.evaluate(f"!!document.querySelector({json.dumps(sel)})"): return True
        await pg.wait_for_timeout(250)
      return False
    async def onboard(farm, stage, tractor, impl, snap=False):
      assert await wait_for('#tcv'), 'job did not open'
      assert await pg.evaluate("document.querySelector('.tsteps b').textContent") == 'Brief', 'job did not start with the briefing'
      if snap: await shot(f'f{farm}s{stage}-brief')
      await pg.click('[data-act="jobStep"][data-p="tractor"]')
      await pg.click('[data-act="jobStep"][data-p="implement"]')   # not allowed yet: nothing picked
      assert await pg.evaluate("document.querySelector('.tsteps b').textContent") == 'Tractor', 'moved on without a tractor'
      await pg.click(f'[data-act="pickTractor"][data-k="{tractor}"]')
      if snap: await shot(f'f{farm}s{stage}-tractor')
      await pg.click('[data-act="jobStep"][data-p="implement"]')
      await pg.click('[data-act="jobStep"][data-p="ready"]')       # not allowed yet: nothing picked
      assert await pg.evaluate("document.querySelector('.tsteps b').textContent") == 'Implement', 'moved on without an implement'
      await pg.click(f'[data-act="pickImpl"][data-k="{impl}"]')
      if snap: await shot(f'f{farm}s{stage}-implement')
      await pg.click('[data-act="jobStep"][data-p="ready"]')
      await pg.click('[data-act="jobCheck"][data-k="hitch"]'); await pg.click('[data-act="jobCheck"][data-k="fuel"]')
      if snap: await shot(f'f{farm}s{stage}-ready')
      await pg.click('[data-act="jobGo"]')
    async def leave():
      btn=pg.locator('.tside [data-act="jobBack"]')
      if await btn.count(): await btn.click()
      else: await pg.click('.tside [data-act="jobRetry"]'); await pg.click('[data-act="jobBack"]')
      await pg.wait_for_timeout(300)
    results=[]
    for farm in FARMS_:
      for stage in [1,2,3]:
        if stage==1: await pg.click(f'.tbadge[data-farm="{farm}"]')
        else: await pg.click('.tside [data-act="jobNext"]')
        await onboard(farm, stage, TRACTOR[farm], RIGHT[farm][stage-1], snap=(farm==FARMS_[0]))
        await pg.click('[data-act="jobAuto"]'); t0=time.time()
        await pg.wait_for_timeout(5000); await shot(f'f{farm}s{stage}-driving')
        assert await wait_for('.tbig', 200), 'job never finished'
        await pg.wait_for_timeout(1500); await shot(f'f{farm}s{stage}-summary')
        results.append((farm, stage, TRACTOR[farm], RIGHT[farm][stage-1], round(time.time()-t0), (await side())[:330]))
      await leave()
    for r in results: print('job', r)
    if EXTRAS:
      # a wrong implement: allowed, scores badly, and the next stage still opens
      farm=FARMS_[0]; await pg.click('#btnTask'); await pg.click(f'.trow [data-act="tractorFarm"][data-farm="{farm}"]')
      await onboard(farm, 1, 'large', 'sprayer'); await pg.click('[data-act="jobAuto"]')
      assert await wait_for('.tbig', 200); await pg.wait_for_timeout(500); await shot('wrong-implement-summary')
      print('wrong implement:', (await side())[:330]); await leave()
      # running out of time
      await pg.click(f'.tbadge[data-farm="{farm}"]'); await onboard(farm, 1, 'compact', 'plough')
      assert await wait_for('.tbig', 200); await shot('timeout-summary'); print('time out:', (await side())[:200]); await leave()
      # steering by tapping and with the keys
      await pg.click(f'.tbadge[data-farm="{farm}"]'); await onboard(farm, 1, 'standard', RIGHT[farm][0])
      box=await pg.locator('#tcv').bounding_box()
      async def ctap(x,y): await pg.mouse.click(box['x']+x*box['width']/580, box['y']+y*box['height']/370)
      for y in [81,101,121]:
        for x in ([450,110] if y==101 else [110,450]): await ctap(x, y); await pg.wait_for_timeout(4500)
      tapped=await pg.evaluate("document.getElementById('tCov').textContent")
      await pg.keyboard.down('ArrowUp'); await pg.keyboard.down('ArrowLeft'); await pg.wait_for_timeout(800); await pg.keyboard.up('ArrowLeft'); await pg.wait_for_timeout(1000); await pg.keyboard.up('ArrowUp')
      await pg.click('[data-act="jobFinish"]'); await pg.wait_for_timeout(300); await shot('manual-summary')
      print('manual: covered', tapped, 'after three tapped rows |', (await side())[:200]); await leave()
      # the Home tractor button opens a job straight away, and Back leaves the agent where it was
      assert await pg.evaluate("(()=>{const b=document.querySelector('#btnTractor');return !b.hidden && !b.classList.contains('dim')})()"), 'Home tractor button is hidden or dimmed'
      pos0=(await S())['pos']; await pg.click('#btnTractor'); assert await wait_for('#tcv', 5), 'Home tractor button did not open a job'
      await pg.click('[data-act="jobBack"]'); await pg.wait_for_timeout(300)
      assert (await S())['pos']==pos0, 'Back from a Home-button job moved the agent'; print('home tractor button: ok')
    s=await S(); t=s['tractor']; print('stage stars', t['best'], '| scores', t['score'], '| saved KSh', round(t['saved']), '| CO2 kg', round(t['co2']))
    ev=[e['e'] for e in await pg.evaluate("window.wakalaEvents()")]
    print('events', {k: ev.count(k) for k in ['tractor_open','tractor_pick','tractor_implement','tractor_drive','tractor_done','tractor_hit']})
    await pg.click('#btnTask'); await pg.wait_for_timeout(200); await shot('tasks')
    print('errors', errs); await b.close()
asyncio.run(main())
