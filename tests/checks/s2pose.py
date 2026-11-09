from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
V=[(18,55,45),(8,40,36),(4,32,30),(0,28,34)]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':520,'height':700})
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();$("charSel").value="sergal2";$("charSel").onchange();$("modeSel").value="idle";$("modeSel").onchange()}')
    for i,(t,k,h) in enumerate(V):
        pg.evaluate(f'()=>{{Object.assign(P.idle,{{thigh:{t},knee:{k},hock:{h}}});Object.assign(cur,{{thigh:{t},knee:{k},hock:{h}}});from={{...cur}};if(!playing)$("play").onclick()}}');pg.wait_for_timeout(900)
        pg.evaluate('()=>{if(playing)$("play").onclick();yaw=1.57;pitch=0.05;zoom=1.3}');pg.wait_for_timeout(300)
        box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
        pg.screenshot(path=S+f'pose{i}.png',clip={'x':box[0]+100,'y':box[1],'width':300,'height':min(box[3],460)})
    b.close()
from PIL import Image
ims=[Image.open(S+f'pose{i}.png') for i in range(len(V))];w,h=ims[0].size
o=Image.new('RGB',(w*len(ims),h));[o.paste(im,(i*w,0)) for i,im in enumerate(ims)];o.save(S+'poses.png')
