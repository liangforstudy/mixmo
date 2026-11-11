const {open,addModel}=require('./lib');
const MD=require('path').resolve(process.env.MODELS||'models')+'/';
(async()=>{const file=process.argv[2],shots=process.argv[3];
 const {b,pg,errs}=await open(file,{w:900,h:1100});
 await pg.waitForFunction(()=>R3.ok,null,{timeout:60000});
 await pg.evaluate(()=>{const s=$("charSel");s.value="sergal2";s.onchange()});
 await addModel(pg,MD+'baller_fox_body.glb');await addModel(pg,MD+'female_sergal_body.glb');
 await pg.evaluate(()=>{for(const c of document.querySelectorAll('.mdlCard'))c.querySelector('[data-g=move] [data-v=move]').click()});
 // stop the loop; pose the models without drawing (drawing is software here and very slow)
 await pg.evaluate(()=>{window.requestAnimationFrame=()=>0;window.__render=render;render=()=>{for(const M of MODELS)mdlPlace(M)};drawGait=()=>{}});
 await pg.waitForTimeout(200);
 const hasP=await pg.evaluate(()=>typeof setPreset2==='function');
 const res={};
 for(const preset of (hasP?['sergal','fox']:['sergal'])){
  if(hasP)await pg.evaluate(p=>setPreset2(p),preset);
  for(const mode of ['idle','walk','run','gallop']){
   const t0=Date.now();
   const r=await pg.evaluate(([mode])=>{const s=$("modeSel");s.value=mode;s.onchange();
    let t=last;const T=R3.T,V=()=>new T.Vector3();
    for(let i=0;i<120;i++){t+=1000/60;frame(t)}
    const stat=MODELS.map(M=>({name:M.info.name.split('_')[0],drop:[],ext:[],sc:0}));
    for(let i=0;i<180;i++){t+=1000/60;frame(t);
     MODELS.forEach((M,j)=>{const mv=M.mv,g=M.grp,sc=g.scale.x,st=stat[j];st.sc=sc;
      for(const sd of ['L','R']){const L=mv.legs[sd],A=L.th.getWorldPosition(V()),F=L.ft.getWorldPosition(V());
       st.drop.push(L.hipH*sc-(A.y-g.position.y));st.ext.push(A.distanceTo(F)/((L.l1+L.l2)*sc))}})}
    const his=typeof withLegs2==='function'?withLegs2(()=>restHeight({...P.idle})):restHeight({...P.idle});
    const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
    return {his:+his.toFixed(1),m:MODELS.map((M,j)=>{const s=stat[j];return{name:s.name,height:+(s.sc*M.info.height).toFixed(0),toe:+M.mv.legs.L.toe.z.toFixed(3),
     dA:+avg(s.drop).toFixed(1),dM:+Math.max(...s.drop).toFixed(1),eA:+avg(s.ext).toFixed(2),eM:+Math.max(...s.ext).toFixed(3)}})}},[mode]);
   res[preset+'/'+mode]=r;
   if(shots){await pg.evaluate(()=>{yaw=Math.PI/2;pitch=0.1;zoom=0.85;let t=last;for(let i=0;i<9;i++){t+=1000/60;frame(t)}__render()});
    await pg.locator('#view').screenshot({path:shots+'/'+preset+'_'+mode+'.png'});await pg.evaluate(()=>{yaw=0.7;pitch=0.28;zoom=1})}
   console.error(preset,mode,(Date.now()-t0)/1000+'s');
  }}
 for(const k in res)console.log(k.padEnd(14),'his hip',res[k].his,'|',res[k].m.map(x=>`${x.name}: h ${x.height} toe ${x.toe} hip drop avg ${x.dA} max ${x.dM}; leg stretch avg ${x.eA} max ${x.eM}`).join(' | '));
 console.log('errors',errs);await b.close()})();
