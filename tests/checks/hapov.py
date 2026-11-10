from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(**p.devices['iPhone 13']);pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script('''window.__lab=0;window.__ov=0;document.addEventListener("click",e=>{if(e.target&&e.target.id==="hapLb")window.__lab++;if(e.target&&e.target.classList&&e.target.classList.contains("hapOv"))window.__ov++},true)''')
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1200)
    print('buttons',pg.evaluate('document.querySelectorAll("button").length'),'with switch',pg.evaluate('document.querySelectorAll("button>.hapOv").length'),'nohaptic',pg.evaluate('document.querySelectorAll("button[data-nohaptic]").length'))
    def tap(sel,label):
        lab0,ov0=pg.evaluate('[__lab,__ov]');pg.tap(sel);pg.wait_for_timeout(250);lab1,ov1=pg.evaluate('[__lab,__ov]')
        print(f'{label:28s} switch hit {ov1-ov0}, backup label clicks {lab1-lab0}')
    p0=pg.evaluate('playing');tap('#play','play/pause');print('   playing changed:',p0!=pg.evaluate('playing'),'| play text:',pg.evaluate('$("play").textContent'),'| switch back:',pg.evaluate('!!$("play").querySelector(".hapOv")'))
    tap('#play','play/pause again')
    h0=pg.evaluate('HEAD_T');tap('text=90° ↷','turn 90');pg.wait_for_timeout(1500);print('   heading target changed:',abs(pg.evaluate('HEAD_T')-h0)>1)
    # a choice already chosen: no switch hit, no tick
    tap('#rendSw [data-r="canvas"]','renderer 2D (choice)')
    tap('#rendSw [data-r="canvas"]','renderer 2D again (no-op)')
    print('   focus after taps:',pg.evaluate('document.activeElement.tagName+"#"+document.activeElement.id+"."+document.activeElement.className'))
    # rewind: pause, step back with the button, step again - history must not be cut by the switch's change events
    pg.wait_for_timeout(1500);pg.tap('#play');pg.wait_for_timeout(200)
    n=pg.evaluate('HIST.length');tap('#prevF','step back');tap('#prevF','step back');print('   rewound HPOS',pg.evaluate('HPOS'),'hist kept',pg.evaluate('HIST.length')==n)
    tap('#nextF','step forward');print('   HPOS',pg.evaluate('HPOS'),'hist kept',pg.evaluate('HIST.length')==n)
    pg.keyboard.press('ArrowLeft');pg.wait_for_timeout(200);print('   arrow key still steps: HPOS',pg.evaluate('HPOS'))
    # the tier switch and the model card buttons (made later)
    tap('#tierSw [data-t="dev"]','Mode: Dev');print('   tier',pg.evaluate('TIER'))
    pg.evaluate('()=>document.querySelector(\'#rendSw [data-r="three"]\').click()')
    pg.set_input_files('#mdlFile',S+'glb/foxlike.glb')
    for i in range(60):
        pg.wait_for_timeout(500)
        if pg.evaluate('MODELS.length===1&&!MLOAD.busy'):break
    print('   card buttons with switch:',pg.evaluate('[...document.querySelectorAll(".mdlCard button")].map(b=>!!b.querySelector(".hapOv")).join()'))
    pg.locator('.mdlCard [data-g="place"] [data-v="in"]').scroll_into_view_if_needed();tap('.mdlCard [data-g="place"] [data-v="in"]','model: in his place');print('   place',pg.evaluate('MODELS[0].place'))
    print(errs[:5]);ctx.close()
    ctx=b.new_context(viewport={'width':1100,'height':800});pg=ctx.new_page();pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    print('desktop: switches',pg.evaluate('document.querySelectorAll(".hapOv").length'));b.close()
