from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':520,'height':700})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1000)
    for m in ['walk','run']:
      r=pg.evaluate(f'''()=>{{$("charSel").value="sergal2";$("charSel").onchange();$("modeSel").value="{m}";$("modeSel").onchange();if(playing)$("play").onclick();
       const out=[];for(let i=0;i<8;i++){{const ph=i/8;buildSergal2({{...P["{m}"],bobWave:0}},ph);
        const leg=prims.filter(q=>q.nm==="Left leg"),arm=prims.filter(q=>q.nm==="Upper arm A"),legR=prims.filter(q=>q.nm==="Right leg");
        const lf=leg[3].b,hip=leg[0].a,hand=arm[arm.length-1].a,sh=arm[0].a;
        out.push([ph,(lf[2]-hip[2]).toFixed(1),(hand[2]-sh[2]).toFixed(1),(legR[3].b[2]-legR[0].a[2]).toFixed(1),HEAD.toFixed(2)])}}return out}}''')
      print(m);[print(x) for x in r]
    print(errs[:3]);b.close()
