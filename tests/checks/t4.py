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
    pg.evaluate('()=>{if(playing)$("play").onclick()}')
    def shot(name,js=''):
        pg.evaluate('()=>{'+js+'}');pg.wait_for_timeout(300);pg.locator('#view').screenshot(path=S+name+'.png');shots.append(name)
    shot('a_default')
    shot('b_capsule','document.querySelector(\'[data-k="limbs"][data-v="capsule"]\').click()')
    shot('c_soft','document.querySelector(\'[data-k="limbs"][data-v="smooth"]\').click();document.querySelector(\'[data-k="style"][data-v="soft"]\').click()')
    shot('d_robot_hills','document.querySelector(\'[data-k="style"][data-v="toon"]\').click();$("charSel").value="robot";$("charSel").onchange();RLOOK.skin="sergal";document.querySelector(\'#terrain [data-t="hills"]\').click()')
    print('errors',errs)
    b.close()
ims=[Image.open(S+n+'.png') for n in shots];w0,h0=ims[0].size
W=Image.new('RGB',(w0*2+10,h0*2+10),'white')
for i,im in enumerate(ims):W.paste(im,((i%2)*(w0+10),(i//2)*(h0+10)))
W.save(S+'look.png')
