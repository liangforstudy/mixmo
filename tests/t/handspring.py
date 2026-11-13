# Handspring / Flip checks (2026-11-13): every fast animation (done, ends in its own animation, ends swapped, lowest
# point, bone fixes), 3 queued flips, turn / Spin pressed during a handspring, Flip during a turn (queues) and while
# spinning (refused), reversed run6, rewinding through a whole handspring. Usage: python3 t/handspring.py [url]
import asyncio,sys,math,json
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv)>1 else "http://localhost:8765/Mixmo.html"
SETUP="""(m)=>{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');if(s.value!=='robot'){s.value='robot';s.onchange()}const q=document.getElementById('modeSel');q.value=m;q.onchange()}"""
MON="""()=>{window.__M={lo:1e9,bone:0,frames:0};const f0=buildRobot;buildRobot=function(p,ph){f0(p,ph);if(FLIP&&FLIP.kind==='spring'){__M.frames++;__M.bone=Math.max(__M.bone,BONEBAD);
 for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a])){const y=v[1]-ground(v[0],v[2]);if(y<__M.lo)__M.lo=y}}}}}"""
async def flip_and_wait(pg,timeout=6):
    await pg.evaluate("$('tF').onclick()")
    for _ in range(int(timeout/0.03)):
        if await pg.evaluate("!FLIP&&!WALKOVER&&FLIPQ===0"):return True
        await pg.wait_for_timeout(30)
    return False
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":420,"height":900});errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto(F if F.startswith("http") else "file://"+F);await pg.wait_for_timeout(400);await pg.evaluate(MON)
        print("-- every fast animation")
        for m in ["run","runTail","dino","roo","run4dog","run4","run5b","run5f","run5head","run6"]:
            await pg.evaluate(SETUP,m);await pg.wait_for_timeout(1300);await pg.evaluate("__M.lo=1e9;__M.bone=0;__M.frames=0")
            s0=await pg.evaluate("SWAP");ok=await flip_and_wait(pg);r=await pg.evaluate("[mode,SWAP,__M.lo,__M.bone,__M.frames,flipKind()]")
            print(f"  {m:9s} done={ok} ends in {r[0]:9s} swapped={r[1]!=s0} lowest={r[2]:.1f} bonefix={r[3]} frames={r[4]}")
        print("-- queue: 3 taps on run6")
        await pg.evaluate(SETUP,"run6");await pg.wait_for_timeout(1300);s0=await pg.evaluate("SWAP")
        for i in range(3):await pg.evaluate("$('tF').onclick()");await pg.wait_for_timeout(80)
        n=0;last=s0
        for _ in range(300):
            await pg.wait_for_timeout(30);s=await pg.evaluate("SWAP")
            if s!=last:n+=1;last=s
            if await pg.evaluate("!FLIP&&FLIPQ===0"):break
        print("  flips played:",n,"mode",await pg.evaluate("mode"))
        print("-- turn pressed during a handspring (run)")
        await pg.evaluate(SETUP,"run");await pg.wait_for_timeout(1300)
        await pg.evaluate("$('tF').onclick()");await pg.wait_for_timeout(250);h0=await pg.evaluate("HEAD")
        await pg.evaluate("$('tL').onclick()");await pg.wait_for_timeout(200);print("  heading changed mid-flip:",abs(await pg.evaluate("HEAD")-h0)>1e-3,"TURNM:",await pg.evaluate("!!TURNM"))
        while await pg.evaluate("!!FLIP||!!TURNM"):await pg.wait_for_timeout(30)
        print("-- flip pressed during a turn (run)")
        await pg.evaluate("$('tR').onclick()");await pg.wait_for_timeout(150);await pg.evaluate("$('tF').onclick()")
        r=await pg.evaluate("[!!TURNM,FLIP&&FLIP.kind,FLIPQ]");print("  during turn: turning",r[0],"flip",r[1],"queued",r[2])
        while await pg.evaluate("!!TURNM||!!FLIP||FLIPQ>0"):await pg.wait_for_timeout(30)
        print("  after: flipped once queued? mode",await pg.evaluate("mode"))
        print("-- flip pressed while spinning (run)")
        await pg.evaluate("$('tS').onclick()");await pg.wait_for_timeout(300);await pg.evaluate("$('tF').onclick()")
        print("  spinning",await pg.evaluate("!!SPIN"),"flip",await pg.evaluate("FLIP&&FLIP.kind"),"msg",await pg.evaluate("$('msg').textContent"))
        await pg.evaluate("toggleSpin(true)");await pg.wait_for_timeout(300)
        while await pg.evaluate("!!FLIP"):await pg.wait_for_timeout(30)
        print("-- reversed (run6, swap ends first, then flip)")
        await pg.evaluate(SETUP,"run6");await pg.wait_for_timeout(1300);await pg.evaluate("document.querySelector('#lyingTurn [data-t=swap]').click();$('tU').onclick()")
        while await pg.evaluate("!!TURNM"):await pg.wait_for_timeout(30)
        await pg.wait_for_timeout(500);await pg.evaluate("__M.lo=1e9;__M.bone=0");d=await pg.evaluate("DIR");z0=await pg.evaluate("[POS[0],POS[1]]")
        ok=await flip_and_wait(pg);z1=await pg.evaluate("[POS[0],POS[1],mode,__M.lo,__M.bone,DIR]")
        print(f"  DIR before {d} done={ok} mode {z1[2]} lowest {z1[3]:.1f} bonefix {z1[4]} DIR after {z1[5]} moved {math.dist(z0,z1[:2]):.0f}")
        print("-- rewind through a whole handspring and come back (run6)")
        await pg.evaluate(SETUP,"run6");await pg.wait_for_timeout(1300);await flip_and_wait(pg);await pg.wait_for_timeout(300)
        await pg.click("#play");end=await pg.evaluate("[POS[0],POS[1],SWAP,phase]")
        kinds=set()
        for i in range(90):
            await pg.evaluate("hStep(-1)");kinds.add(await pg.evaluate("FLIP&&FLIP.kind"))
        mid=await pg.evaluate("[HPOS,SWAP]")
        for i in range(90):await pg.evaluate("hStep(1)")
        back=await pg.evaluate("[POS[0],POS[1],SWAP,phase,HPOS]")
        print("  seen while stepping back:",kinds,"| back at now:",back[4]==-1,"same place:",math.dist(end[:2],back[:2])<1e-6,"same ends:",end[2]==back[2])
        print("errors",errs);await b.close()
asyncio.run(main())
