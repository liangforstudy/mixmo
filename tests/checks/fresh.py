from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#uiSw [data-ui="desk"]\').click();localStorage.setItem("tripodCollapsed","[\\"x\\"]");localStorage.setItem("tripodSplitPct","30");localStorage.setItem("w3schoolsThing","keep me")}')
    print('before:',pg.evaluate('()=>Object.keys(localStorage).sort()'))
    pg.evaluate('()=>$("freshGo").scrollIntoView()');pg.click('#freshGo');pg.wait_for_timeout(200)
    el=pg.query_selector('#fresh');el.screenshot(path=S+'fresh.png')
    with pg.expect_navigation():pg.click('#freshYes')
    pg.wait_for_timeout(1000)
    print('after :',pg.evaluate('()=>Object.keys(localStorage).sort()'),'| renderer',pg.evaluate('R3.want'),'| desktop class',pg.evaluate('document.documentElement.classList.contains("desk")'))
    print(errs);b.close()
