import base64
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/glb/'
JS=r'''async(spec)=>{const T=await import("https://cdn.jsdelivr.net/npm/three@0.170.0/+esm");
 const {GLTFExporter}=await import("https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/exporters/GLTFExporter.js/+esm");
 const scene=new T.Scene();const bones={},list=[];
 for(const [n,par,x,y,z] of spec.bones){const b=new T.Bone();b.name=n;const P=par?bones[par]:null;const pw=P?P.userData.w:[0,0,0];b.position.set(x-pw[0],y-pw[1],z-pw[2]);b.userData.w=[x,y,z];(P||scene).add?0:0;if(P)P.add(b);bones[n]=b;list.push(b)}
 const geo=new T.CylinderGeometry(spec.r,spec.r,spec.h,12,24);geo.translate(0,spec.h/2,0);
 const mat=new T.MeshStandardMaterial({color:0xcc8844});
 let mesh;
 if(list.length){const n=geo.attributes.position.count,si=new Uint16Array(n*4),sw=new Float32Array(n*4);
  for(let i=0;i<n;i++){const y=geo.attributes.position.getY(i);let bi=0,bd=1e9;list.forEach((b,j)=>{const d=Math.abs(b.userData.w[1]-y);if(d<bd){bd=d;bi=j}});si[i*4]=bi;sw[i*4]=1}
  geo.setAttribute("skinIndex",new T.Uint16BufferAttribute(si,4));geo.setAttribute("skinWeight",new T.Float32BufferAttribute(sw,4));
  mesh=new T.SkinnedMesh(geo,mat);const root=list[0];mesh.add(root);mesh.bind(new T.Skeleton(list))}
 else mesh=new T.Mesh(geo,mat);
 mesh.name="Body";scene.add(mesh);
 const ab=await new GLTFExporter().parseAsync(scene,{binary:true});
 let s="";const u=new Uint8Array(ab);for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode(...u.subarray(i,i+8192));return btoa(s)}'''
L=lambda s,x:x if s=='L' else -x
fox=[("Hips_01_8",None,0,1.29,0),("spine_02_9","Hips_01_8",0,1.36,0),("Lowerchest_03_10","spine_02_9",0,1.5,0),("upper chest_04_11","Lowerchest_03_10",0,1.65,0),
 ("neck_05_12","upper chest_04_11",0,1.85,0),("HeadBone_06_13","neck_05_12",0,1.94,0),("Jaw_07_14","HeadBone_06_13",0,1.97,0.05)]
for s,i in [('L',0),('R',1)]:
    x=0.12 if s=='L' else -0.12
    fox+= [(f"thigh.{s}_09{i}_98","Hips_01_8",x,1.22,0),(f"shin.{s}_09{i}_99",f"thigh.{s}_09{i}_98",x,0.73,0.13),(f"foot.{s}_09{i}_100",f"shin.{s}_09{i}_99",x,0.06,-0.10),
           (f"shoulder.{s}_04{i}_53","upper chest_04_11",x*0.75,1.81,0),(f"upper_arm.{s}_04{i}_54",f"shoulder.{s}_04{i}_53",x*1.5,1.77,0),(f"forearm.{s}_04{i}_55",f"upper_arm.{s}_04{i}_54",x*4.2,1.74,0),(f"hand.{s}_04{i}_57",f"forearm.{s}_04{i}_55",x*7,1.73,0)]
fox+=[("TailRoot_096_104","Hips_01_8",0,1.39,-0.11)]+[(f"tail{k}_0{96+k}_{104+k}",("TailRoot_096_104" if k==1 else f"tail{k-1}_0{95+k}_{103+k}"),0,1.35-0.07*k,-0.26-0.15*k) for k in range(1,11)]
mixamo=[("mixamorig:Hips",None,0,1.0,0),("mixamorig:Spine","mixamorig:Hips",0,1.1,0),("mixamorig:Spine2","mixamorig:Spine",0,1.3,0),("mixamorig:Neck","mixamorig:Spine2",0,1.5,0),("mixamorig:Head","mixamorig:Neck",0,1.6,0),
 ("mixamorig:LeftUpLeg","mixamorig:Hips",0.1,0.95,0),("mixamorig:LeftLeg","mixamorig:LeftUpLeg",0.1,0.5,0),("mixamorig:LeftFoot","mixamorig:LeftLeg",0.1,0.08,0),("mixamorig:LeftToeBase","mixamorig:LeftFoot",0.1,0.02,0.12),
 ("mixamorig:RightUpLeg","mixamorig:Hips",-0.1,0.95,0),("mixamorig:RightLeg","mixamorig:RightUpLeg",-0.1,0.5,0),("mixamorig:RightFoot","mixamorig:RightLeg",-0.1,0.08,0),
 ("mixamorig:LeftArm","mixamorig:Spine2",0.2,1.45,0),("mixamorig:LeftForeArm","mixamorig:LeftArm",0.45,1.45,0),("mixamorig:LeftHand","mixamorig:LeftForeArm",0.7,1.45,0)]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto('about:blank')
    for name,spec in [('foxlike',{'bones':fox,'r':0.25,'h':2.6}),('mixamo',{'bones':mixamo,'r':0.2,'h':1.75}),('static',{'bones':[],'r':0.5,'h':1.0})]:
        d=base64.b64decode(pg.evaluate(JS,spec));open(S+name+'.glb','wb').write(d);print(name,len(d))
    b.close()
