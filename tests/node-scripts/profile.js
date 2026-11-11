const {open,addModel}=require('./lib');
(async()=>{const {b,pg,errs}=await open(require('path').resolve(process.env.MIXMO||'Mixmo.html'));
 await addModel(pg,process.argv[2]);
 const r=await pg.evaluate(()=>{const M=MODELS[0],T=R3.T,root=M.root;root.updateMatrixWorld(true);
  const inv=new T.Matrix4().copy(root.matrixWorld).invert(),v=new T.Vector3(),pts=[];
  root.traverse(o=>{if(!o.isMesh)return;const n=o.geometry.attributes.position.count;for(let i=0;i<n;i+=2){o.getVertexPosition(i,v);v.applyMatrix4(o.matrixWorld).applyMatrix4(inv);if(v.x>0.04)pts.push([v.x,v.y,v.z])}});
  const minY=Math.min(...pts.map(p=>p[1]));const rows=[];
  for(let y=0;y<1.3;y+=0.04){const s=pts.filter(p=>p[1]-minY>=y&&p[1]-minY<y+0.04&&p[0]<0.35);if(!s.length){rows.push([y,0]);continue}
   const zs=s.map(p=>p[2]);rows.push([+y.toFixed(2),s.length,+Math.min(...zs).toFixed(3),+Math.max(...zs).toFixed(3)])}
  return rows});
 for(const x of r)console.log(x.join('\t'));console.log(errs);await b.close()})();
