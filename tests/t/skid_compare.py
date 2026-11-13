import asyncio,io
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
# old vs fix: Run on six at a run, two 180s; frames through each skid, side view
async def shots(b,k):
    pg=await b.new_page(viewport={"width":360,"height":700});await pg.add_init_script(f"try{{localStorage.setItem('mixmoTier','dev');localStorage.setItem('mixmoSkidEnd','{k}')}}catch(e){{}}")
    await pg.goto("http://localhost:8765/Mixmo.html");await pg.wait_for_timeout(400)
    await pg.evaluate("()=>{document.querySelector('#rendSw [data-r=canvas]').click();const s=document.getElementById('charSel');s.value='robot';s.onchange();const m=document.getElementById('modeSel');m.value='run6';m.onchange();yaw=1.57;pitch=0.1;zoom=0.85}")
    await pg.wait_for_timeout(1200);await pg.click("#play");out=[]
    for turn in range(2):
        await pg.evaluate("$('tU').onclick()");fr=[]
        for i in range(60):
            t=await pg.evaluate("TURNM?(phase-TURNM.p0)/TURNM.len:null")
            if t is None and i>2:break
            if t is not None and any(abs(t-x)<0.035 for x in (0.1,0.3,0.5,0.75)) and (not fr or abs(fr[-1][0]-t)>0.1):
                await pg.evaluate("yaw=1.57-HEAD");el=await pg.query_selector("#view")
                fr.append((t,Image.open(io.BytesIO(await el.screenshot())).convert("RGB")))
            await pg.evaluate("hStep(1)");await pg.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        out.append(fr)
        for _ in range(20):await pg.evaluate("hStep(1)")
    await pg.close();return out
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        rows=[("Now: same end every time","same"),("Fix: the end behind him","behind")]
        data=[(lab,await shots(b,k)) for lab,k in rows]
        W,H=data[0][1][0][0][1].size;s=0.6;cw,ch=int(W*s),int(H*s*0.36);ncol=4
        o=Image.new("RGB",(cw*ncol,(ch+18)*4+24),"white");d=ImageDraw.Draw(o)
        d.text((6,4),"Run on all six, running: 180 pressed twice. Side view. 180 #1: he runs to the right, so his left end is behind. 180 #2: he runs to the left, so his right end is behind.",fill=(0,0,0))
        r=0
        for ti in range(2):
            for lab,turns in data:
                y=24+r*(ch+18);d.text((6,y),f"180 #{ti+1} ({'running right' if ti==0 else 'running left'}): {lab}",fill=(140,30,20))
                for c,(t,im) in enumerate(turns[ti][:4]):
                    sm=im.resize((cw,int(H*s))).crop((0,int(H*s*0.40),cw,int(H*s*0.40)+ch));o.paste(sm,(c*cw,y+14));d.text((c*cw+4,y+16),f"{int(t*100)}%",fill=(0,0,0))
                r+=1
        o.save("/home/claude/work/skid-compare.png");print(o.size,[len(x) for _,t in data for x in t])
        await b.close()
asyncio.run(main())
