from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read();rows=[]
TRY={'current':'','straighter':'Object.assign(P.run4dog,{knee:40,hock:34,thigh:20,splay:6,lift:24})'}
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    for name,js in TRY.items():
        pg=b.new_page(viewport={'width':900,'height':700})
        pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
        pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
        pg.evaluate('()=>{$("charSel").value="robot";$("charSel").onchange();'+js+';$("modeSel").value="run4dog";$("modeSel").onchange();blendU=1;yaw=Math.PI/2;pitch=0.05;zoom=1.6;panY=-40}');pg.wait_for_timeout(2500)
        pg.evaluate('()=>{if(playing)$("play").onclick()}');ims=[]
        for i in range(6):
            pg.evaluate('()=>{for(let i=0;i<4;i++)stepFrame(1)}');pg.wait_for_timeout(250)
            pg.locator('#view').screenshot(path=S+'d.png');im=Image.open(S+'d.png');w,h=im.size;ims.append(im.crop((int(w*0.12),int(h*0.35),int(w*0.88),int(h*0.98))).resize((280,int(280*h*0.63/(w*0.76)))))
        rows.append(ims);pg.close()
    b.close()
w,h=rows[0][0].size;W=Image.new('RGB',(w*3+20,h*4+30),'white')
for r,ims in enumerate(rows):
    for i,im in enumerate(ims):W.paste(im,((i%3)*(w+10),(r*2+i//3)*(h+10)))
W.save(S+'dog2.png')
