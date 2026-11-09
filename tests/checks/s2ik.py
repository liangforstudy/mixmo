from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':520,'height':700})
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1000)
    for ch in ['sergal2','sergal']:
      print(ch,pg.evaluate('''(ch)=>{$("charSel").value=ch;$("charSel").onchange();$("modeSel").value="idle";$("modeSel").onchange();if(playing)$("play").onclick();
      const q={...P.idle,thigh:0,knee:28,hock:34,bobWave:0};charDef().build(q,0);const L=prims.filter(z=>z.nm==="Left leg");
      const ang=(a,b)=>(Math.atan2(b[2]-a[2],-(b[1]-a[1]))*57.3).toFixed(0);
      return {H:restHeight(q).toFixed(1),hipY:L[0].a[1].toFixed(1),bones:L.map(z=>ang(z.a,z.b)),ik:charDef().limbs[1].ik,feet:TER.feet,lean:q.lean}}''',ch))
    b.close()
