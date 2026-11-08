from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
rows={}
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
    pg.evaluate('()=>{$("modeSel").value="idle";$("modeSel").onchange();yaw=0.35;pitch=0.2;zoom=1.05}')
    for opt,vals in [(1,[0.3,0.45,0.75,1.3,1.6,2.0]),(2,[1.3,1.6,1.75,1.85,1.93,2.0]),(3,[1.3,1.6,1.75,1.85,1.93,2.0])]:
        pg.evaluate(f'()=>document.querySelector(\'#armOpt [data-a="{opt}"]\').click()');ims=[]
        for v in vals:
            pg.evaluate(f'()=>setCycle({v})');pg.wait_for_timeout(1400)
            pg.locator('#view').screenshot(path=S+'c.png');im=Image.open(S+'c.png');w,h=im.size;ims.append(im.crop((int(w*0.1),int(h*0.08),int(w*0.9),int(h*0.92))).resize((230,int(230*h*0.84/(w*0.8)))))
        rows[opt]=ims
    print(errs);b.close()
w,h=rows[1][0].size;W=Image.new('RGB',(w*6+50,h*3+20),'white')
for r,opt in enumerate([1,2,3]):
    for i,im in enumerate(rows[opt]):W.paste(im,(i*(w+10),r*(h+10)))
W.save(S+'arms.png')
