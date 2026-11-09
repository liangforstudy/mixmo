from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':850});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click()}')
    print('box visible in game:',pg.is_visible('#mdlBox'))
    pg.set_input_files('#mdlFile',S+'glb/foxlike.glb')
    for i in range(60):
        pg.wait_for_timeout(500)
        if pg.evaluate('!!MDL.info'):break
    print('lying',pg.evaluate('MDL.info.lying'),'| visible text:',pg.inner_text('#mdlBox')[-300:])
    print('bones row visible:',pg.is_visible('#mdlBones'))
    print(errs);b.close()
