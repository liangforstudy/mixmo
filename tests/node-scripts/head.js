const {open}=require('./lib');
(async()=>{const {b,pg}=await open(process.argv[2],{});
 await pg.evaluate(()=>{window.requestAnimationFrame=()=>0});const r=await pg.evaluate(()=>{const s=$("charSel");s.value="sergal2";s.onchange();const out={};
  for(const p of (typeof setPreset2==='function'?['sergal','fox']:['sergal'])){if(typeof setPreset2==='function')setPreset2(p);
   const ms=$("modeSel");ms.value="idle";ms.onchange();let t=last;for(let i=0;i<30;i++){t+=16.7;frame(t)}charDef().build({...cur},phase);const hip=REC.legs.phBL.hip[1],gy=REC.legs.phBL.pts[2][1]-3.2;
   out[p]={hip:+(hip-gy).toFixed(1),headBase:REC.head&&+(REC.head.base[1]-gy).toFixed(1),headO:REC.head&&+(REC.head.o[1]-gy).toFixed(1)}}return out});
 console.log(JSON.stringify(r));await b.close()})();
