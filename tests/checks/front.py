from playwright.sync_api import sync_playwright
from PIL import Image
import sys,shutil
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read();rows=[]
shutil.copy(S+'before_yaw.html','/home/claude/before_yaw.html')
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    for f in ['before_yaw.html','Mixmo.html']:
        pg=b.new_page(viewport={'width':600,'height':700})
        pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
        pg.goto('http://localhost:8765/'+f);pg.wait_for_timeout(1500)
        pg.evaluate('()=>{$("charSel").value="robot";$("charSel").onchange();$("modeSel").value="run";$("modeSel").onchange();blendU=1}');pg.wait_for_timeout(2500)
        pg.evaluate('()=>{if(playing)$("play").onclick();yaw=0;pitch=0.12;zoom=2.0;panY=-120}')
        ims=[]
        for fr in [10,11,12,13,14]:
            pg.evaluate(f'()=>{{scrubTo(({fr}-1)/24);const tg=P[mode];for(const k in tg)cur[k]=tg[k];charDef().build({{...cur}},phase);render()}}');pg.wait_for_timeout(250)
            pg.locator('#view').screenshot(path=S+'fr.png');im=Image.open(S+'fr.png');w,h=im.size;ims.append(im.crop((int(w*.1),int(h*.25),int(w*.9),h)).resize((220,int(220*h*.75/(w*.8)))))
        rows.append(ims);pg.close()
    b.close()
w,h=rows[0][0].size;W=Image.new('RGB',(w*5+40,h*2+10),'white')
for r,ims in enumerate(rows):
    for i,im in enumerate(ims):W.paste(im,(i*(w+10),r*(h+10)))
W.save(S+'front.png')
