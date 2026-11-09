from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':850});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click();yaw=0.7}');pg.wait_for_timeout(400)
    pg.mouse.click(600,300)
    pg.evaluate('()=>{$("charSel").value="sergal2";$("charSel").dispatchEvent(new Event("change"))}');pg.wait_for_timeout(500)
    pg.keyboard.down('ArrowUp');pg.wait_for_timeout(1500);print('arrow:',pg.evaluate('mode'))
    pg.keyboard.up('ArrowUp');pg.keyboard.down('w');pg.wait_for_timeout(2000);print('w:',pg.evaluate('mode'),pg.evaluate('HEAD.toFixed(2)'))
    pg.keyboard.up('w');pg.keyboard.down('s');pg.wait_for_timeout(150);pg.keyboard.up('s')
    pg.wait_for_timeout(100);print('turn:',pg.evaluate('TURNM&&TURNM.kind'))
    for k in range(40):
        pg.wait_for_timeout(100)
        if not pg.evaluate('!!TURNM'):break
    pg.wait_for_timeout(800);print('after:',pg.evaluate('mode'),pg.evaluate('HEAD.toFixed(2)'))
    pg.keyboard.down('d');pg.wait_for_timeout(1200);pg.keyboard.up('d');pg.wait_for_timeout(1000);print('d:',pg.evaluate('HEAD.toFixed(2)'))
    pg.screenshot(path=S+'s2game.png')
    for ch in ['sergal','robot','sergal2','sergal']:
        pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").dispatchEvent(new Event("change"))}}');pg.wait_for_timeout(400)
    pg.evaluate('()=>document.querySelector(\'#tierSw [data-t="dev"]\').click()');
    pg.evaluate('()=>{$("charSel").value="sergal2";$("charSel").dispatchEvent(new Event("change"))}');pg.wait_for_timeout(600)
    print('groups:',pg.evaluate('[...document.querySelectorAll("#sliders legend")].map(l=>l.textContent)'))
    print(errs);b.close()
