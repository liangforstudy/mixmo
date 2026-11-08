from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read();ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
    pg.evaluate('()=>{$("charSel").value="robot";$("charSel").onchange();$("modeSel").value="walk";$("modeSel").onchange();blendU=1;yaw=1.3;pitch=0.15;zoom=1.0}');pg.wait_for_timeout(1500)
    pg.evaluate('()=>{if(playing)$("play").onclick();STEPBLEND=true;$("modeSel").value="run4dog";$("modeSel").onchange()}')
    log=[]
    for i in range(16):
        pg.evaluate('()=>{for(let i=0;i<5;i++)stepFrame(1)}');pg.wait_for_timeout(200)
        log.append(pg.evaluate('`${$("stText").textContent} | flip:${FLIP?FLIP.kind:"-"} blendU:${blendU.toFixed(2)}`'))
        pg.locator('#view').screenshot(path=S+'f.png');im=Image.open(S+'f.png');w,h=im.size;ims.append(im.crop((int(w*.15),int(h*.1),int(w*.85),int(h*.95))).resize((210,int(210*h*.85/(w*.7)))))
    print("\n".join(log));print(errs);b.close()
w,h=ims[0].size;W=Image.new('RGB',(w*8+70,h*2+10),'white')
for i,im in enumerate(ims):W.paste(im,((i%8)*(w+10),(i//8)*(h+10)))
W.save(S+'flap.png')
