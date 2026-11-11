const {chromium}=require('playwright');
async function run(file){
 const b=await chromium.launch();const pg=await b.newPage();await pg.addInitScript(()=>{window.requestAnimationFrame=()=>0;Math.random=(()=>{let s=1;return()=>(s=(s*16807)%2147483647)/2147483647})()});const errs=[];
 pg.on('pageerror',e=>errs.push(e.message));
 await pg.goto('file://'+file);await pg.waitForTimeout(800);
 const r=await pg.evaluate(()=>{playing=false;let NUL=0;const out={},times={};
  const chars=[...document.getElementById('charSel').options].map(o=>o.value);
  for(const c of chars){const s=document.getElementById('charSel');s.value=c;s.onchange();
   for(const [m] of MODES)for(const tt of ["flat","hills","bumpy","steps"]){TER.type=tt;groundOff=0;
    const key=c+"/"+m+"/"+tt,arr=[];const t0=performance.now();
    for(let i=0;i<48;i++){groundOff=i*7;{const p={...P[m]};p.bobWave=Math.sin(2*Math.PI*(i/48)*Math.round(p.bobMul||1));charDef().build(p,i/48)}const js=JSON.stringify(prims.map(q=>[q.a,q.b,q.ra,q.rb]));if(js.includes("[null,null,null]"))NUL++;arr.push(js)}
    times[key]=performance.now()-t0;out[key]=arr}}
  return {out,times,chars,NUL}});
 await b.close();return {...r,errs};
}
(async()=>{const A=await run(process.argv[2]),B=await run(process.argv[3]);
 let n=0,diff=0;const seen={};for(const k in A.out){for(let i=0;i<A.out[k].length;i++){n++;if(A.out[k][i]!==B.out[k][i]){diff++;if(!seen[k]){seen[k]=1;console.log('DIFF',k)}}}}
 const ta=Object.values(A.times).reduce((a,b)=>a+b,0),tb=Object.values(B.times).reduce((a,b)=>a+b,0);
 console.log('frames with NaN: A',A.NUL,'B',B.NUL,'| chars',A.chars.join(','),'frames compared',n,'different',diff,'missing',Object.keys(A.out).length-Object.keys(B.out).length);
 console.log('build time before',ta.toFixed(0),'ms after',tb.toFixed(0),'ms');console.log('errors',A.errs,B.errs);})();
