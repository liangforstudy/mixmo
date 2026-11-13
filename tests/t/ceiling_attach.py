import asyncio,sys
from playwright.async_api import async_playwright
# per frame: body axis (the two end caps), each limb's root (first cap) and how far it is from the nearest body end,
# and the body's tilt from level. Phases: up (from the floor) or down (from the ceiling).
async def main():
    url,mode,phase,w,d=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5];verb=len(sys.argv)>6
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script("try{if(!localStorage.getItem('mixmoTier'))localStorage.setItem('mixmoTier','anim')}catch(e){}")
        await pg.goto(url);await pg.wait_for_timeout(400)
        await pg.evaluate(f"""()=>{{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange();const ct=document.querySelector('#ceilTurn [data-c={__import__('os').environ.get('TURN','flip')}]');if(ct)ct.click();const cw=document.querySelector('#ceilDown [data-w={w}]');if(cw)cw.click();const q=document.querySelector('#ceilDrop [data-d={d}]');if(q)q.click()}}""")
        await pg.wait_for_timeout(1300)
        if phase=="down":
            await pg.evaluate("$('tC').onclick()")
            while await pg.evaluate("!!FLIP"):await pg.wait_for_timeout(30)
            await pg.wait_for_timeout(800)
        await pg.click("#play");await pg.evaluate("$('tC').onclick()")
        rows=[];k=0
        for i in range(200):
            r=await pg.evaluate("""()=>{const caps=prims.filter(q=>q.nm==='Body'&&q.cap).map(q=>q.a);const A=caps[0],B=caps[1];
              const roots={};for(const q of prims){if(q.nm==='Body'||!q.cap)continue;if(!roots[q.nm])roots[q.nm]=q.a}
              const D=(u,v)=>Math.hypot(u[0]-v[0],u[1]-v[1],u[2]-v[2]);const ax=[B[0]-A[0],B[1]-A[1],B[2]-A[2]],L=Math.hypot(...ax);
              const tilt=Math.asin(Math.max(-1,Math.min(1,ax[1]/L)))*180/Math.PI;let worst=0,wn='';const att={};
              for(const n in roots){const v=roots[n];const dd=Math.min(D(v,A),D(v,B));att[n]=[+dd.toFixed(0),D(v,A)<D(v,B)?'A':'B'];if(dd>worst){worst=dd;wn=n}}
              return [FLIP&&FLIP.kind,FLIP?+flipT().toFixed(2):1,+tilt.toFixed(0),+worst.toFixed(0),wn,att,+L.toFixed(0)]}""")
            rows.append((i,)+tuple(r))
            if not r[0]:
                k+=1
                if k>3:break
            await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        base=rows[0][4]
        top=max(rows,key=lambda x:x[4])
        tl=[x[3] for x in rows]
        print(f"{url.split('/')[-1]:11s} {mode:8s} {phase:4s} {w:5s} {d:4s} frames {len(rows)} root-to-body-end start {base} worst {top[4]} ({top[5]} at t {top[2]}) tilt range {min(tl)}..{max(tl)} start {tl[0]} end {tl[-1]}")
        if verb:
            for x in rows:print(x[0],x[1],x[2],'tilt',x[3],'worst',x[4],x[5],'len',x[7],{n:v for n,v in x[6].items()})
        await b.close()
asyncio.run(main())
