from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':520,'height':700})
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1000)
    print(pg.evaluate('''()=>{$("charSel").value="sergal2";$("charSel").onchange();$("modeSel").value="walk";$("modeSel").onchange();
      buildSergal2({...P.walk},0.1);return JSON.stringify([...new Set(prims.map(q=>q.nm))])+JSON.stringify(prims.filter(q=>q.nm==="Left leg").map(q=>[q.t,q.a,q.b]))}'''))
    b.close()
