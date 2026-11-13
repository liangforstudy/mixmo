import asyncio,sys
from playwright.async_api import async_playwright
# spin each way round: heading over time, where it stops, biggest frame-to-frame step of the drawn parts, errors
MEAS="""()=>{const P=[];for(const q of prims){if(q.t===2)continue;P.push([q.a[0]+POS[0],q.a[1],q.a[2]+POS[1]])}
 let worst=0;if(window.__p){for(const v of P){let m=1e9;for(const u of __p){const d=(v[0]-u[0])**2+(v[1]-u[1])**2+(v[2]-u[2])**2;if(d<m)m=d}if(m>worst)worst=m}}window.__p=P;
 return [+(HEAD*180/Math.PI).toFixed(1),!!SPIN,+Math.sqrt(worst).toFixed(1),+OMEGA.toFixed(2)]}"""
async def main():
    url=sys.argv[1]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        for ch,mode in [("robot","run6"),("robot","walk"),("robot","dino"),("sergal","walk"),("sergal2","walk")]:
            for d in (1,-1):
                pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script("try{localStorage.setItem('mixmoTier','anim')}catch(e){}")
                errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));await pg.goto(url);await pg.wait_for_timeout(300)
                await pg.evaluate(f"()=>{{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='{ch}';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange()}}")
                await pg.wait_for_timeout(1000);await pg.click("#play");await pg.evaluate("window.__p=null")
                await pg.evaluate(f"toggleSpin(false,{d})");rows=[]
                for i in range(200):
                    if i==60:await pg.evaluate("toggleSpin()")
                    rows.append(await pg.evaluate(MEAS))
                    if i>60 and not rows[-1][1]:break
                    await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
                hs=[x[0] for x in rows];top=max(x[2] for x in rows[1:])
                print(f"{ch:7s} {mode:5s} dir {d:+d}: heading {hs[0]} -> {hs[30]} -> stops at {hs[-1]} (square {abs(hs[-1]%90)<0.01 or abs(hs[-1]%90-90)<0.01}) | omega sign {set((x[3]>0)-(x[3]<0) for x in rows if x[1])} | biggest step {top} | errs {errs[:1]}")
                await pg.close()
        await b.close()
asyncio.run(main())
