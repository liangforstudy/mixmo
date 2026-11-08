import math
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click();yaw=0.7}');pg.wait_for_timeout(400)
    print('before tap: joystick shown',pg.evaluate('!!$("stick").offsetParent'),'| button shown',pg.evaluate('!!$("stickBtn").offsetParent'))
    pg.click('#stickBtn');pg.wait_for_timeout(300)
    print('after tap : joystick shown',pg.evaluate('!!$("stick").offsetParent'))
    pg.screenshot(path=S+'stick_shown.png',clip={'x':0,'y':0,'width':390,'height':560})
    box=pg.evaluate('()=>{const r=$("stick").getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}');cx,cy=box
    def push(dx,dy,ms):
        y0=pg.evaluate('yaw');p0=pg.evaluate('[...POS]')
        pg.mouse.move(cx,cy);pg.mouse.down();pg.mouse.move(cx+dx,cy+dy,steps=5);pg.wait_for_timeout(ms)
        m=pg.evaluate('mode');pg.screenshot(path=S+'stick_push.png',clip={'x':0,'y':0,'width':390,'height':560}) if dx==0 and dy==-60 else None
        pg.mouse.up();p1=pg.evaluate('[...POS]');y1=pg.evaluate('yaw')
        v=pg.evaluate('a=>{const v=rotY([a[0],0,a[1]],yaw);return [v[0],v[2]]}',[p1[0]-p0[0],p1[1]-p0[1]])
        return m,v,abs(y1-y0)
    for label,dx,dy in [('a little up',0,-22),('all the way up',0,-60),('all the way right',60,0)]:
        m,v,dyaw=push(dx,dy,1500)
        print(f'  {label:18s}: mode {m:5s}, moved right {v[0]:6.1f}, toward camera {v[1]:6.1f}; camera turned {dyaw:.3f}')
    pg.wait_for_timeout(1500);print('  released: mode',pg.evaluate('mode'))
    # circle the stick
    pg.mouse.move(cx+45,cy);pg.mouse.down()
    for i in range(1,80):
        a=i*0.22;pg.mouse.move(cx+45*math.cos(a),cy-45*math.sin(a));pg.wait_for_timeout(25)
    sp=pg.evaluate('!!SPIN');print('  after circling ~2.8 turns: spinning',sp)
    for i in range(80,140):
        a=i*0.22;pg.mouse.move(cx+45*math.cos(a),cy-45*math.sin(a));pg.wait_for_timeout(25)
    print('  still circling: spinning',pg.evaluate('!!SPIN&&SPIN.stopH===undefined'))
    pg.mouse.up();pg.wait_for_timeout(5000)
    h=pg.evaluate('HEAD*180/Math.PI');print(f'  let go: spinning {pg.evaluate("!!SPIN")}, facing {h%360:.1f} deg (multiple of 90: {abs(h/90-round(h/90))<1e-6})')
    print(errs);b.close()
