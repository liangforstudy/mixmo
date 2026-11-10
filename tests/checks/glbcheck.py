from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1100,'height':850});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").dispatchEvent(new Event("change"))}')
    pg.wait_for_timeout(2500)
    pg.set_input_files('#mdlFile',[S+'real/baller_fox_body.glb',S+'real/female_sergal_body.glb'])
    for i in range(160):
        pg.wait_for_timeout(500)
        if pg.evaluate('MODELS.length===2&&!MLOAD.busy'):break
    for i in range(40):
        if pg.evaluate('$("mdlMsg").textContent===""'):break
        pg.wait_for_timeout(500)
    print('models:',pg.evaluate('MODELS.map(M=>[M.info.name,M.info.preset,M.place])'),'msg:',repr(pg.evaluate('$("mdlMsg").textContent')))
    cards=pg.query_selector_all('.mdlCard')
    for c in cards:c.query_selector('[data-g="move"] [data-v="move"]').click()
    box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
    shots=[]
    for mo in ['idle','walk','run']:
        pg.evaluate(f'()=>{{$("modeSel").value="{mo}";$("modeSel").onchange();if(!playing)$("play").onclick();yaw=0.15;pitch=0.3;zoom=0.55}}')
        pg.wait_for_timeout(1500)
        # driven = bones move between two moments
        a=pg.evaluate('MODELS.map(M=>{const v=new (M.grp.position.constructor)();const o=[];M.grp.traverse(x=>{if(x.isBone){x.getWorldPosition(v);o.push(v.x,v.y,v.z)}});return o})')
        pg.wait_for_timeout(300)
        c=pg.evaluate('MODELS.map(M=>{const v=new (M.grp.position.constructor)();const o=[];M.grp.traverse(x=>{if(x.isBone){x.getWorldPosition(v);o.push(v.x,v.y,v.z)}});return o})')
        mv=[max(abs(x-y) for x,y in zip(A,C)) for A,C in zip(a,c)]
        nan=[any(x!=x for x in C) for C in c]
        print(mo,'bone movement',[round(m,2) for m in mv],'NaN',nan)
        f=S+f'glb_{mo}.png';pg.screenshot(path=f,clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]});shots.append(f)
    print('errors:',errs[:5]);b.close()
ims=[Image.open(f) for f in shots];w,h=ims[0].size;o=Image.new('RGB',(w//2*3,h//2))
for i,im in enumerate(ims):o.paste(im.resize((w//2,h//2)),(i*w//2,0))
o.save(S+'glbcheck.png')
