import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':850});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/'+F);pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click();yaw=0.7}');pg.wait_for_timeout(400)
    pg.mouse.click(600,300)
    pg.evaluate('''()=>{window.TL=[];const st=window.startTurn;window.startTurn=function(k,e){const r=st.apply(this,arguments);if(TURNM)TL.push([TURNM.label,!!TURNM.skid,Math.round(cur.travel),mode]);return r}}''')
    for ch in ['sergal','robot']:
        pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").dispatchEvent(new Event("change"))}}');pg.wait_for_timeout(500)
        for trial in range(3):
            pg.evaluate('TL.length=0');pg.keyboard.down('w');pg.wait_for_timeout(2500);pg.keyboard.up('w');pg.keyboard.down('s');pg.wait_for_timeout(2500);pg.keyboard.up('s');pg.wait_for_timeout(1200)
            print(f'  {ch} W then S: {pg.evaluate("TL")}')
    b.close()
