# Plays the first session, then all 7 rounds on every farm back to back. Farms have no ready timer,
# so each farm's rounds are played one after another without leaving it.
import asyncio, json, os, time
from playwright.async_api import async_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', '')+'rounds/'; os.makedirs(OUT,exist_ok=True)
R={2:[('water',1),('pest',2),('healthy',0),('water',0),('nutrient',3),('weeds',1),('pest',0)],
   3:[('water',2),('healthy',1),('pest',1),('water',3),('nutrient',0),('weeds',2),('nutrient',1)],
   4:[('pest',0),('water',3),('healthy',2),('pest',1),('nutrient',2),('weeds',3),('water',0)],
   1:[('pest',3),('water',0),('healthy',3),('pest',2),('weeds',1),('nutrient',3),('healthy',0)]}
SEV={(1,0):.45,(1,3):.55,(3,2):.6,(2,1):.7,(2,6):.35}
CROP={1:'maize',2:'maize',3:'maize',4:'beans'}
def rx(farm,n,prob):
  if prob=='water': return 'Water morning and evening'
  if prob=='pest':
    if CROP[farm]=='beans': return 'lambda-cyhalothrin'
    return 'Scout and crush' if SEV.get((farm,n),.5)<.5 else 'emamectin'
  return {'nutrient':'Add CAN beside','weeds':'Hoe the weeds out'}[prob]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**({'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}))
    pg=await b.new_page(viewport={'width':874,'height':402}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    n=[0]; snapped=[0]
    async def shot(name): n[0]+=1; await pg.locator('#stage').screenshot(path=f'{OUT}{n[0]:02d}-{name}.png')
    async def tap(x,y):
      box=await pg.locator('#stage').bounding_box(); await pg.mouse.click(box['x']+x*box['width']/874, box['y']+y*box['height']/402)
    async def S(): return await pg.evaluate("JSON.parse(localStorage.getItem('wakala-save-v3'))")
    async def waitrv():
      for i in range(200):
        if await pg.evaluate("!!document.querySelector('.rpanel .rsteps')"): return True
        await pg.wait_for_timeout(250)
      return False
    await pg.goto('file://' + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'index.html'))); await pg.wait_for_timeout(300)
    await pg.click('[data-n="Amani"]'); await pg.click('[data-act="createDone"]')
    async def walk(t):
      for i in range(60):
        await tap(*t); await pg.wait_for_timeout(500)
        if await pg.evaluate("!!document.querySelector('.rpanel')"): break
    async def review(prob, field, wrong=False, snap=None):
      for pt in ['crops','signs','land','layout']:
        await pg.click(f'.part[data-p="{pt}"]')
        if snap and pt=='signs': await shot(snap+'-zoom')
        await pg.click('.zoomfull .btn[data-act="unzoom"]')
      if prob=='healthy': await pg.click('[data-f="none"]')
      else: await pg.click(f'.fieldbtn[data-f="{field}"]')
      if snap: await shot(snap+'-judge')
      call = ('water' if prob!='water' else 'pest') if wrong else prob
      await pg.click(f'.call[data-c="{call}"]'); await pg.wait_for_timeout(150)
    await walk((630,226)); await shot('june-r1-look'); await review('water',1)
    await pg.click('[data-act="rvContinue"]'); await pg.click('.call:has-text("Water morning and evening")'); await pg.click('[data-act="startCare"]')
    await pg.locator('.holdbtn').focus()
    for i in range(3): await pg.keyboard.press('Space')
    await pg.click('[data-act="careContinue"]'); await pg.wait_for_timeout(2700)
    await walk((664,117)); await review('pest',0); await pg.click('[data-act="rvContinue"]')
    await pg.click('.call:has-text("lambda-cyhalothrin")'); await pg.click('.rpanel button[data-act="rvContinue"] >> nth=-1'); await shot('hook'); await pg.click('[data-act="hookDone"]')
    await pg.wait_for_timeout(400); await shot('free-home')
    t0=time.time(); played=0
    for farm in [1,3,2,4]:
      for _ in range(8):
        k=(await S())['rv'][str(farm)]['n']
        if k>=7: break
        prob,field=R[farm][k]
        t1=time.time()
        await pg.click(f'.flabel[data-farm="{farm}"]')
        ok=await waitrv()
        if not ok: print('stuck at', farm, k); await shot(f'stuck-{farm}-{k}'); break
        if k==0 and farm==1: await shot('mark-r1-look')
        if farm==1 and k==1: print('same farm again: review opened', round(time.time()-t1,1), 's after the click')
        if farm==2 and k==4: await shot('june-r5-look')
        snap = f'june-r{k+1}' if (farm==2 and k==4) else (f'brian-r{k+1}' if farm==3 and k==5 else None)
        wrong = (farm==3 and k==3)
        await review(prob, field, wrong=wrong, snap=snap)
        await pg.click('.rpanel [data-act="rvContinue"]')
        if not wrong and prob!='healthy':
          await pg.click(f'.call:has-text("{rx(farm,k,prob)}")')
          await pg.click('.rpanel button[data-act="rvContinue"] >> nth=-1')
        await pg.wait_for_timeout(200); played+=1
    await shot('all-done')
    s=await S()
    print('played',played,'rounds in',round(time.time()-t0),'s')
    print('n', {k:v['n'] for k,v in s['rv'].items()}, 'passed', s['passed'], 'coins', s['coins'], 'gems', s['gems'])
    print('routines', len(s['care']), [ (r['farm'],r['kind'],r['status']) for r in s['care']][-8:])
    ev=[e['e'] for e in await pg.evaluate("window.wakalaEvents()")]
    print('unlocked event', 'problems_unlocked' in ev, 'rounds_complete', ev.count('rounds_complete'))
    await pg.click('#btnTask'); await pg.wait_for_timeout(300); await shot('tasks')
    print('errors', errs); await b.close()
asyncio.run(main())
