# Ceiling checks (2026-11-13). Usage: see the arguments in main(); serve this folder on port 8765 first.
import asyncio,sys,math
from playwright.async_api import async_playwright
# visual jump: for every drawn point this frame, distance to the nearest drawn point last frame (max over points),
# so swapping which limb is called what doesn't count, only shapes that really move
async def main():
    url=sys.argv[1];mode=sys.argv[2];kind=sys.argv[3]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":360,"height":700})
        await pg.goto(url);await pg.wait_for_timeout(400)
        await pg.evaluate(f"""()=>{{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange()}}""")
        await pg.wait_for_timeout(1300)
        if kind=="down":
            await pg.evaluate("$('tC').onclick()")
            while await pg.evaluate("!!FLIP"):await pg.wait_for_timeout(30)
            await pg.wait_for_timeout(800)
        await pg.click("#play");await pg.evaluate("$('tC').onclick()")
        await pg.evaluate("""()=>{window.__vis=[];window.__prev=null}""")
        rows=[]
        for i in range(130):
            r=await pg.evaluate("""()=>{const P=[];for(const q of prims){if(q.t===2)continue;P.push([q.a[0]+POS[0],q.a[1],q.a[2]+POS[1]]);if(q.b&&q.b!==q.a)P.push([q.b[0]+POS[0],q.b[1],q.b[2]+POS[1]])}
              let worst=0,at=null;if(__prev){for(const v of P){let m=1e9;for(const u of __prev){const d=(v[0]-u[0])**2+(v[1]-u[1])**2+(v[2]-u[2])**2;if(d<m)m=d}if(m>worst){worst=m;at=v}}}
              __prev=P;return [FLIP&&FLIP.kind,FLIP?+flipT().toFixed(3):1,Math.sqrt(worst),at&&at.map(x=>+x.toFixed(0))]}""")
            rows.append((i,)+tuple(r))
            if not r[0] and i>2:break
            await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        top=sorted(rows[1:],key=lambda x:-x[3])[:5]
        print(mode,kind,"frames",len(rows),"| biggest visual jumps (frame, t, size):",[(x[0],x[2],round(x[3],1)) for x in top])
        await b.close()
asyncio.run(main())
