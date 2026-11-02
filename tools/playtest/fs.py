# First-session playtest. Usage: python3 fs.py right|wrong [url]. HUMAN=1 adds human think times. Plays like a new player and screenshots each moment.
import asyncio, sys, json, time
from playwright.async_api import async_playwright
import os
MODE=sys.argv[1]; OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'fs-{MODE}', ''); os.makedirs(OUT,exist_ok=True)
HUMAN=os.environ.get('HUMAN')=='1'
async def think(pg, sec):
  if HUMAN: await pg.wait_for_timeout(int(sec*1000))
URL=sys.argv[2] if len(sys.argv)>2 else 'file://' + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'index.html'))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**({'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}))
    pg=await b.new_page(viewport={'width':874,'height':402}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    n=[0]
    async def shot(name):
      n[0]+=1; await pg.locator('#stage').screenshot(path=f'{OUT}{n[0]:02d}-{name}.png')
    async def tapstage(x,y):  # tap at stage coords
      box=await pg.locator('#stage').bounding_box(); await pg.mouse.click(box['x']+x*box['width']/874, box['y']+y*box['height']/402)
    await pg.goto(URL); await pg.wait_for_timeout(500); await shot('create')
    await think(pg,4); await pg.click('[data-n="Amani"]'); await think(pg,3); await pg.click('[data-l="boy"]'); await think(pg,2); await pg.wait_for_timeout(150); await shot('create-picked')
    await pg.click('[data-act="createDone"]'); await pg.wait_for_timeout(300); await shot('walk-start')
    async def walk(target):
      for i in range(40):
        await tapstage(*target); await pg.wait_for_timeout(600)
        await think(pg, 1.2 if i==0 else .3)
        if i==1: await shot('walking')
        if await pg.evaluate("!!document.querySelector('.rpanel')"): break
    await walk((630,226)); await pg.wait_for_timeout(300); await shot('review-look')
    async def review(call, hint=True):
      parts=['crops','signs','land','layout']
      for i,pt in enumerate(parts):
        await think(pg,2); await pg.click(f'.part[data-p="{pt}"]'); await pg.wait_for_timeout(200); await think(pg, 6 if hint else 4)
        if i in (0,1,2): await shot(f'zoom-{pt}')
        await pg.click('.zoomfull .btn[data-act="unzoom"]'); await pg.wait_for_timeout(150)
      await shot('spot')
      sc=await pg.evaluate("JSON.parse(localStorage.getItem('wakala-save-v3')).phase")
      # tap a wrong field first once to test feedback, then the right one
      field=await pg.evaluate("(()=>{const c=document.querySelectorAll('.fieldbtn');return c.length})()")
      return field
    await review('water')
    # find the problem field: we know from data -> read via the scene field
    async def spot_and_judge(field, call, wrongfirst=False):
      if wrongfirst:
        await think(pg,4); await pg.click(f'.fieldbtn[data-f="{(field+1)%4}"]'); await pg.wait_for_timeout(200); await shot('spot-wrong-field')
      await pg.click(f'.fieldbtn[data-f="{field}"]'); await pg.wait_for_timeout(200); await shot('judge')
      await think(pg,5); await pg.click(f'.call[data-c="{call}"]'); await pg.wait_for_timeout(2600); await shot('result')
    if MODE=='right':
      await spot_and_judge(1,'water',wrongfirst=True)
    else:
      await spot_and_judge(1,'pest')
      await think(pg,6); await pg.click('[data-act="rvContinue"]'); await pg.wait_for_timeout(300); await shot('retry-walk')
      await walk((226,192)); await pg.wait_for_timeout(300)
      await review('water'); await spot_and_judge(2,'water')
    await think(pg,3); await pg.click('[data-act="rvContinue"]'); await pg.wait_for_timeout(300); await shot('care-prescribe')
    await think(pg,5); await pg.click('.call:has-text("Spray an insecticide")'); await pg.wait_for_timeout(200); await shot('care-wrong')
    await think(pg,4); await pg.click('.call:has-text("Water morning and evening")'); await pg.wait_for_timeout(200); await shot('care-plan')
    await think(pg,3); await pg.click('[data-act="startCare"]'); await pg.wait_for_timeout(300); await shot('care-water')
    hb=await pg.locator('.holdbtn').bounding_box(); await pg.mouse.move(hb['x']+40,hb['y']+20); await pg.mouse.down(); await pg.wait_for_timeout(800); await shot('care-holding'); await pg.wait_for_timeout(1100); await pg.mouse.up(); await pg.wait_for_timeout(1900); await shot('care-done')
    await think(pg,2); await pg.click('[data-act="careContinue"]'); await pg.wait_for_timeout(700); await shot('unlock-0.7s')
    await pg.wait_for_timeout(1500); await shot('unlock-2.2s')
    await walk((664,117)); await pg.wait_for_timeout(300); await shot('review2-look')
    await review('pest', hint=False)
    await spot_and_judge(0,'pest')
    await pg.click('[data-act="rvContinue"]'); await pg.wait_for_timeout(300); await shot('care2-prescribe')
    await think(pg,5); await pg.click('.call:has-text("Water more")'); await pg.wait_for_timeout(200)
    await think(pg,3); await pg.click('.call:has-text("lambda-cyhalothrin")'); await pg.wait_for_timeout(200); await shot('care2-plan')
    await think(pg,2); await pg.click('.rpanel [data-act="rvContinue"]'); await pg.wait_for_timeout(400); await shot('hook')
    await pg.click('[data-act="hookDone"]'); await pg.wait_for_timeout(400); await shot('free-home')
    ev=await pg.evaluate("window.wakalaEvents()")
    print(json.dumps([[e['e'],e['sec']] + ([e.get('ok')] if 'ok' in e else []) for e in ev]))
    print('errors',errs); await b.close()
asyncio.run(main())
