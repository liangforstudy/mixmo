import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':850});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/'+F);pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click();yaw=0.7}');pg.wait_for_timeout(400)
    pg.mouse.click(600,300)
    for ch in ['sergal','robot']:
        pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").dispatchEvent(new Event("change"))}}');pg.wait_for_timeout(500)
        pg.keyboard.down('w');pg.wait_for_timeout(2500);pg.keyboard.up('w');pg.keyboard.down('s');pg.wait_for_timeout(150);pg.keyboard.up('s')   # tap S: flick, then let go
        # after the turn ends: how far does he still travel?
        for k in range(40):
            pg.wait_for_timeout(100)
            if not pg.evaluate('!!TURNM'):break
        p0=pg.evaluate('[...POS]');t0=pg.evaluate('cur.travel');pg.wait_for_timeout(1500);p1=pg.evaluate('[...POS]')
        d=((p1[0]-p0[0])**2+(p1[1]-p0[1])**2)**0.5
        print(f'  {ch:6s}: at the end of the turn mode {pg.evaluate("mode")}, travel {t0:.0f}; moved {d:.0f} units in the 1.5 s after the turn')
        pg.wait_for_timeout(1500)
    print(errs);b.close()
