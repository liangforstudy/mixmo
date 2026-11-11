const {open}=require('./lib');
(async()=>{const file=process.argv[2];const {b,pg,errs}=await open(file,{w:600,h:900});
 await pg.waitForTimeout(800);
 await pg.evaluate(()=>document.querySelector('#rendSw [data-r]:not([data-r="three"])').click());await pg.waitForTimeout(300);
 await pg.selectOption('#charSel','robot');await pg.evaluate(()=>{const s=$("modeSel");s.value="walk";s.onchange()});await pg.waitForTimeout(1500);
 await pg.evaluate(()=>{window.requestAnimationFrame=()=>0});
 await pg.click('#tF');const rows=[];
 for(let i=0;i<230;i++){const r=await pg.evaluate(()=>{frame(last+16.67);
   const st=$("stText").textContent,m=st.match(/Rise onto front end, frame (\d+)\/53/);
   const by={};for(const q of prims){if(q.t!==5||q.col!==RLOOK.pawB)continue;(by[q.nm]=by[q.nm]||[]).push(...q.pts)}
   const paws=Object.entries(by).map(([n,pts])=>{const lo=Math.min(...pts.map(v=>v[1])),c=pts.reduce((a,v)=>[a[0]+v[0]/pts.length,a[1]+v[2]/pts.length],[0,0]);
     // world spot: undo his heading and add travel
     const w=rotY([c[0],0,c[1]],0);return{n,lo:+lo.toFixed(1),x:c[0],z:c[1]+groundOff}});
   return{f:m?+m[1]:0,go:+groundOff.toFixed(1),paws,done:!WALKOVER&&!FLIP}});
  if(r.f)rows.push(r);if(r.done&&rows.length)break}
 const prev={};let maxSlide=0;
 for(const r of rows){const s=r.paws.map(p=>{let sl='';if(prev[p.n]&&p.lo<4){const d=Math.hypot(p.x-prev[p.n].x,p.z-prev[p.n].z);sl=d.toFixed(2);if(r.f>9&&r.f<45)maxSlide=Math.max(maxSlide,d)}prev[p.n]=p;return p.lo+(sl?'/'+sl:'')});
  if(r.f%4===1||s.some(x=>+String(x).split('/')[1]>1))console.log('rise',String(r.f).padStart(2),'travel',r.go,'| red paws low/slide:',s.join('  '))}
 console.log('worst slide/frame of a red paw on the ground, rise frames 10-44:',maxSlide.toFixed(2));console.log(errs);await b.close()})();
