# After the first session: click each farm (not its label) on Home and on Map, check the agent walks there and the review opens.
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'clicks', ''); os.makedirs(OUT, exist_ok=True)
URL=sys.argv[1] if len(sys.argv)>1 else 'file://' + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'index.html'))
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
BOX={1:[105,0,370,142],2:[598,200,874,382],3:[99,196,377,362],4:[565,0,775,122]}
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
      for i in range(60):
        await tap(*t); await pg.wait_for_timeout(400)
        if await pg.evaluate("!!document.querySelector('.rpanel')"): break
    async def review(prob, field):
      for pt in ['crops','signs','land','layout']:
        await pg.click(f'.part[data-p="{pt}"]'); await pg.click('.zoomfull .btn[data-act="unzoom"]')
      if prob=='healthy': await pg.click('[data-f="none"]')
      else: await pg.click(f'.fieldbtn[data-f="{field}"]')
      await pg.click(f'.call[data-c="{prob}"]'); await pg.wait_for_timeout(150)
    await walk((630,226)); await review('water',1)
    await pg.click('[data-act="rvContinue"]'); await pg.click('.call:has-text("Water morning and evening")'); await pg.click('[data-act="startCare"]')
    await pg.locator('.holdbtn').focus()
    for i in range(3): await pg.keyboard.press('Space')
    await pg.click('[data-act="careContinue"]'); await pg.wait_for_timeout(2700)
    await walk((664,117)); await review('pest',0); await pg.click('[data-act="rvContinue"]')
    await pg.click('.call:has-text("lambda-cyhalothrin")'); await pg.click('.rpanel button[data-act="rvContinue"] >> nth=-1'); await pg.click('[data-act="hookDone"]')
    await pg.wait_for_timeout(300)
    results=[]
    async def tryfarm(farm, where, x, y):
      t0=time.time(); await tap(x,y); await pg.wait_for_timeout(250)
      walking=await pg.evaluate("!!document.querySelector('#me') && !!document.querySelector('.wpath')")
      await shot(f'{where}-farm{farm}-click')
      opened=False
      for i in range(160):
        if await pg.evaluate("!!document.querySelector('.rpanel .rsteps')"): opened=True; break
        await pg.wait_for_timeout(250)
      await shot(f'{where}-farm{farm}-after')
      s=await S(); results.append((where, farm, 'walk' if walking else 'NO WALK', 'review' if opened else 'NO REVIEW', round(time.time()-t0,1), s['pos']))
      if opened:
        k=s['rv'][str(farm)]['n']; prob,field=R[farm][k]
        for pt in ['crops','signs','land','layout']:
          await pg.click(f'.part[data-p="{pt}"]'); await pg.click('.zoomfull .btn[data-act="unzoom"]')
        if prob=='healthy': await pg.click('[data-f="none"]')
        else: await pg.click(f'.fieldbtn[data-f="{field}"]')
        await pg.click(f'.call[data-c="{prob}"]'); await pg.wait_for_timeout(150)
        await pg.click('.rpanel [data-act="rvContinue"]')
        if prob!='healthy':
          await pg.click(f'.call:has-text("{rx(farm,k,prob)}")'); await pg.click('.rpanel button[data-act="rvContinue"] >> nth=-1')
        await pg.wait_for_timeout(300)
    for f in [3,1,2,4]:
      bx=BOX[f]; await tryfarm(f,'home',(bx[0]+bx[2])/2+40,(bx[1]+bx[3])/2+25)
    for f in [3,1,2,4]:
      await pg.click('#btnMap'); await pg.wait_for_timeout(300)
      bx=BOX[f]; await tryfarm(f,'map',(bx[0]+bx[2])/2+40,(bx[1]+bx[3])/2+25)
    # upgraded hub map: farms sit elsewhere
    await pg.click('[data-v="storage"]'); await pg.wait_for_timeout(200)
    await pg.click('[data-act="upgrade"]'); await pg.wait_for_timeout(200)
    await pg.click('[data-v="home"]'); await pg.wait_for_timeout(300); await shot('hub-home')
    HUBB={1:[60,20,360,180],2:[535,240,820,402],3:[45,240,330,402],4:[540,20,815,165]}
    for f in [3,2]:
      bx=HUBB[f]; await tryfarm(f,'hub',(bx[0]+bx[2])/2+30,(bx[1]+bx[3])/2+30)
    for r in results: print(r)
    print('errors',errs); await b.close()
asyncio.run(main())
