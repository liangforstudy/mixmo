from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700})
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").onchange();$("modeSel").value="idle";$("modeSel").onchange()}')
    for f in ['female_sergal_body','baller_fox_body']:
        pg.evaluate('()=>{while(MODELS.length)mdlRemove(MODELS[0]);mdlUI()}')
        pg.set_input_files('#mdlFile',S+'real/'+f+'.glb')
        for i in range(120):
            pg.wait_for_timeout(500)
            if pg.evaluate('MODELS.length===1&&!MLOAD.busy'):break
        js='''(()=>{const M=MODELS[0],T=R3.T,m=M.rig,w=b=>b.getWorldPosition(new T.Vector3());const fw=new T.Vector3(0,0,1).applyAxisAngle(new T.Vector3(0,1,0),HEAD);
          const tilt=(a,b)=>{const v=w(b).sub(w(a));return (Math.atan2(v.dot(fw),v.y)*57.3).toFixed(1)};
          return {hips_chest:tilt(m.hips,m.chest),chest_neck:tilt(m.chest,m.neck),neck_head:tilt(m.neck,m.head)}})()'''
        pg.wait_for_timeout(800);st=pg.evaluate(js)
        pg.click('.mdlCard [data-g="move"] [data-v="move"]');pg.wait_for_timeout(1500);mv=pg.evaluate(js)
        print(f,'statue',st,'| copying idle',mv)
    print('his neck dir',pg.evaluate('(()=>{const h=REC.head;return [0,1,2].map(i=>(h.top[i]-h.base[i]).toFixed(1))})()'))
    b.close()
