const {open}=require('./lib');
(async()=>{const file=process.argv[2],shots=process.argv[3];const {b,pg,errs}=await open(file,{w:600,h:900});
 await pg.waitForTimeout(800);await pg.evaluate(()=>document.querySelector('#rendSw [data-r]:not([data-r="three"])').click());
 await pg.selectOption('#charSel','robot');await pg.waitForTimeout(800);
 await pg.evaluate(()=>{window.requestAnimationFrame=()=>0;yaw=Math.PI/2;pitch=0.08;let t=last;for(let i=0;i<60;i++){t+=16.67;frame(t)}});
 const log=[];
 for(let n=1;n<=3;n++){await pg.click('#tF');
  const r=await pg.evaluate(async([n,shots])=>{const out=[];let prev=null,k=0,after=0;
   for(let i=0;i<500;i++){frame(last+16.67);render();
    const by={};for(const q of prims){if(q.t!==5||(q.col!==RLOOK.pawB&&q.col!==RLOOK.pawA))continue;const key=q.nm+"|"+(q.col===RLOOK.pawB?"red":"blk");(by[key]=by[key]||[]).push(...q.pts)}
    const cen={};let lowAll=1e9;for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a]))lowAll=Math.min(lowAll,v[1])}
    for(const [kk,pts] of Object.entries(by))cen[kk]=[pts.reduce((a,v)=>a+v[0],0)/pts.length,pts.reduce((a,v)=>a+v[1],0)/pts.length,pts.reduce((a,v)=>a+v[2],0)/pts.length];
    let jump=0,jk="";if(prev)for(const kk in cen)if(prev[kk]){const d=Math.hypot(cen[kk][0]-prev[kk][0],cen[kk][1]-prev[kk][1],cen[kk][2]+groundOff-prev[kk][2]);if(d>jump){jump=d;jk=kk}}
    prev={};for(const kk in cen)prev[kk]=[cen[kk][0],cen[kk][1],cen[kk][2]+groundOff];
    out.push({i,st:$("stText").textContent,jump:+jump.toFixed(1),jk,low:+lowAll.toFixed(1),swap:SWAP});
    if(!WALKOVER&&!FLIP){if(++after>40)break}}
   return out},[n,shots]);
  log.push(r);
  const bad=r.filter(x=>x.jump>10||x.low<-6);
  console.log(`== Over #${n}: ${r.length} frames; frames with a paw jump >10 or something sinking >6: ${bad.length}`);
  for(const x of bad.slice(0,25))console.log(`  f${x.i} jump ${x.jump} (${x.jk}) low ${x.low} swap ${x.swap} | ${x.st}`);
 }
 console.log(errs);await b.close()})();
