import asyncio,sys
from playwright.async_api import async_playwright
# Run on six: press 180 twice; per frame the two body end heights (named by the end they are: front = the travel
# direction), and the lowest point
async def main():
    url,mode,spd=sys.argv[1],sys.argv[2],sys.argv[3]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script("try{localStorage.setItem('mixmoTier','anim')}catch(e){}")
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));await pg.goto(url);await pg.wait_for_timeout(300)
        await pg.evaluate(f"""()=>{{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange()}}""")
        await pg.wait_for_timeout(1200);await pg.click("#play")
        for k in range(2):
            await pg.evaluate("$('tU').onclick()");rows=[]
            for i in range(80):
                r=await pg.evaluate("""()=>{const caps=prims.filter(q=>q.nm==='Body'&&q.cap).map(q=>q.a);
                 // which cap is ahead in the travel direction: local +z is T; travel is along DIR (+1 = T leads)
                 const zT=caps[0][2]>caps[1][2]?0:1,front=DIR>=0?zT:1-zT;let lo=1e9,ln='';for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a]))if(v[1]<lo){lo=v[1];ln=q.nm}}
                 return [TURNM?+((phase-TURNM.p0)/TURNM.len).toFixed(2):null,TURNM?TURNM.d0:null,+DIR.toFixed(2),+caps[zT][1].toFixed(1),+caps[1-zT][1].toFixed(1),+lo.toFixed(1),ln,+SKIDLEAN.toFixed(1),SWAP]}""")
                rows.append(r)
                if r[0] is None and i>3:break
                await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            d0=rows[1][1];tt=[x for x in rows if x[0] is not None]
            dipT=min(tt,key=lambda x:x[3]);dipB=min(tt,key=lambda x:x[4]);low=min(tt,key=lambda x:x[5])
            print(f"turn {k+1}: d0 {d0} start T-end {rows[0][3]} B-end {rows[0][4]} | lowest T-end {dipT[3]} at t {dipT[0]}, lowest B-end {dipB[4]} at t {dipB[0]} | skid lean range {min(x[7] for x in tt)}..{max(x[7] for x in tt)} | lowest point {low[5]} ({low[6]}) at t {low[0]} | errs {errs}")
            for _ in range(25):await pg.evaluate("hStep(1)")
        await b.close()
asyncio.run(main())
