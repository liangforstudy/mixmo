from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(3500)
    pg.evaluate('()=>{window.RN=0;const f=window.render;window.render=function(){RN++;return f.apply(this,arguments)};window.GT={n:0,ms:0};const g=window.drawGait;window.drawGait=function(){const t=performance.now();g();GT.n++;GT.ms+=performance.now()-t}}')
    def rate(ms=2000):
        pg.evaluate('()=>{RN=0}');pg.wait_for_timeout(ms);return round(pg.evaluate('RN')*1000/ms)
    for rend in ['canvas','three']:
        pg.evaluate(f'()=>document.querySelector(\'#rendSw [data-r="{rend}"]\').click()');pg.wait_for_timeout(500)
        for pw in ['off','on']:
            pg.evaluate(f'()=>{{document.querySelector(\'#powSw [data-p="{pw}"]\').click();if(!playing)$("play").onclick()}}');pg.wait_for_timeout(800)
            play=rate()
            pg.evaluate('()=>{if(playing)$("play").onclick()}');pg.wait_for_timeout(1500);idle=rate()
            # drag the camera while paused
            box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}')
            pg.evaluate('()=>{RN=0}');pg.mouse.move(box[0],box[1]);pg.mouse.down()
            for k in range(20):pg.mouse.move(box[0]+k*4,box[1]);pg.wait_for_timeout(50)
            pg.mouse.up();drag=pg.evaluate('RN')
            info=pg.evaluate('()=>({px:cv.width/cv.clientWidth,shadow3d:R3.sun?R3.sun.castShadow:null})')
            print(f'{rend:6s} power {pw:3s}: renders/s playing {play:3d}, paused {idle:3d}; renders during a 1 s camera drag while paused {drag:3d}; canvas pixels x{info["px"]}, 3D real shadows {info["shadow3d"]}')
        pg.evaluate('()=>document.querySelector(\'#powSw [data-p="off"]\').click()')
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#powSw [data-p="on"]\').click();if(playing)$("play").onclick()}');pg.wait_for_timeout(1500)
    box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
    pg.screenshot(path=S+'power_idle.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]*0.6})
    pg.evaluate('()=>{GT.n=0;GT.ms=0;document.querySelector(\'#powSw [data-p="off"]\').click();if(!playing)$("play").onclick()}');pg.wait_for_timeout(2000)
    print('gait chart + labels per frame now: %.3f ms'%(pg.evaluate('GT.ms/GT.n')))
    pg.evaluate('()=>$("powSw").scrollIntoView()');pg.query_selector('#powSw').evaluate('e=>e.closest(".row").parentElement.scrollTop')
    print(errs);b.close()
