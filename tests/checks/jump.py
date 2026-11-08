from playwright.sync_api import sync_playwright
import sys
JS=r'''([m,n])=>{if(playing)$("play").onclick();STEPBLEND=true;$("charSel").value="robot";$("charSel").onchange();
 const fb=()=>{const tg=P[mode],u=ease(blendU);for(const k in tg)cur[k]=from[k]+(tg[k]-from[k])*u;cur.bobWave=Math.sin(2*Math.PI*phase*Math.round(cur.bobMul||1));springStep(1/60);flipStep()};
 const sel=$("modeSel");sel.value=m;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;
 for(let i=0;i<60;i++){advance(1/96);fb();buildRobot({...cur},phase)}
 const knees=()=>prims.filter(q=>q.t===1).map(q=>q.a);   // joint balls
 let prev=null,out=[];
 for(let i=0;i<n;i++){advance(1/96);fb();buildRobot({...cur},phase);
  const k=ROBFEET.map(f=>f.p);const J=LASTHIPS?LASTHIPS:[];
  const pts=prims.filter(q=>q.t===1).map(q=>q.a);
  if(prev&&prev.length===pts.length){let w=0,wi=0;pts.forEach((p,j)=>{const d=Math.hypot(p[0]-prev[j][0],p[1]-prev[j][1],p[2]-prev[j][2]);if(d>w){w=d;wi=j}});out.push([i,+w.toFixed(2),Math.floor(((phase%1)+1)%1*24)+1])}
  prev=pts}
 out.sort((a,b)=>b[1]-a[1]);return out.slice(0,6)}'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in sys.argv[1:]:
        pg=b.new_page();pg.goto('http://localhost:8765/'+f);pg.wait_for_timeout(500)
        for m in ['run','walk','runTail','walk2','dino']:
            r=pg.evaluate(JS,[m,192]);print(f,m,'biggest joint moves per 1/96 cycle [step, units, frame]:',r[:4])
        pg.close()
    b.close()
