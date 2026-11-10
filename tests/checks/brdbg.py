from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(**p.devices['iPhone 13']);pg=ctx.new_page();logs=[]
    pg.on('console',lambda m:logs.append(m.text))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(2500)
    pg.evaluate('''()=>{const o=hBranch;window.hBranch=function(){console.log("BRANCH "+new Error().stack.split("\\n").slice(1,4).join(" | "));return o.apply(this,arguments)};
      ["click","change","input","pointerdown","pointerup"].forEach(t=>document.addEventListener(t,e=>console.log(t+" "+(e.target.id||e.target.className||e.target.tagName)),true))}''')
    pg.tap('#play');pg.wait_for_timeout(300);pg.tap('#prevF');pg.wait_for_timeout(250);logs.append('--- 2nd');pg.tap('#prevF');pg.wait_for_timeout(250)
    print('\n'.join(logs[-30:]));b.close()
