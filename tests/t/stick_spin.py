import asyncio,math
from playwright.async_api import async_playwright
# Game mode on a touch phone: put a thumb down on the stick and circle it, each way round
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        for way in ("counter-clockwise","clockwise"):
            ctx=await b.new_context(viewport={"width":390,"height":844},has_touch=True,is_mobile=True)
            pg=await ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
            await pg.goto("http://localhost:8765/Mixmo.html");await pg.wait_for_timeout(800)
            await pg.evaluate("()=>{const s=document.getElementById('charSel');s.value='robot';s.onchange()}");await pg.wait_for_timeout(600)
            z=await pg.evaluate("(()=>{const r=document.getElementById('stickZone').getBoundingClientRect();return [r.left,r.top,r.width,r.height,getComputedStyle(document.getElementById('stickZone')).display]})()")
            cx,cy=z[0]+z[2]/2,z[1]+z[3]/2;cdp=await ctx.new_cdp_session(pg)
            async def tp(t,x,y):await cdp.send("Input.dispatchTouchEvent",{"type":t,"touchPoints":[] if t=="touchEnd" else [{"x":x,"y":y,"id":1}]})
            await tp("touchStart",cx,cy);await pg.wait_for_timeout(50)
            sg=1 if way=="counter-clockwise" else -1;spun=None
            for i in range(1,80):   # two and a bit turns; screen y points down, so counter-clockwise on screen is -angle in screen terms
                a=sg*i*2*math.pi/28;await tp("touchMove",cx+50*math.cos(a),cy-50*math.sin(a));await pg.wait_for_timeout(16)
                s=await pg.evaluate("SPIN&&SPIN.dir")
                if s and spun is None:spun=s
            h=await pg.evaluate("HEAD*180/Math.PI");await tp("touchEnd",0,0);await pg.wait_for_timeout(1500)
            print(f"stick circled {way}: zone shown {z[4]}, spin started way round {spun} (+1 = heading up), heading while circling {h:.0f}, after letting go: spinning {await pg.evaluate('!!SPIN')}, heading {await pg.evaluate('HEAD*180/Math.PI'):.0f} | errs {errs[:1]}")
            await ctx.close()
        await b.close()
asyncio.run(main())
