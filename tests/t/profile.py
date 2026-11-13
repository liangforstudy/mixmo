import asyncio,sys,json
from playwright.async_api import async_playwright
WRAP="""()=>{window.__T={};const w=(o,k,lab)=>{const f=o[k];if(typeof f!=='function')return;o[k]=function(...a){const t=performance.now();const r=f.apply(this,a);const d=performance.now()-t;const e=__T[lab]||(__T[lab]=[0,0]);e[0]+=d;e[1]++;return r}};
 for(const k of ['buildRobot','buildRig','hRecord','hSnap','drawGait','showStatus','camReport','speedoUI','powerSig','r3render','drawGround','flipStep','advance','springStep','gameStep'])w(window,k,k);
 // the whole frame
 const rf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=cb=>rf(t=>{const s=performance.now();cb(t);const e=__T.frame||(__T.frame=[0,0]);e[0]+=performance.now()-s;e[1]++})}"""
async def main():
    url,char,mode,rend,play=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]=="play"
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
        pg=await b.new_page(viewport={"width":412,"height":915},device_scale_factor=2.6)
        await pg.add_init_script(f"try{{localStorage.setItem('mixmoTier','anim');localStorage.setItem('mixmoRenderer','{rend}')}}catch(e){{}}")
        await pg.goto(url);await pg.wait_for_timeout(2500)
        await pg.evaluate(f"()=>{{const s=document.getElementById('charSel');s.value='{char}';s.onchange();const m=document.getElementById('modeSel');m.value='{mode}';m.onchange()}}")
        await pg.wait_for_timeout(1500)
        if play!=await pg.evaluate("playing"):await pg.click("#play")
        await pg.evaluate(WRAP);await pg.wait_for_timeout(5000)
        T=await pg.evaluate("[__T,R3.ok,HIST.length,performance.memory?Math.round(performance.memory.usedJSHeapSize/1e6):null]")
        fr=T[0].get('frame',[0,1]);n=fr[1]
        print(f"{char} {mode} {rend} {'playing' if play else 'paused'}: 3D ok {T[1]} | {n} frames in 5 s | per frame ms:",{k:round(v[0]/n,2) for k,v in sorted(T[0].items(),key=lambda x:-x[1][0]) if v[0]/n>0.05},"| history",T[2],"| JS heap MB",T[3])
        await b.close()
asyncio.run(main())
