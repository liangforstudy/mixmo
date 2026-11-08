import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
tag=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':760},device_scale_factor=1)
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/'+(sys.argv[2] if len(sys.argv)>2 else 'Mixmo.html'));pg.wait_for_timeout(1200)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();$("charSel").value="robot";$("charSel").onchange();$("modeSel").value="run4dog";$("modeSel").onchange();if(!playing)$("play").onclick()}')
    pg.wait_for_timeout(3000);pg.evaluate('()=>{if(playing)$("play").onclick()}')
    shots=[]
    for i,(yw,pt) in enumerate([(2.3,0.08),(2.5,0.08),(2.7,0.08),(2.9,0.08),(3.1,0.08),(3.4,0.08)]):
        pg.evaluate(f'()=>{{yaw={yw};pitch={pt};zoom=2.4}}');pg.wait_for_timeout(250)
        box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
        f=S+f'd2_{tag}_{i}.png';pg.screenshot(path=f,clip={'x':box[0],'y':box[1],'width':box[2],'height':min(box[3],380)});shots.append(f)
    b.close()
from PIL import Image
ims=[Image.open(f) for f in shots];w,h=ims[0].size;o=Image.new('RGB',(w*3,h*2))
for k,im in enumerate(ims):o.paste(im,((k%3)*w,(k//3)*h))
o.save(S+f'd2_{tag}.png')
