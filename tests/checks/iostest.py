from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    for dev in ['iPhone 13',None]:
        ctx=b.new_context(**p.devices[dev]) if dev else b.new_context(viewport={'width':1100,'height':800})
        pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
        print(dev,'accept =',pg.evaluate('$("mdlFile").getAttribute("accept")'))
        if dev:
            pg.set_input_files('#mdlFile',S+'glb/notglb.txt');pg.wait_for_timeout(4000)
            print(' wrong file msg:',pg.evaluate('$("mdlMsg").textContent'))
            pg.set_input_files('#mdlFile',S+'real/baller_fox_body.glb')
            for i in range(60):
                pg.wait_for_timeout(500)
                if pg.evaluate('!!MDL.info'):break
            print(' glb loaded:',pg.evaluate('MDL.info&&MDL.info.preset'),errs[:3])
        ctx.close()
    b.close()
