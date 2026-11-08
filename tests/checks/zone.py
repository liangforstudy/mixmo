import math
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True,is_mobile=True);pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click();yaw=0.7}');pg.wait_for_timeout(500)
    z=pg.evaluate('()=>{const r=$("stickZone").getBoundingClientRect(),v=$("view").getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height,vw:v.width,vh:v.height,label:getComputedStyle(document.querySelector("#stickZone .zl")).display,layout:document.documentElement.className}}')
    print('zone',z)
    pg.screenshot(path=S+'zone_fresh.png',clip={'x':0,'y':0,'width':390,'height':560})
    def drag(x0,y0,dx,dy,ms):
        p0=pg.evaluate('[...POS]');y_0=pg.evaluate('yaw')
        pg.mouse.move(x0,y0);pg.mouse.down();pg.mouse.move(x0+dx,y0+dy,steps=5);pg.wait_for_timeout(ms)
        m=pg.evaluate('mode');shown=pg.evaluate('$("stick").classList.contains("show")')
        if dx==0:pg.screenshot(path=S+'zone_drag.png',clip={'x':0,'y':0,'width':390,'height':560})
        pg.mouse.up();p1=pg.evaluate('[...POS]')
        v=pg.evaluate('a=>{const v=rotY([a[0],0,a[1]],yaw);return [v[0],v[2]]}',[p1[0]-p0[0],p1[1]-p0[1]])
        return m,shown,v,abs(pg.evaluate('yaw')-y_0)
    cx=z['x']+z['w']*0.5;cy=z['y']+z['h']*0.6
    m,sh,v,dy=drag(cx,cy,0,-60,1500);print(f'drag up (all the way): mode {m}, stick shown {sh}, moved toward camera {v[1]:.0f}, camera turned {dy:.3f}, label after: {pg.evaluate("getComputedStyle(document.querySelector(\'#stickZone .zl\')).display")}')
    m,sh,v,dy=drag(cx,cy,-20,0,1500);print(f'drag a little left: mode {m}, moved right {v[0]:.0f}')
    pg.wait_for_timeout(1200);print('released: mode',pg.evaluate('mode'),'| stick shown',pg.evaluate('$("stick").classList.contains("show")'))
    # right half still orbits the camera
    y0=pg.evaluate('yaw');rx=z['x']+z['vw']*0.8
    pg.mouse.move(rx,cy);pg.mouse.down();pg.mouse.move(rx+60,cy,steps=6);pg.mouse.up();print('drag in the right half turns the camera:',abs(pg.evaluate('yaw')-y0)>0.05)
    pg.reload();pg.wait_for_timeout(1000);print('after reload: label shown again',pg.evaluate('$("stickZone").classList.contains("fresh")'))
    ctx.close()
    pg=b.new_page(viewport={'width':1200,'height':760});pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(800)
    print('desktop layout: zone shown',pg.evaluate('!!$("stickZone").offsetParent'),errs)
    b.close()
