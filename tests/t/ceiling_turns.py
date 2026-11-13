import asyncio,sys
from playwright.async_api import async_playwright
# press a turn button partway through a ceiling move; measure the biggest frame-to-frame jump (nearest drawn point),
# hips against the body ends, floor dips, errors, where it ends
SET="""()=>{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='%s';m.onchange()}"""
MEAS="""()=>{const P=[];for(const q of prims){if(q.t===2)continue;P.push([q.a[0]+POS[0],q.a[1],q.a[2]+POS[1]]);if(q.b&&q.b!==q.a)P.push([q.b[0]+POS[0],q.b[1],q.b[2]+POS[1]])}
 let worst=0;if(window.__p){for(const v of P){let m=1e9;for(const u of __p){const d=(v[0]-u[0])**2+(v[1]-u[1])**2+(v[2]-u[2])**2;if(d<m)m=d}if(m>worst)worst=m}}window.__p=P;
 let lo=1e9;for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a]))lo=Math.min(lo,v[1])}
 const caps=prims.filter(q=>q.nm==='Body'&&q.cap).map(q=>q.a);let att=0;const seen={};for(const q of prims){if(q.nm==='Body'||!q.cap||seen[q.nm])continue;seen[q.nm]=1;const v=q.a,D=u=>Math.hypot(v[0]-u[0],v[1]-u[1],v[2]-u[2]);att=Math.max(att,Math.min(D(caps[0]),D(caps[1])))}
 return [FLIP&&FLIP.kind,FLIP?+flipT().toFixed(2):1,+Math.sqrt(worst).toFixed(1),+lo.toFixed(1),+att.toFixed(0),!!TURNM,!!SPIN,GECKO,+(HEAD*180/Math.PI).toFixed(0)]}"""
async def main():
    url,mode,phase,btn,at=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5])
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script("try{localStorage.setItem('mixmoTier','anim')}catch(e){}")
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));await pg.goto(url);await pg.wait_for_timeout(300);await pg.evaluate(SET%mode);await pg.wait_for_timeout(900)
        if phase!="up":
            await pg.evaluate("$('tC').onclick()")
            while await pg.evaluate("!!FLIP"):await pg.wait_for_timeout(30)
            await pg.wait_for_timeout(300)
        await pg.click("#play");await pg.evaluate("window.__p=null")
        if phase!="hang":await pg.evaluate("$('tC').onclick()")
        rows=[];said=""
        for i in range(140):
            if i==at:
                await pg.evaluate(f"$('{btn}').onclick()")
                said=await pg.evaluate("(document.getElementById('status')||{}).textContent||''")
            rows.append(await pg.evaluate(MEAS))
            await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            if i>at+5 and not rows[-1][0] and not rows[-1][5] and not rows[-1][6] and phase!="hang":break
            if phase=="hang" and i>at+90:break
        top=sorted(rows[1:],key=lambda x:-x[2])[:3]
        low=min(rows,key=lambda x:x[3]);print("lowest at",rows.index(low),low[:3],low[5]);print(f"{mode:7s} {phase:5s} {btn} at frame {at} ({rows[at][0]} t {rows[at][1]}): turn ran {any(x[5] for x in rows[at:])} spin {any(x[6] for x in rows[at:])} | biggest steps {[(x[0],x[1],x[2]) for x in top]} | lowest {min(x[3] for x in rows)} | hips {max(x[4] for x in rows)} | ends gecko {rows[-1][7]} heading {rows[0][8]}->{rows[-1][8]} | errs {errs[:2]}")
        await b.close()
asyncio.run(main())
