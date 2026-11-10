import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    for F in sys.argv[1:]:
        pg=b.new_page(viewport={'width':900,'height':700});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8765/'+F);pg.wait_for_timeout(800)
        pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click()}');pg.wait_for_timeout(3000)
        # hide the view the way a pulled-down drawer does (view too small to draw), then add the model
        pg.evaluate('()=>{$("view").style.display="none"}');pg.wait_for_timeout(400)
        pg.set_input_files('#mdlFile',S+'real/baller_fox_body.glb')
        for i in range(160):
            pg.wait_for_timeout(500)
            if pg.evaluate('MODELS.length===1&&!MLOAD.busy&&$("mdlMsg").textContent===""'):break
        pg.wait_for_timeout(1500)
        r=pg.evaluate('''()=>new Promise(res=>{const n0=R3.rd.info.programs.length,k0=new Set(R3.rd.info.programs.map(q=>q.cacheKey)),o=window.r3render;let mx=0,n=0,c0=0;
            window.r3render=function(){const t=performance.now();const v=o.apply(this,arguments);const dt=performance.now()-t;if(R3.rd.info.render.calls>0){n++;mx=Math.max(mx,dt)}return v};
            $("view").style.display="";setTimeout(()=>res([n0,R3.rd.info.programs.length,mx.toFixed(0),n,R3.rd.info.programs.filter(q=>!k0.has(q.cacheKey)).map(q=>q.name+' '+q.cacheKey.slice(0,40).replace(/\\s+/g,' '))]),2500)})''')
        print(F,'programs before showing',r[0],'after first frame',r[1],'slowest frame ms',r[2],'frames',r[3],errs[:2]);print('\n'.join(r[4]))
        pg.close()
    b.close()
