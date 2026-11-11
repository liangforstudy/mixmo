const {open,addModel}=require('./lib');const fs=require('fs');
(async()=>{const {b,pg,errs}=await open(require('path').resolve(process.env.MIXMO||'Mixmo.html'));
 await addModel(pg,process.argv[2]);
 const r=await pg.evaluate(()=>{const M=MODELS[0],T=R3.T,root=M.root;root.updateMatrixWorld(true);
  const inv=new T.Matrix4().copy(root.matrixWorld).invert(),v=new T.Vector3(),pts=[];
  root.traverse(o=>{if(!o.isMesh)return;const n=o.geometry.attributes.position.count;for(let i=0;i<n;i++){o.getVertexPosition(i,v);v.applyMatrix4(o.matrixWorld).applyMatrix4(inv);pts.push([+v.x.toFixed(4),+v.y.toFixed(4),+v.z.toFixed(4)])}});
  const wp=b=>root.worldToLocal(b.getWorldPosition(new T.Vector3())).toArray();const m=M.rig;
  const bones={};for(const k of ["hips","thighL","shinL","footL","toesL","thighR","spine"])if(m[k])bones[k]=wp(m[k]);return{pts,bones}});
 fs.writeFileSync(process.argv[3],JSON.stringify(r));console.log(errs);await b.close()})();
