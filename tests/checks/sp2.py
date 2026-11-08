from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1280,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
    pg.evaluate('()=>{$("modeSel").value="idle";$("modeSel").onchange();yaw=0.25;pitch=0.25}');pg.wait_for_timeout(800)
    for nm,js in [('s0',''),('s05','setSplit(0.5)'),('s1','setSplit(1)'),('h1','setSplit(0);SPLITE=0;setHMerge(1)')]:
        pg.evaluate('()=>{'+js+'}');pg.wait_for_timeout(1500);pg.locator('#view').screenshot(path=S+nm+'.png');shots.append(nm)
    # long-press drag on the body
    pg.evaluate('()=>{setHMerge(0)}');pg.wait_for_timeout(300)
    bx=pg.locator('#view').bounding_box();cx,cy=bx['x']+bx['width']/2,bx['y']+bx['height']*0.6
    pg.mouse.move(cx,cy);pg.mouse.down();pg.wait_for_timeout(500);print('gesture',pg.evaluate('gesture&&gesture.pull'));pg.mouse.move(cx+120,cy,steps=6);pg.mouse.up()
    print('split after drag',pg.evaluate('SPLIT'),'yaw unchanged',pg.evaluate('yaw.toFixed(2)'))
    pg.mouse.move(cx,cy);pg.mouse.down();pg.mouse.move(cx+60,cy,steps=4);pg.mouse.up();print('quick drag orbits: yaw',pg.evaluate('yaw.toFixed(2)'),'split',pg.evaluate('SPLIT'))
    print('errors',errs);b.close()
ims=[Image.open(S+n+'.png') for n in shots];w0,h0=ims[0].size
W=Image.new('RGB',(w0*2+10,h0*2+10),'white')
for i,im in enumerate(ims):W.paste(im,((i%2)*(w0+10),(i//2)*(h0+10)))
W.save(S+'split.png')
