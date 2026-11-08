import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
tag=sys.argv[1];F=sys.argv[2] if len(sys.argv)>2 else 'Mixmo.html'
views=[(2.45,0.06,0),(2.75,0.06,0),(2.6,0.12,6),(2.6,0.0,3)]
from PIL import Image
out=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':420,'height':760},device_scale_factor=1)
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('file:///home/claude/'+F);pg.wait_for_timeout(3500)
    pg.evaluate('()=>{R3.look.limbs="capsule";R3.look.outline="on";r3applyLook();$("charSel").value="robot";$("charSel").onchange();$("modeSel").value="run4dog";$("modeSel").onchange();if(!playing)$("play").onclick()}')
    pg.wait_for_timeout(3000);pg.evaluate('()=>{if(playing)$("play").onclick()}')
    for i,(yw,pt,st) in enumerate(views):
        for k in range(st):pg.evaluate('()=>$("nextF").click()')
        pg.evaluate(f'()=>{{yaw={yw};pitch={pt};zoom=3.2;panY=-150;panX=-60}}')
        row=[]
        for r in ['canvas','three']:
            pg.evaluate(f'()=>document.querySelector(\'#rendSw [data-r="{r}"]\').click()');pg.wait_for_timeout(300)
            box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
            f=S+f'dc_{tag}_{i}_{r}.png';pg.screenshot(path=f,clip={'x':box[0],'y':box[1],'width':box[2],'height':min(box[3],380)});row.append(Image.open(f))
        out.append(row)
    b.close()
w,h=out[0][0].size;o=Image.new('RGB',(w*4,h*2))
for i,(a,c) in enumerate(out):o.paste(a,((i%2)*2*w,(i//2)*h));o.paste(c,((i%2)*2*w+w,(i//2)*h))
o.save(S+f'dc_{tag}.png')
