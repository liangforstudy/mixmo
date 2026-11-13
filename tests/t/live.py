import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as pw:
    for dev,r2d in [(None,False),(None,True),("iPhone 13",False)]:
        b=pw.chromium.launch()
        ctx=b.new_context(**(pw.devices[dev] if dev else {"viewport":{"width":1200,"height":800}}))
        pg=ctx.new_page();pg.add_init_script("try{if(!localStorage.getItem('mixmoTier'))localStorage.setItem('mixmoTier','anim')}catch(e){}");errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e)));pg.on("console",lambda m:errs.append("console: "+m.text) if m.type=="error" else None)
        pg.goto(url);pg.wait_for_timeout(2500)
        if r2d:pg.evaluate("R3.want='2d'")
        pg.evaluate("$('charSel').value='robot';$('charSel').onchange();$('modeSel').value='walk';$('modeSel').onchange()")
        pg.wait_for_timeout(1200)
        st=[]
        for rep in range(2):
            pg.evaluate("$('tF').onclick()")
            for i in range(60):
                pg.wait_for_timeout(100);st.append(pg.evaluate("[FLIP?FLIP.kind+(FLIP.nu?'*':''):'-',$('stText').textContent]"))
        kinds=sorted(set(k for k,_ in st));txt=[t for _,t in st if 'Rise' in t]
        print(dev or "desktop","2D" if r2d else "3D:"+str(pg.evaluate("R3.ok")),"| flip kinds seen",kinds,"| errors",errs[:3])
        print("   status samples:",txt[1] if len(txt)>1 else None,"|",txt[len(txt)//2] if txt else None)
        print("   end:",pg.evaluate("[mode,SWAP,blendU,HIST.length>0]"))
        b.close()
