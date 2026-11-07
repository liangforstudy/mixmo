from playwright.sync_api import sync_playwright
import sys
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    for mode in ['ok','offline']:
        pg=b.new_page(viewport={'width':1280,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        if mode=='ok':pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
        else:pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
        pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
        print(mode,'ok:',pg.evaluate('R3.ok'),'msg:',pg.evaluate('$("r3msg").textContent'),'errs',errs[:3])
        if mode=='ok':
            for ch in ['sergal','robot']:
                pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").onchange()}}');pg.wait_for_timeout(500)
                pg.locator('#view').screenshot(path=S+f'3d_{ch}.png')
                pg.click('[data-r="canvas"]');pg.wait_for_timeout(300);pg.locator('#view').screenshot(path=S+f'2d_{ch}.png');pg.click('[data-r="three"]');pg.wait_for_timeout(300)
        else:pg.locator('#view').screenshot(path=S+'off.png')
        pg.close()
    b.close()
