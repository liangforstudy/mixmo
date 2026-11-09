import json,sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1100,'height':850});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").onchange();$("modeSel").value="idle";$("modeSel").onchange()}')
    for f in ['baller_fox_body','female_sergal_body']:
        pg.set_input_files('#mdlFile',S+'real/'+f+'.glb')
        for i in range(120):
            pg.wait_for_timeout(500)
            if not pg.evaluate('MDL.busy') and pg.evaluate('!!MDL.info&&MDL.info.name.startsWith("%s")'%f):break
        pg.wait_for_timeout(1500)
        info=pg.evaluate('MDL.info');print(f,{k:info[k] for k in ['lying','preset','bones','height','tris']},pg.evaluate('$("mdlMsg").textContent'))
        print([t for t in pg.evaluate('[...document.querySelectorAll("#mdlInfo p")].map(p=>p.textContent)') if 'leg' in t.lower()][-1:])
        # where are the feet relative to the model origin (in his place)?
        pg.click('#mdlPlace [data-p="in"]');pg.wait_for_timeout(300)
        print('feet vs origin:',pg.evaluate('''()=>{const m=MDL.info.parts,T=R3.T,v=new T.Vector3();const g=n=>{let o=null;MDL.root.traverse(x=>{if(x.name===n)o=x});o.getWorldPosition(v);return [v.x.toFixed(1),v.z.toFixed(1)]};return {hips:g(m.hips),footL:g(m.footL),footR:g(m.footR)}}'''))
        pg.evaluate('()=>{yaw=0.6;pitch=0.15;zoom=1}');pg.wait_for_timeout(800)
        box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
        pg.screenshot(path=S+f'real_{f}.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]})
    print(errs[:5]);b.close()
