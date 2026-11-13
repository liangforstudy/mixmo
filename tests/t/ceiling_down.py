import asyncio,sys
from playwright.async_api import async_playwright
# ceiling down with a chosen way (cat/swing/float): per frame visual jump, lowest drawn point, body height
async def main():
    url,mode,w=sys.argv[1],sys.argv[2],sys.argv[3];dd=sys.argv[4] if len(sys.argv)>4 else 'flip';rl=sys.argv[5] if len(sys.argv)>5 else 'yes';verbose=len(sys.argv)>6
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":360,"height":700})
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto(url);await pg.wait_for_timeout(400)
        await pg.evaluate(f"""()=>{{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange();document.querySelector('#ceilTurn [data-c={__import__('os').environ.get('TURN','flip')}]').click();document.querySelector('#ceilDown [data-w={w}]').click();const q=document.querySelector('#ceilDrop [data-d={dd}]');if(q)q.click();const r=document.querySelector('#ceilRoll [data-r="{rl}"]');if(r)r.click()}}""")
        await pg.wait_for_timeout(1300)
        await pg.evaluate("$('tC').onclick()")
        while await pg.evaluate("!!FLIP"):await pg.wait_for_timeout(30)
        await pg.wait_for_timeout(800)
        g=await pg.evaluate("GECKO")
        await pg.click("#play");await pg.evaluate("$('tC').onclick()");await pg.evaluate("window.__prev=null")
        rows=[];lab=await pg.evaluate("FLIP&&[FLIP.kind,!!FLIP.cat,!!FLIP.jump]")
        for i in range(160):
            r=await pg.evaluate("""()=>{const P=[];let lo=1e9,nm='';for(const q of prims){if(q.t===2)continue;P.push([q.a[0]+POS[0],q.a[1],q.a[2]+POS[1],q.nm]);if(q.b&&q.b!==q.a)P.push([q.b[0]+POS[0],q.b[1],q.b[2]+POS[1]]);for(const v of (q.pts||[q.a])){if(v[1]<lo){lo=v[1];nm=q.nm}}}
              let worst=0,wn='';if(__prev){for(const v of P){let m=1e9;for(const u of __prev){const d=(v[0]-u[0])**2+(v[1]-u[1])**2+(v[2]-u[2])**2;if(d<m)m=d}if(m>worst){worst=m;wn=v[3]}}}
              __prev=P;return [FLIP&&FLIP.kind,FLIP?+flipT().toFixed(3):1,+Math.sqrt(worst).toFixed(1),+lo.toFixed(1),nm,+LASTMID[1].toFixed(1),+SPR.y.toFixed(1),wn]}""")
            rows.append((i,)+tuple(r))
            if not r[0] and i>2:
                if len(rows)>i and i>=rows[0][0]+3: 
                    # a few more frames after exit
                    pass
            if not r[0] and i>2 and all(not x[1] for x in rows[-6:]):break
            await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        g2=await pg.evaluate("GECKO")
        top=sorted(rows[1:],key=lambda x:-x[3])[:4]
        dips=[(x[0],x[4],x[5]) for x in rows if x[4]<-0.5]
        print(f"{mode:8s} {w:5s} gecko {g}->{g2} {lab} frames {len(rows)} jumps {[(x[0],x[2],x[3]) for x in top]} dips {dips[:6]}{'...' if len(dips)>6 else ''} errs {errs[:2]}")
        if verbose:
            for x in rows:print(x)
        await b.close()
asyncio.run(main())
