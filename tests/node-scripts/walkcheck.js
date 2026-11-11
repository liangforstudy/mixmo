const {open}=require('./lib');
(async()=>{const {b,pg}=await open(process.argv[2],{w:600,h:900});
 await pg.waitForTimeout(800);await pg.selectOption('#charSel','robot');await pg.waitForTimeout(500);
 const r=await pg.evaluate(()=>{window.requestAnimationFrame=()=>0;let lowAll=1e9,nm='',at=0;for(let i=0;i<400;i++){frame(last+16.67);for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a]))if(v[1]<lowAll){lowAll=v[1];nm=q.nm;at=i}}}return{mode,lowAll:+lowAll.toFixed(1),nm,at}});
 console.log('plain walking for 400 frames:',JSON.stringify(r));await b.close()})();
