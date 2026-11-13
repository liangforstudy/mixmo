# Ceiling checks (2026-11-13). Usage: see the arguments in main(); serve this folder on port 8765 first.
import asyncio,sys,io
from playwright.async_api import async_playwright
from PIL import Image
# fall.py mode opt(four|six|flip) out.png n
async def main():
    mode,opt,out,n=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]);roll=sys.argv[5] if len(sys.argv)>5 else '1'
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script("try{if(!localStorage.getItem('mixmoTier'))localStorage.setItem('mixmoTier','anim')}catch(e){}");errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("http://localhost:8765/Mixmo.html");await pg.wait_for_timeout(400)
        await pg.evaluate(f"""()=>{{document.querySelector('#rendSw [data-r=canvas]').click();document.querySelector('#ceilDrop [data-d={opt}]').click();document.querySelector('#ceilRoll [data-r="{roll}"]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange();yaw=1.57;pitch=0.1;zoom=0.7}}""")
        await pg.wait_for_timeout(1300);await pg.evaluate("$('tC').onclick()")
        while await pg.evaluate("!!FLIP"):await pg.wait_for_timeout(30)
        await pg.wait_for_timeout(900);await pg.click("#play");await pg.evaluate("$('tC').onclick()")
        await pg.evaluate("window.__prev=null")
        frames=[];lo=1e9;bad=0;jumps=[];kinds=set()
        for i in range(140):
            r=await pg.evaluate("""()=>{const P=[];let lo=1e9;for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a])){P.push([v[0]+POS[0],v[1],v[2]+POS[1]]);lo=Math.min(lo,v[1]-ground(v[0],v[2]))}}
              let worst=0;if(__prev){for(const v of P){let m=1e9;for(const u of __prev){const d=(v[0]-u[0])**2+(v[1]-u[1])**2+(v[2]-u[2])**2;if(d<m)m=d}if(m>worst)worst=m}}
              __prev=P;return [FLIP&&FLIP.kind,FLIP?+flipT().toFixed(2):1,lo,Math.sqrt(worst),BONEBAD,mode,GECKO,$('stText').textContent]}""")
            if r[0]:kinds.add(r[0])
            if r[0] or i<3: lo=min(lo,r[2]);bad=max(bad,r[4]);jumps.append((r[1],round(r[3],1)))
            el=await pg.query_selector("#view");frames.append(Image.open(io.BytesIO(await el.screenshot())))
            if not r[0] and i>2:break
            await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        top=sorted(jumps[1:],key=lambda x:-x[1])[:4]
        print(f"{mode} {opt} roll={roll}: kinds {kinds} frames {len(frames)} ends in {r[5]} gecko {r[6]} lowest {lo:.1f} bonefix {bad} biggest steps {top} errors {errs}")
        fr=[frames[round(j*(len(frames)-1)/(n-1))] for j in range(n)];w,h=fr[0].size;s=0.5
        o=Image.new("RGB",(int(w*s)*n,int(h*s*0.62)),"white")
        for j,im in enumerate(fr):o.paste(im.resize((int(w*s),int(h*s))).crop((0,int(h*s*0.04),int(w*s),int(h*s*0.66))),(j*int(w*s),0))
        o.save(out);await b.close()
asyncio.run(main())
