import sys,math
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").onchange()}')
    pg.set_input_files('#mdlFile',S+'real/'+F+'.glb')
    for i in range(120):
        pg.wait_for_timeout(500)
        if pg.evaluate("MODELS.length===1&&!MLOAD.busy"):break
    pg.click('.mdlCard [data-g="place"] [data-v="in"]');pg.click('.mdlCard [data-g="move"] [data-v="move"]')
    for mo in ['idle','walk','run']:
        pg.evaluate(f'()=>{{$("modeSel").value="{mo}";$("modeSel").onchange();if(!playing)$("play").onclick()}}');pg.wait_for_timeout(2500)
        rows=pg.evaluate('''()=>new Promise(res=>{const out=[],T=R3.T,v=new T.Vector3();let last=null;
          const id=setInterval(()=>{if(out.length>=150){clearInterval(id);res(out);return}const sig=REC.legs.phBL.pts[2].join();if(sig===last)return;last=sig;const r={};
           for(const [sd,k] of [["L","phBL"],["R","phBR"]]){const M=MODELS[0],L=M.mv.legs[sd];L.ft.getWorldPosition(v);{const rq=M.root.getWorldQuaternion(new T.Quaternion()),rw=rq.clone().multiply(M.mv.RW.get(L.ft)),W=L.ft.getWorldQuaternion(new T.Quaternion());
            const t=L.toe.clone().multiplyScalar(M.grp.scale.x).applyQuaternion(rq).applyQuaternion(rw.invert()).applyQuaternion(W);v.add(t)}const pw=REC.legs[k].pts[2];
            r[sd]=[v.x+POS[0],v.y-groundW(v.x+POS[0],v.z+POS[1]),v.z+POS[1],pw[0]+POS[0],pw[1],pw[2]+POS[1]]}
           out.push(r)},5)})''')
        for sd in ['L','R']:
            slide=0;minh=1e9;maxh=-1e9;n=0
            for a,c in zip(rows,rows[1:]):
                A,C=a[sd],c[sd]
                his=math.hypot(C[3]-A[3],C[5]-A[5])
                minh=min(minh,A[1])
                if his<0.05:
                    n+=1;slide=max(slide,math.hypot(C[0]-A[0],C[2]-A[2]))
            print(mo,sd,'ball min height %.2f'%minh,'planted frames',n,'worst model slide %.3f'%slide)
    print('rest ankle height (world):',pg.evaluate('MODELS[0].mv.legs.L.ankleH*MODELS[0].grp.scale.x'))
    print(errs[:3]);b.close()
