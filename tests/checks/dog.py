from playwright.sync_api import sync_playwright
from PIL import Image
import sys
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
url=sys.argv[1] if len(sys.argv)>1 else 'Mixmo.html';out=sys.argv[2] if len(sys.argv)>2 else 'dog.png'
rows=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/'+url);pg.wait_for_timeout(1500)
    for m in ['run6','run4dog']:
        pg.evaluate(f'()=>{{$("charSel").value="robot";$("charSel").onchange();$("modeSel").value="{m}";$("modeSel").onchange();blendU=1;yaw=Math.PI/2;pitch=0.05;zoom=0.85;panY=60}}');pg.wait_for_timeout(2500)
        pg.evaluate('()=>{if(playing)$("play").onclick()}');ims=[]
        for i in range(6):
            pg.evaluate('()=>{for(let i=0;i<4;i++)stepFrame(1)}');pg.wait_for_timeout(250)
            pg.locator('#view').screenshot(path=S+'d.png');im=Image.open(S+'d.png');w,h=im.size;ims.append(im.crop((0,int(h*0.25),w,h)).resize((300,int(300*h*0.75/w))))
        rows.append(ims)
    print(errs);b.close()
w,h=rows[0][0].size;W=Image.new("RGB",(w*3+20,h*4+30),"white")
for r,ims in enumerate(rows):
    for i,im in enumerate(ims):W.paste(im,((i%3)*(w+10),(r*2+i//3)*(h+10)))
W.save(S+out)
