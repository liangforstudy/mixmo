from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
vals=[0,0.15,0.3,0.55,0.8,1.05,1.3,1.6,1.8,2.0];ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
    pg.evaluate('()=>{$("modeSel").value="idle";$("modeSel").onchange();yaw=0.5;pitch=0.2;zoom=1.1}');pg.wait_for_timeout(500)
    for v in vals:
        pg.evaluate(f'()=>setCycle({v})');pg.wait_for_timeout(1400)
        pg.locator('#view').screenshot(path=S+'c.png');im=Image.open(S+'c.png');w,h=im.size;ims.append(im.crop((int(w*0.2),int(h*0.05),int(w*0.8),int(h*0.95))).resize((260,int(260*h*0.9/(w*0.6)))))
    print(errs);b.close()
w,h=ims[0].size;W=Image.new('RGB',(w*5+40,h*2+10),'white')
for i,im in enumerate(ims):W.paste(im,((i%5)*(w+10),(i//5)*(h+10)))
W.save(S+'cycle.png')
