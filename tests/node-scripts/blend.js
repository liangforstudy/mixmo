const {open}=require('./lib');
(async()=>{const {b,pg}=await open(process.argv[2]);
 await pg.evaluate(()=>{window.requestAnimationFrame=()=>0;render=()=>{};drawGait=()=>{}});
 const r=await pg.evaluate(()=>{const s=$("charSel");s.value="sergal";s.onchange();
  // use the new run phases in both files, so only the blending differs
  Object.assign(P.run,{phF:.76,phBL:.15,phBR:.51});
  const out={};let t=last;const go=m=>{const ms=$("modeSel");ms.value=m;ms.onchange()};
  const step=n=>{const tr=[];for(let i=0;i<n;i++){t+=16.67;frame(t);tr.push({phF:cur.phF,paw:[...REC0()]})}return tr};
  const REC0=()=>{const L=LEGS[0];return L.lastPaw||[0,0,0]};
  for(const [a,c] of [["walk","run"],["run","walk"],["idle","run"],["run","idle"]]){go(a);step(150);go(c);
   const tr=[];let prevPh=cur.phF,maxD=0,path=0;for(let i=0;i<90;i++){t+=16.67;frame(t);const d=cur.phF-prevPh;path+=Math.abs(d-Math.round(d));prevPh=cur.phF}
   out[a+" -> "+c]="tail-leg timing moved "+path.toFixed(2)+" of a cycle during the switch (end "+cur.phF.toFixed(2)+")"}
  return out});
 for(const k in r)console.log(k.padEnd(14),r[k]);await b.close()})();
