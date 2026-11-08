import math
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':1200,'height':900},has_touch=True,is_mobile=True);pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#uiSw [data-ui="touch"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click();$("charSel").value="robot";$("charSel").dispatchEvent(new Event("change"));yaw=0.7}');pg.wait_for_timeout(600)
    print('panel shown for robot:',pg.evaluate('!!$("formsBox").offsetParent'),'| T-pose button shown while standing:',pg.evaluate('!!$("emoteBtn").offsetParent'))
    cx,cy=pg.evaluate('()=>{const r=$("stickZone").getBoundingClientRect();return [r.left+r.width/2,r.top+r.height*0.6]}')
    def stick(px,ms):
        pg.mouse.move(cx,cy);pg.mouse.down();pg.mouse.move(cx,cy-px,steps=3);pg.wait_for_timeout(ms);m=pg.evaluate('mode');return m
    for px,label in [(14,'small push (30%)'),(32,'medium push (67%)'),(46,'full push (96%)')]:
        print(f'  {label:18s}: {stick(px,1200)}');pg.mouse.up();pg.wait_for_timeout(700)
    pg.click('#fMid [data-m="roo"]');print('  between = Kangaroo, medium push:',stick(32,1200));pg.mouse.up();pg.wait_for_timeout(600)
    pg.click('#fWalk [data-m="walk2"]');print('  walk = on two, small push:',stick(14,1200));pg.mouse.up();pg.wait_for_timeout(600)
    pg.select_option('#fRun','run6');print('  run = all six, full push:',stick(46,3000))
    h0=pg.evaluate('HEAD');d0=pg.evaluate('DIR');pg.mouse.move(cx,cy+46,steps=2);pg.wait_for_timeout(3500)
    tr=pg.evaluate('()=>[HEAD,DIR]');p0=pg.evaluate('[...POS]');pg.wait_for_timeout(800);p1=pg.evaluate('[...POS]')
    v=pg.evaluate('a=>{const v=rotY([a[0],0,a[1]],yaw);return v[2]}',[p1[0]-p0[0],p1[1]-p0[1]])
    print(f'  all six, flick back: ends swapped (DIR {d0} -> {tr[1]}), now travelling toward camera {v:.0f} (positive = toward = correct)')
    pg.mouse.up();pg.wait_for_timeout(2500)
    pg.screenshot(path=S+'forms.png',clip={'x':0,'y':0,'width':760,'height':900})
    pg.click('#emoteBtn');pg.wait_for_timeout(1500);print('  T-pose tapped:',pg.evaluate('mode'));stick(20,800);pg.mouse.up();print('  moved -> T-pose ended:',pg.evaluate('!EMOTE'),pg.evaluate('mode'))
    pg.wait_for_timeout(1500)
    # Ctrl on the keyboard
    pg.mouse.click(1000,200);pg.keyboard.down('Control');pg.keyboard.down('ArrowUp');pg.wait_for_timeout(1200);print('  Ctrl + Up arrow:',pg.evaluate('mode'));pg.keyboard.up('ArrowUp')
    pg.keyboard.down('d');pg.wait_for_timeout(800);print('  Ctrl + D:',pg.evaluate('mode'),'| page still here (no bookmark dialog):',pg.evaluate('document.title'));pg.keyboard.up('d');pg.keyboard.up('Control')
    pg.evaluate('()=>{$("charSel").value="sergal";$("charSel").dispatchEvent(new Event("change"))}');pg.wait_for_timeout(300)
    print('sergal: panel hidden',pg.evaluate('!$("formsBox").offsetParent'),'| T-pose hidden',pg.evaluate('!$("emoteBtn").offsetParent'),errs)
    b.close()
