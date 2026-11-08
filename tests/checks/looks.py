from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':520,'height':700});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type in('error','warning') else None)
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
    combos=[dict(style=s,limbs=l,outline=o,shadow=sh,ground=g) for s in ['toon','soft'] for l in ['smooth','capsule'] for o in ['on','off'] for sh in ['real','soft'] for g in ['solid','grid']]
    import json
    for i,c in enumerate(combos):
        pg.evaluate(f'()=>{{Object.assign(R3.look,{json.dumps(c)});r3applyLook();$("charSel").value="{"robot" if i%2 else "sergal"}";$("charSel").onchange()}}');pg.wait_for_timeout(250)
    pg.evaluate('()=>{Object.assign(R3.look,{style:"soft",limbs:"smooth",outline:"on",shadow:"real",ground:"solid"});r3applyLook();$("charSel").value="sergal";$("charSel").onchange()}');pg.wait_for_timeout(1200)
    box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
    pg.screenshot(path=S+'soft.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':min(box[3],460)})
    print('combos',len(combos),'segments',pg.evaluate('R3.segG.instanceCount'),'errors',errs[:5]);b.close()
