import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
F=sys.argv[1];mo=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700})
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").onchange()}')
    pg.set_input_files('#mdlFile',S+'real/'+F+'.glb')
    for i in range(120):
        pg.wait_for_timeout(500)
        if pg.evaluate('MODELS.length===1&&!MLOAD.busy'):break
    pg.click('.mdlCard [data-g="place"] [data-v="in"]');pg.click('.mdlCard [data-g="move"] [data-v="move"]')
    pg.evaluate(f'()=>{{$("modeSel").value="{mo}";$("modeSel").onchange();if(!playing)$("play").onclick()}}');pg.wait_for_timeout(2500)
    shots=[]
    for k in range(4):
        pg.evaluate('()=>{if(playing)$("play").onclick();yaw=1.57;pitch=0.02;zoom=1.25;panY=60}');pg.wait_for_timeout(400)
        box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
        fn=S+f'step_{k}.png';pg.screenshot(path=fn,clip={'x':box[0]+box[2]*0.2,'y':box[1]+box[3]*0.35,'width':box[2]*0.6,'height':box[3]*0.65});shots.append(fn)
        pg.evaluate('()=>{if(!playing)$("play").onclick()}');pg.wait_for_timeout(170 if mo=='walk' else 90)
    b.close()
from PIL import Image
ims=[Image.open(f) for f in shots];w,h=ims[0].size;o=Image.new('RGB',(w*4,h));[o.paste(im,(i*w,0)) for i,im in enumerate(ims)];o=o.resize((w*2,h//2));o.save(S+f'steps_{F}_{mo}.png')
