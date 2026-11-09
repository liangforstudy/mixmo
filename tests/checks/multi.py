from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1100,'height':850});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    # timing chart: dev tier, switch characters, check the mini chart has been drawn on the live canvas
    pg.evaluate('()=>document.querySelector(\'#tierSw [data-t="dev"]\').click()');pg.wait_for_timeout(500)
    for ch in ['sergal2','robot','sergal']:
        pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").dispatchEvent(new Event("change"))}}');pg.wait_for_timeout(700)
        print(ch,'mini chart drawn:',pg.evaluate('(()=>{const g=document.querySelector(".gaitMini");return !!g&&g.isConnected&&g.width>0&&g===GMINI&&!!g._key})()'))
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").dispatchEvent(new Event("change"))}')
    pg.set_input_files('#mdlFile',[S+'real/baller_fox_body.glb',S+'real/female_sergal_body.glb',S+'glb/mixamo.glb'])
    for i in range(160):
        pg.wait_for_timeout(500)
        if pg.evaluate('MODELS.length===3&&!MLOAD.busy'):break
    print('models:',pg.evaluate('MODELS.map(M=>[M.info.name,M.place,M.info.preset])'),'cards',pg.evaluate('document.querySelectorAll(".mdlCard").length'))
    cards=pg.query_selector_all('.mdlCard')
    cards[0].query_selector('[data-g="move"] [data-v="move"]').click()
    cards[1].query_selector('[data-g="move"] [data-v="move"]').click()
    pg.evaluate('()=>{$("modeSel").value="walk";$("modeSel").onchange();if(!playing)$("play").onclick();yaw=0.15;pitch=0.3;zoom=0.55}');pg.wait_for_timeout(2500)
    box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
    pg.screenshot(path=S+'multi_a.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    print('slots:',pg.evaluate('MODELS.map(M=>M.place+" "+mdlSlot(M)[0])'))
    cards[1].query_selector('[data-g="place"] [data-v="in"]').click();pg.wait_for_timeout(300)
    cards[0].query_selector('[data-g="place"] [data-v="in"]').click();pg.wait_for_timeout(1200)
    print('after in-place swaps:',pg.evaluate('MODELS.map(M=>M.place)'))
    pg.screenshot(path=S+'multi_b.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    cards[2].query_selector('[data-a="del"]').click();pg.wait_for_timeout(300)
    print('after remove:',pg.evaluate('MODELS.length'),pg.evaluate('document.querySelectorAll(".mdlCard").length'),pg.evaluate('R3.sc.children.length'))
    print(errs[:5]);b.close()
from PIL import Image
a=Image.open(S+'multi_a.png');c=Image.open(S+'multi_b.png');w,h=a.size;o=Image.new('RGB',(w,h//2));o.paste(a.resize((w//2,h//2)),(0,0));o.paste(c.resize((w//2,h//2)),(w//2,0));o.save(S+'multi.png')
