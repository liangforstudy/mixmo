import sys
from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
cases=[('walk',1,0.7,0.3),('walk',1,3.8,0.3),('run6',1,1.9,0.5),('run6',3,4.6,0.3),('run5head',2,0.3,0.2),('run4dog',1,5.2,-0.25)]
rows=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':420,'height':760},device_scale_factor=1);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(3500)
    pg.evaluate('()=>{R3.look.limbs="capsule";r3applyLook();$("charSel").value="robot";$("charSel").onchange()}')
    for m,sg,yw,pt in cases:
        pg.evaluate(f'()=>{{RLOOK.segs={sg};$("modeSel").value="{m}";$("modeSel").onchange();if(!playing)$("play").onclick()}}');pg.wait_for_timeout(2500)
        pg.evaluate(f'()=>{{if(playing)$("play").onclick();yaw={yw};pitch={pt};zoom=1.5}}')
        row=[]
        for r in ['canvas','three']:
            pg.evaluate(f'()=>document.querySelector(\'#rendSw [data-r="{r}"]\').click()');pg.wait_for_timeout(300)
            box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
            f=S+'w.png';pg.screenshot(path=f,clip={'x':box[0],'y':box[1],'width':box[2],'height':min(box[3],380)});row.append(Image.open(f).copy())
        rows.append(row)
    print(errs);b.close()
w,h=rows[0][0].size;o=Image.new('RGB',(w*4,h*3))
for i,(a,c) in enumerate(rows):o.paste(a,((i%2)*2*w,(i//2)*h));o.paste(c,((i%2)*2*w+w,(i//2)*h))
o.save(S+'wide.png')
