from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1100,'height':850})
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click()}')
    pg.set_input_files('#mdlFile',S+'real/female_sergal_body.glb')
    for i in range(120):
        pg.wait_for_timeout(500)
        if pg.evaluate('!!MDL.info'):break
    pg.click('#mdlPlace [data-p="in"]');pg.evaluate('()=>{yaw=0.3;pitch=0.05;zoom=2.6;panY=-40}');pg.wait_for_timeout(1500)
    box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
    pg.screenshot(path=S+'fem_close.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    print(pg.evaluate('''()=>{const o=[];MDL.root.traverse(m=>{if(m.isMesh)for(const mt of [].concat(m.material))o.push([m.name,mt.name,!!mt.map,mt.map?mt.map.image&&mt.map.image.width:0,mt.color.getHexString(),mt.transparent,mt.alphaTest])});return o}'''))
    b.close()
