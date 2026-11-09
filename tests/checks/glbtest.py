import json
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1200,'height':850});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type in('error','warning') else None)
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    # start in 2D to test loading three on demand
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();$("charSel").value="sergal2";$("charSel").onchange();$("modeSel").value="idle";$("modeSel").onchange()}')
    for f in ['foxlike','mixamo','static']:
        pg.set_input_files('#mdlFile',S+'glb/'+f+'.glb')
        for i in range(60):
            pg.wait_for_timeout(500)
            if not pg.evaluate('MDL.busy'):break
        print(f,'msg:',pg.evaluate('$("mdlMsg").textContent'),'| 3d btn hidden:',pg.evaluate('$("mdl3d").hidden'))
        print(json.dumps(pg.evaluate('MDL.info'))[:900])
    print('legs:',pg.evaluate('[...document.querySelectorAll("#mdlInfo p")].map(p=>p.textContent)'))
    pg.set_input_files('#mdlFile',S+'glb/foxlike.glb');pg.wait_for_timeout(1500)
    print('legs fox:',[t for t in pg.evaluate('[...document.querySelectorAll("#mdlInfo p")].map(p=>p.textContent)') if 'leg' in t.lower()])
    pg.click('#mdlTo3d');pg.wait_for_timeout(4000)
    pg.evaluate('()=>{yaw=0.4;pitch=0.2;zoom=0.8}');pg.wait_for_timeout(600)
    pg.screenshot(path=S+'glb_beside.png')
    pg.click('#mdlBones [data-b="on"]');pg.click('#mdlPlace [data-p="in"]');pg.wait_for_timeout(600)
    pg.screenshot(path=S+'glb_in.png')
    pg.click('#mdlDel');pg.wait_for_timeout(400);print('after remove:',pg.evaluate('!!MDL.grp'),pg.evaluate('R3.sc.children.length'))
    print([e for e in errs if 'GPU stall' not in e][:8]);b.close()
