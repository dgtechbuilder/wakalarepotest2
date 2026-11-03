# Tractor jobs: plays the first session, unlocks the jobs in Settings, then drives every farm's job.
# Usage: python3 tools/playtest/tractor.py [levels]   (levels default "1"; e.g. "123" for all three)
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'tractor', ''); os.makedirs(OUT, exist_ok=True)
URL='file://' + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'index.html'))
LEVELS=[int(c) for c in (sys.argv[1] if len(sys.argv) > 1 else '1')]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**({'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}))
    pg=await b.new_page(viewport={'width':874,'height':402}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    n=[0]
    async def shot(name): n[0]+=1; await pg.locator('#stage').screenshot(path=f'{OUT}{n[0]:02d}-{name}.png')
    async def tap(x,y):
      box=await pg.locator('#stage').bounding_box(); await pg.mouse.click(box['x']+x*box['width']/874, box['y']+y*box['height']/402)
    async def S(): return await pg.evaluate("JSON.parse(localStorage.getItem('wakala-save-v3'))")
    await pg.goto(URL); await pg.wait_for_timeout(300)
    await pg.click('[data-n="Amani"]'); await pg.click('[data-act="createDone"]')
    async def walk(t):
      for i in range(150):
        await tap(*t); await pg.wait_for_timeout(400)
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
    await pg.wait_for_timeout(300); await shot('home-no-badges')
    # unlock for testing
    await pg.click('[data-v="settings"]'); await pg.click('[data-act="unlockJobs"]'); await pg.click('[data-act="back"]'); await pg.wait_for_timeout(300); await shot('home-badges')
    # the Home tractor button (above Map) opens a job straight away, and Back leaves the agent where it was
    assert await pg.evaluate("(()=>{const b=document.querySelector('#btnTractor');return !b.hidden && !b.classList.contains('dim')})()"), 'Home tractor button is hidden or dimmed'
    pos0=(await S())['pos']
    await pg.click('#btnTractor')
    for i in range(20):
      if await pg.evaluate("!!document.querySelector('#tcv')"): break
      await pg.wait_for_timeout(250)
    assert await pg.evaluate("!!document.querySelector('#tcv')"), 'Home tractor button did not open a job'
    await shot('home-button-job'); await pg.click('[data-act="jobBack"]'); await pg.wait_for_timeout(300)
    assert (await S())['pos']==pos0, 'Back from a Home-button job moved the agent'
    print('home tractor button: ok')
    results=[]
    async def until_done(limit=150):
      for i in range(limit*4):
        if await pg.evaluate("!!document.querySelector('.tstars')"): return True
        await pg.wait_for_timeout(250)
      return False
    async def prep(farm, level, via):
      if via=='badge':
        await pg.click(f'.tbadge[data-farm="{farm}"]')
      else:
        await pg.click('#btnTask'); await pg.wait_for_timeout(200); await pg.click(f'.trow [data-act="tractorFarm"][data-farm="{farm}"]')
      for i in range(80):
        if await pg.evaluate("!!document.querySelector('#tcv')"): break
        await pg.wait_for_timeout(250)
      if level>1: await pg.click(f'.lvl[data-l="{level}"]')
      await pg.wait_for_timeout(150)
    for farm in [1,2,3,4]:
      for level in LEVELS:
        await prep(farm, level, 'badge' if farm%2 else 'task')
        await shot(f'farm{farm}-L{level}-card')
        await pg.click('[data-act="jobReady"]'); await pg.wait_for_timeout(100); await shot(f'farm{farm}-L{level}-check')
        for k in await pg.evaluate("[...document.querySelectorAll('[data-act=jobCheck]')].map(b=>b.dataset.k)"):
          await pg.click(f'[data-act="jobCheck"][data-k="{k}"]')
        await pg.click('[data-act="jobGo"]'); await pg.click('[data-act="jobAuto"]'); t0=time.time()
        await pg.wait_for_timeout(6000); await shot(f'farm{farm}-L{level}-driving')
        ok=await until_done(); await pg.wait_for_timeout(1600); await shot(f'farm{farm}-L{level}-done')
        txt=await pg.evaluate("document.querySelector('.tside').innerText.replace(/\\n+/g,' | ')")
        stars=await pg.evaluate("document.querySelectorAll('.tstars .on').length")
        results.append((farm, level, stars, round(time.time()-t0), txt[:230]))
        btn=pg.locator('.tside [data-act="jobBack"]')
        if await btn.count(): await btn.click()
        else:
          await pg.click('.tside [data-act="jobRetry"]'); await pg.click('[data-act="jobBack"]')
        await pg.wait_for_timeout(300)
    for r in results: print('autopilot', r)
    # manual driving on Mark's level 1: taps along the rows, then the arrow keys
    await prep(1, 1, 'badge'); await pg.click('.lvl[data-l="1"]'); await pg.click('[data-act="jobReady"]')
    for k in await pg.evaluate("[...document.querySelectorAll('[data-act=jobCheck]')].map(b=>b.dataset.k)"): await pg.click(f'[data-act="jobCheck"][data-k="{k}"]')
    await pg.click('[data-act="jobGo"]')
    box=await pg.locator('#tcv').bounding_box()
    async def ctap(x,y):  # canvas coords
      await pg.mouse.click(box['x']+x*box['width']/580, box['y']+y*box['height']/370)
    before=await pg.evaluate("document.getElementById('tCov').textContent")
    for y in [111,131,151,171,191,211,231,251]:
      for x in ([430,150] if y in (131,171,211,251) else [150,430]):
        await ctap(x, y); await pg.wait_for_timeout(4200)
    await shot('manual-taps')
    mid=await pg.evaluate("document.getElementById('tCov').textContent")
    await pg.keyboard.down('ArrowUp'); await pg.keyboard.down('ArrowLeft'); await pg.wait_for_timeout(900); await pg.keyboard.up('ArrowLeft'); await pg.wait_for_timeout(1200); await pg.keyboard.up('ArrowUp')
    await shot('manual-keys')
    await pg.click('[data-act="jobFinish"]'); await pg.wait_for_timeout(300); await shot('manual-done')
    print('manual: done', before, '->', mid, '| result:', await pg.evaluate("document.querySelector('.tside').innerText.replace(/\\n+/g,' | ').slice(0,200)"))
    btn=pg.locator('.tside [data-act="jobBack"]')
    if await btn.count(): await btn.click()
    else: await pg.click('.tside [data-act="jobRetry"]'); await pg.click('[data-act="jobBack"]')
    await pg.wait_for_timeout(200)
    s=await S(); print('best stars', s['tractor']['best'], 'coins', s['coins'])
    ev=[e['e'] for e in await pg.evaluate("window.wakalaEvents()")]
    print('events', {k: ev.count(k) for k in ['tractor_open','tractor_drive','tractor_done','tractor_hit']})
    await pg.click('#btnTask'); await pg.wait_for_timeout(200); await shot('tasks')
    print('errors', errs); await b.close()
asyncio.run(main())
