import json,sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
F=sys.argv[1] if len(sys.argv)>1 else 'baller_fox_body'
modes=sys.argv[2].split(',') if len(sys.argv)>2 else ['idle','walk','run']
place=sys.argv[3] if len(sys.argv)>3 else 'in'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1100,'height':850});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").onchange()}')
    pg.set_input_files('#mdlFile',S+'real/'+F+'.glb')
    for i in range(120):
        pg.wait_for_timeout(500)
        if pg.evaluate('!!MDL.info'):break
    pg.click(f'#mdlPlace [data-p="{place}"]');pg.click('#mdlMove [data-m="move"]');pg.wait_for_timeout(500)
    print('moves:',pg.evaluate('MDL.info.moves'),pg.evaluate('$("mdlMoveNote").textContent'),'base',pg.evaluate('MDL.mv&&MDL.mv.base'))
    shots=[]
    for mo in modes:
        pg.evaluate(f'()=>{{$("modeSel").value="{mo}";$("modeSel").onchange();if(!playing)$("play").onclick()}}');pg.wait_for_timeout(2500)
        for k,(yw,ph) in enumerate([(1.57,0),(0.6,0)]):
            pg.evaluate(f'()=>{{if(playing)$("play").onclick();yaw={yw};pitch=0.12;zoom=1.1}}');pg.wait_for_timeout(500)
            box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
            fn=S+f'm2_{F}_{mo}_{k}.png';pg.screenshot(path=fn,clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]});shots.append(fn)
            pg.evaluate('()=>{if(!playing)$("play").onclick()}');pg.wait_for_timeout(300)
    print(errs[:5]);b.close()
from PIL import Image
ims=[Image.open(f) for f in shots];w,h=ims[0].size;sc=0.5
o=Image.new('RGB',(int(w*sc)*2,int(h*sc)*len(modes)),'white')
for i,im in enumerate(ims):o.paste(im.resize((int(w*sc),int(h*sc))),((i%2)*int(w*sc),(i//2)*int(h*sc)))
o.save(S+f'm2_{F}_grid.png');print('saved')
