import time
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700});pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>document.querySelector(\'#rendSw [data-r="three"]\').click()');pg.wait_for_timeout(2500)
    # 1: normal warm-up
    pg.set_input_files('#mdlFile',S+'real/baller_fox_body.glb');t0=time.time();shown=False
    for i in range(300):
        pg.wait_for_timeout(50);m=pg.evaluate('$("mdlMsg").textContent')
        if 'GPU' in m:shown=True;last=m
        if shown and m=='':print('last progress:',last);print('normal: message cleared after %.1fs'%(time.time()-t0));break
    # 2: a warm-up that never finishes (as it might on a GPU that never reports ready)
    pg.evaluate('()=>{window.mdlWarm=()=>new Promise(()=>{});const g=R3.rd.properties.get.bind(R3.rd.properties);R3.rd.properties.get=o=>{const v=g(o);if(o&&o.isMaterial&&o.name==="")return {...v,currentProgram:{isReady:()=>false}};return v}}')
    pg.set_input_files('#mdlFile',S+'glb/foxlike.glb');t0=time.time();shown=False
    for i in range(300):
        pg.wait_for_timeout(50);m=pg.evaluate('$("mdlMsg").textContent')
        if 'GPU' in m:shown=True
        if 'confirmed' in m and 'yet' in m:print('stuck warm-up after %.1fs:'%(time.time()-t0),m);break
        if shown and m=='':print('stuck warm-up: message cleared after %.1fs, cards %d, button enabled %s'%(time.time()-t0,pg.evaluate('document.querySelectorAll(".mdlCard").length'),pg.evaluate('!$("mdlPick").disabled')));break
    b.close()
