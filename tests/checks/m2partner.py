from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1100,'height':850});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="robot";$("charSel").onchange()}')
    pg.set_input_files('#mdlFile',S+'real/baller_fox_body.glb')
    for i in range(120):
        pg.wait_for_timeout(500)
        if pg.evaluate('!!MDL.info'):break
    pg.click('#mdlMove [data-m="move"]');pg.wait_for_timeout(400)
    print('char after Copies:',pg.evaluate('CHAR'),'|',pg.evaluate('$("mdlMoveNote").textContent'))
    pg.evaluate('()=>{$("modeSel").value="walk";$("modeSel").onchange();if(!playing)$("play").onclick();yaw=0.25;pitch=0.25;zoom=0.8}');pg.wait_for_timeout(2000)
    box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
    pg.screenshot(path=S+'partner_walk.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    pg.click('text=90° ↷');pg.wait_for_timeout(700)
    pg.screenshot(path=S+'partner_turn.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    pg.wait_for_timeout(2500)
    pg.click('#mdlPlace [data-p="in"]');pg.click('text=Spin');pg.wait_for_timeout(1500)
    pg.screenshot(path=S+'in_spin.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    pg.click('text=Spin');pg.wait_for_timeout(2500)
    # switch to robot while moving: back to a statue pose, no errors
    pg.evaluate('()=>{$("charSel").value="robot";$("charSel").dispatchEvent(new Event("change"))}');pg.wait_for_timeout(800)
    print('robot:',pg.evaluate('$("mdlMoveNote").textContent'),'posed',pg.evaluate('MDL.mv.posed'))
    pg.evaluate('()=>{$("charSel").value="sergal2";$("charSel").dispatchEvent(new Event("change"))}');pg.wait_for_timeout(500)
    # game: run with W
    pg.evaluate('()=>document.querySelector(\'#tierSw [data-t="game"]\').click()');pg.wait_for_timeout(400)
    pg.mouse.click(400,300);pg.keyboard.down('w');pg.wait_for_timeout(2000)
    pg.screenshot(path=S+'game_run.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    pg.keyboard.up('w');pg.wait_for_timeout(1500)
    print('game mode',pg.evaluate('mode'),'visible in game:',pg.is_visible('#mdlMove'))
    print(errs[:5]);b.close()
from PIL import Image
fs=['partner_walk','partner_turn','in_spin','game_run'];ims=[Image.open(S+f+'.png') for f in fs];w,h=ims[0].size
o=Image.new('RGB',(w,h));[o.paste(im.resize((w//2,h//2)),((i%2)*(w//2),(i//2)*(h//2))) for i,im in enumerate(ims)];o.save(S+'partner_grid.png')
