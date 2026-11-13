import asyncio,sys
from playwright.async_api import async_playwright
SET="""()=>{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='%s';m.onchange()}"""
async def main():
    url=sys.argv[1]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        async def page(mode):
            pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script("try{localStorage.setItem('mixmoTier','anim')}catch(e){}")
            errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));await pg.goto(url);await pg.wait_for_timeout(300);await pg.evaluate(SET%mode);await pg.wait_for_timeout(900);return pg,errs
        async def run(pg,n):
            out=[]
            for i in range(n):
                out.append(await pg.evaluate("[FLIP&&FLIP.kind,FLIP?+flipT().toFixed(2):1,+CAMY.toFixed(0),GECKO,$('tC').textContent]"))
                await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            return out
        # camera through up, hang, cat drop
        for mode in ["run6","walk"]:
            pg,errs=await page(mode);await pg.click("#play");await pg.evaluate("$('tC').onclick()")
            r=await run(pg,60);await pg.evaluate("$('tC').onclick()");r+=await run(pg,64)
            cam=[x[2] for x in r];steps=[abs(cam[i]-cam[i-1]) for i in range(1,len(cam))]
            print(mode,"camera",cam[0],"->",max(cam),"->",cam[-1],"biggest change a frame",max(steps),"errs",errs)
            print("  ",[(x[0],x[1],x[2]) for x in r[::8]])
            await pg.close()
        # out of reach: camera rises a little and comes back
        pg,errs=await page("walk");await pg.evaluate("()=>{const c=$('ceilH');c.value=600;c.oninput&&c.oninput();c.onchange&&c.onchange()}");await pg.click("#play");await pg.evaluate("$('tC').onclick()")
        r=await run(pg,50);cam=[x[2] for x in r];print("out of reach",[x[0] for x in r[:3]],"camera",cam[0],"max",max(cam),"end",cam[-1],errs);await pg.close()
        # queue: three presses: up, down, up
        pg,errs=await page("run6");await pg.click("#play")
        for i in range(3):await pg.evaluate("$('tC').onclick()")
        lab=await pg.evaluate("$('tC').textContent")
        r=await run(pg,220);seq=[];
        for x in r:
            if x[0] and (not seq or seq[-1]!=x[0]):seq.append(x[0])
        print("queue label after 3 presses:",lab,"| moves:",seq,"| ends on ceiling:",r[-1][3],"label",r[-1][4],errs)
        await b.close()
asyncio.run(main())
