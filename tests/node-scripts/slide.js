const {open}=require('./lib');
(async()=>{const {b,pg,errs}=await open(process.argv[2]);
 await pg.evaluate(([a,c])=>{window.TURNS=a;window.ROT=c;window.requestAnimationFrame=()=>0;render=()=>{};drawGait=()=>{}},[process.argv[3]==="1",process.argv[4]==="1"]);
 const out=await pg.evaluate(()=>{const s=$("charSel");s.value="sergal2";s.onchange();const res={};
  for(const pre of ['sergal','fox'])for(const ter of ['flat','hills'])for(const m of ['idle','walk','run']){setPreset2(pre);TER.type=ter;
   const ms=$("modeSel");ms.value=m;ms.onchange();let t=last;for(let i=0;i<120;i++){t+=16.67;frame(t)}
   const prev={};let worst=0,nan=0;
   for(let i=0;i<400;i++){if(TURNS){if(i===100)$("tR").click();if(i===250)$("tU").click()}t+=16.67;frame(t);
    for(const k of ['phBL','phBR']){const L=REC.legs[k];if(!L||!L.pts[2].every(Number.isFinite)){nan++;continue}const p=L.pts[2],gy=groundW(p[0]+POS[0],p[2]+POS[1]);
     const q=ROT?rotY(p,HEAD):p,w=[q[0]+POS[0],p[1],q[2]+POS[1]];if(p[1]-gy<3.25){if(prev[k])worst=Math.max(worst,Math.hypot(w[0]-prev[k][0],w[2]-prev[k][2]));prev[k]=w}else prev[k]=null}}
   res[pre+'/'+ter+'/'+m]=[+worst.toFixed(3),nan]}
  return res});
 for(const k in out)console.log(k.padEnd(20),'worst planted slide/frame',out[k][0],'nan',out[k][1]);console.log(errs);await b.close()})();
