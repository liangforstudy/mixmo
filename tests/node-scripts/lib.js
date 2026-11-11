const {chromium}=require('playwright');const fs=require('fs');
const NM=__dirname+'/node_modules/three/';
const BASE='https://cdn.jsdelivr.net/npm/three@0.170.0/';
const fix=s=>s.replace(/from\s+'three'/g,"from '"+BASE+"+esm'").replace(/'\.\.\/utils\/BufferGeometryUtils\.js'/g,"'"+BASE+"examples/jsm/utils/BufferGeometryUtils.js'");
async function open(file,{w=900,h=900,stopLoop=false}={}){
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const pg=await b.newPage({viewport:{width:w,height:h}});const errs=[];
 pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text())});
 await pg.route(/cdn\.jsdelivr\.net\/npm\/three@0\.170\.0\/.*/,r=>{const u=r.request().url();let p;
  if(/\/\+esm$/.test(u)&&!/examples/.test(u))p=NM+'build/three.module.js';
  else{const m=u.match(/three@0\.170\.0\/(.*?)(\/\+esm)?$/);p=NM+m[1]}
  r.fulfill({status:200,contentType:'application/javascript',headers:{'access-control-allow-origin':'*'},body:fix(fs.readFileSync(p,'utf8'))})});
 if(stopLoop)await pg.addInitScript(()=>{window.requestAnimationFrame=()=>0});
 await pg.goto('file://'+file);await pg.waitForTimeout(500);
 return {b,pg,errs};
}
async function addModel(pg,path){const n=await pg.evaluate(()=>MODELS.length);
 await pg.setInputFiles('#mdlFile',path);await pg.waitForFunction(k=>MODELS.length>k&&!MLOAD.busy,n,{timeout:120000});await pg.waitForTimeout(300)}
module.exports={open,addModel};
