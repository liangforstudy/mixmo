const {chromium}=require('playwright');
async function run(file){const b=await chromium.launch();const pg=await b.newPage();
 await pg.addInitScript(()=>{window.requestAnimationFrame=()=>0});
 await pg.goto('file://'+file);await pg.waitForTimeout(800);
 const r=await pg.evaluate(()=>{playing=false;const res={};
  for(const [c,m] of [["sergal","walk"],["sergal2","run"],["robot","run5b"]]){const s=document.getElementById('charSel');s.value=c;s.onchange();TER.type="hills";
   for(let i=0;i<300;i++){groundOff=i;charDef().build({...P[m]},i/60)}
   const t0=performance.now();for(let i=0;i<3000;i++){groundOff=i;charDef().build({...P[m]},i/60)}res[c+"/"+m]=((performance.now()-t0)/3000*1000).toFixed(0)+" us"}
  return res});await b.close();return r}
(async()=>{for(let k=0;k<2;k++){console.log('before',JSON.stringify(await run(process.argv[2])));console.log('after ',JSON.stringify(await run(process.argv[3])))}})();
