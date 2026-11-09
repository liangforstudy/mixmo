import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
shots=[(m,ph,yw) for m in ['idle','walk','run','gallop'] for ph,yw in [(0.0,1.57),(0.25,0.7)]]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':520,'height':700})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1200)
    pg.evaluate('()=>{$("charSel").value="sergal2";$("charSel").onchange()}')
    for m,ph,yw in shots:
        pg.evaluate(f'()=>{{$("modeSel").value="{m}";$("modeSel").onchange();if(!playing)$("play").onclick()}}');pg.wait_for_timeout(1500)
        pg.evaluate(f'()=>{{if(playing)$("play").onclick();yaw={yw};pitch=0.15;zoom=1.2}}');pg.wait_for_timeout(300)
        box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
        pg.screenshot(path=S+f's2_{m}_{ph}.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':min(box[3],460)})
    print(errs[:5]);b.close()
