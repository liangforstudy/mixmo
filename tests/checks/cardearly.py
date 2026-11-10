from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700});pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>document.querySelector(\'#rendSw [data-r="three"]\').click()');pg.wait_for_timeout(2500)
    pg.set_input_files('#mdlFile',S+'real/female_sergal_body.glb')
    seen=None
    for i in range(400):
        pg.wait_for_timeout(50)
        msg=pg.evaluate('$("mdlMsg").textContent');cards=pg.evaluate('document.querySelectorAll(".mdlCard").length')
        if 'GPU' in msg:seen=(msg,cards);break
    print('during warm-up:',seen)
    b.close()
