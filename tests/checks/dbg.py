from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':420,'height':760})
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1200)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();$("charSel").value="robot";$("charSel").onchange();$("modeSel").value="run4dog";$("modeSel").onchange();if(!playing)$("play").onclick()}')
    pg.wait_for_timeout(3000);pg.evaluate('()=>{if(playing)$("play").onclick();yaw=2.45;pitch=0.06;zoom=3.2;panY=-150;panX=-60}');pg.wait_for_timeout(300)
    r=pg.evaluate('''()=>{const out=[];const gs={};
     prims.forEach((q,i)=>{if(q.t!==5)return;const area=(()=>{let s=0;const P=q.pts;for(let k=1;k<P.length-1;k++){const c=cross3(sub3(P[k],P[0]),sub3(P[k+1],P[0]));s+=Math.hypot(...c)/2}return s})();
       const f=proj(add(q.a,q.fn)).z-proj(q.a).z;(gs[q.g]||(gs[q.g]=[])).push({i,area:Math.round(area),n:q.pts.length,f:+f.toFixed(3),z:+proj(q.a).z.toFixed(1)})});
     return Object.entries(gs).map(([g,l])=>({g,big:l.filter(x=>x.area>300).length,caps:l.filter(x=>x.n>4).map(x=>[x.area,x.f,x.z]),cnt:l.length,maxA:Math.max(...l.map(x=>x.area))}))}''')
    for x in r:print(x)
    b.close()
