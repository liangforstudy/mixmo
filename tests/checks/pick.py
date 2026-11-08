from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':900},has_touch=False);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();$("charSel").value="robot";$("charSel").onchange();$("modeSel").value="run4dog";$("modeSel").onchange();if(!playing)$("play").onclick()}')
    pg.wait_for_timeout(2500);pg.evaluate('()=>{if(playing)$("play").onclick();yaw=2.45;pitch=0.06;zoom=3.2;panY=-150;panX=-60}')
    pg.evaluate('()=>document.querySelector(\'#pickSw [data-p="on"]\').click()');pg.wait_for_timeout(200)
    print('hint:',pg.evaluate('$("pickOut").textContent'))
    # tap the middle of the body box's back-end face: find its screen centre
    c=pg.evaluate('()=>{const o=DRAWN.find(o=>o.q.cap&&o.q.nm==="Body");const p=proj(o.q.a);const r=cv.getBoundingClientRect();return [r.left+p.x,r.top+p.y]}')
    pg.mouse.click(c[0],c[1]);pg.wait_for_timeout(300)
    print('1:',pg.evaluate('$("pickOut").textContent'))
    for yw in [2.9,3.6,5.0]:
        pg.evaluate(f'()=>{{yaw={yw}}}');pg.wait_for_timeout(300);print(f'yaw {yw}:',pg.evaluate('$("pickOut").textContent'))
    # a front leg from the side, then rotate so the body hides it
    pg.evaluate('()=>{yaw=1.57;pitch=0.2;zoom=2;panX=0;panY=-60}');pg.wait_for_timeout(300)
    c=pg.evaluate('()=>{const o=DRAWN.filter(o=>/Front/i.test(o.q.nm||"")).pop()||DRAWN[3];const p=proj(o.q.a);const r=cv.getBoundingClientRect();return [r.left+p.x,r.top+p.y,o.q.nm]}')
    pg.mouse.click(c[0],c[1]);pg.wait_for_timeout(300);print('2:',pg.evaluate('$("pickOut").textContent'))
    pg.evaluate("()=>{yaw=2.6;pitch=0.1;zoom=2.6;panY=-120}");pg.wait_for_timeout(300);print('rotated:',pg.evaluate('$("pickOut").textContent'))
    box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
    pg.screenshot(path=S+'pick.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':min(box[3],380)})
    pg.evaluate('()=>$("pickBox").scrollIntoView()');pg.query_selector('#pickBox').screenshot(path=S+'pickbox.png')
    print('names sample:',pg.evaluate('()=>[...new Set(prims.map(q=>q.nm))]'))
    pg.evaluate('()=>{$("charSel").value="sergal";$("charSel").onchange()}');pg.wait_for_timeout(300)
    print('sergal names:',pg.evaluate('()=>[...new Set(prims.map(q=>q.nm))]'))
    print(errs);b.close()
