const {open,addModel}=require('./lib');
(async()=>{const {b,pg,errs}=await open(require('path').resolve(process.env.MIXMO||'Mixmo.html'));
 await addModel(pg,require('path').resolve(process.env.MODELS||'models','baller_fox_body.glb'));
 const r=await pg.evaluate(()=>{const M=MODELS[0],T=R3.T,root=M.root;root.updateMatrixWorld(true);
  const box=new T.Box3().setFromObject(root);const wp=b=>root.worldToLocal(b.getWorldPosition(new T.Vector3()));
  const m=M.rig,o={h:box.max.y-box.min.y,minY:box.min.y};for(const k of ["hips","thighL","shinL","footL","toesL","spine","chest","neck","head","upperArmL","forearmL","handL"]){if(m[k]){const v=wp(m[k]);o[k]=[v.x,v.y-box.min.y,v.z].map(x=>+x.toFixed(3))}}
  o.foot_children=m.footL.children.map(c=>c.name+" "+c.position.toArray().map(x=>x.toFixed(3)));o.mv=M.mv&&{l1:M.mv.legs.L.l1,l2:M.mv.legs.L.l2,ankleH:M.mv.legs.L.ankleH,hipH:M.mv.legs.L.hipH,toe:M.mv.legs.L.toe.toArray(),base:M.mv.base};return o});
 console.log(JSON.stringify(r,null,1));console.log(errs);await b.close()})();
