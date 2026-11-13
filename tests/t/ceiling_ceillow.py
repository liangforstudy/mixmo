# Ceiling checks (2026-11-13). Usage: see the arguments in main(); serve this folder on port 8765 first.
import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    url,mode,kind=sys.argv[1],sys.argv[2],sys.argv[3]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script("try{if(!localStorage.getItem('mixmoTier'))localStorage.setItem('mixmoTier','anim')}catch(e){}")
        await pg.goto(url);await pg.wait_for_timeout(400)
        await pg.evaluate(f"""()=>{{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange()}}""")
        await pg.wait_for_timeout(1300)
        if kind=="down":
            await pg.evaluate("$('tC').onclick()")
            while await pg.evaluate("!!FLIP"):await pg.wait_for_timeout(30)
            await pg.wait_for_timeout(800)
        await pg.click("#play");await pg.evaluate("$('tC').onclick()");out=[]
        for i in range(80):
            r=await pg.evaluate("""()=>{let lo=1e9,nm='';for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a])){if(v[1]<lo){lo=v[1];nm=q.nm}}}return [FLIP&&FLIP.kind,FLIP?+flipT().toFixed(2):1,+lo.toFixed(1),nm]}""")
            if r[2]<0:out.append((r[1],r[2],r[3]))
            if not r[0] and i>2:break
            await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        print(url.split('/')[-1],mode,kind,"frames below the floor:",out)
        await b.close()
asyncio.run(main())
