from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':520,'height':700})
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    for ch in ['sergal2','sergal']:
      print(ch,pg.evaluate('''(ch)=>{$("charSel").value=ch;$("charSel").onchange();$("modeSel").value="idle";$("modeSel").onchange();return new Promise(r=>setTimeout(()=>{let mx=-1e9,mn=1e9;for(const q of prims){if(q.t===2)continue;for(const v of [q.a,q.b])if(v){mx=Math.max(mx,v[1]+(q.ra||0));mn=Math.min(mn,v[1]-(q.ra||0))}}r([mx,mn])},1500))}''',ch))
    b.close()
