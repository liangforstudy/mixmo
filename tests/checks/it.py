from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read();ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
    pg.evaluate('()=>{yaw=1.2;pitch=0.2;zoom=1.1}')
    for m,wait in [('idle',1500),('idleTail',250),('idleTail',1500)]:
        pg.evaluate(f'()=>{{$("modeSel").value="{m}";$("modeSel").onchange()}}');pg.wait_for_timeout(wait)
        pg.locator('#view').screenshot(path=S+'c.png');im=Image.open(S+'c.png');w,h=im.size;ims.append(im.crop((int(w*0.15),0,int(w*0.85),h)).resize((300,int(300*h/(w*0.7)))))
    print('mode list',pg.evaluate('MODES.map(m=>m[0]).join(",")'),'errors',errs);b.close()
w,h=ims[0].size;W=Image.new('RGB',(w*3+20,h),'white')
for i,im in enumerate(ims):W.paste(im,(i*(w+10),0))
W.save(S+'idles.png')
