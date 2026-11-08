import asyncio
from playwright.async_api import async_playwright
SP='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':500,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/Mixmo.html');await pg.wait_for_timeout(1500)
    await pg.evaluate("()=>{const s=document.getElementById('rendSw');}")
    await pg.select_option('#modeSel','idle');await pg.wait_for_timeout(300)
    for c in [0.3,0.33,0.4,0.55,0.75,1.0,1.3]:
      await pg.evaluate(f"()=>{{setCycle({c});yaw=2.4;}}");await pg.wait_for_timeout(900)
      n=await pg.evaluate("()=>prims.length");st=await pg.evaluate("()=>cycleStage()")
      await pg.screenshot(path=SP+f'stub_{c}.png',clip={'x':0,'y':0,'width':500,'height':420});print(c,n,st)
    print(errs);await b.close()
asyncio.run(main())
