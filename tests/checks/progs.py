import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':520,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/'+F);pg.wait_for_timeout(4000)
    print(F,'3D ready:',pg.evaluate('R3.ok'),'programs after start:',pg.evaluate('R3.rd.info.programs.length'),'2D label:',pg.evaluate('document.querySelector("#rendSw [data-r=canvas]").textContent'))
    tot=0
    for k,v in [('style','soft'),('shadow','blob'),('outline','off'),('ground','grid'),('limbs','capsule'),('style','toon'),('shadow','real'),('outline','on'),('ground','solid'),('limbs','smooth')]+[('char','robot'),('style','soft'),('shadow','blob'),('ground','grid')]:
        n0=pg.evaluate('R3.rd.info.programs.length');ph0=pg.evaluate('phase')
        if k=='char':pg.evaluate('()=>{$("charSel").value="robot";$("charSel").onchange()}')
        else:pg.evaluate(f'()=>document.querySelector(\'#r3Look [data-k="{k}"][data-v="{v}"]\').click()')
        pg.wait_for_timeout(500);n1=pg.evaluate('R3.rd.info.programs.length');ph1=pg.evaluate('phase')
        tot+=n1-n0;print(f'  {k}={v}: new shaders built on the spot {n1-n0}, still playing {ph1!=ph0}')
    print('total',tot,errs);b.close()
