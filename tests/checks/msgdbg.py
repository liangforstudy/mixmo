import time
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>document.querySelector(\'#rendSw [data-r="three"]\').click()');pg.wait_for_timeout(2500)
    pg.set_input_files('#mdlFile',S+'real/baller_fox_body.glb');t0=time.time();seen=[]
    for i in range(200):
        pg.wait_for_timeout(100);m=pg.evaluate('$("mdlMsg").textContent')
        if not seen or seen[-1][1]!=m:seen.append((round(time.time()-t0,1),m))
    for x in seen:print(x)
    print(errs)
    b.close()
