import json,sys
from playwright.sync_api import sync_playwright
# Records (or compares) the exact pose of both characters, every mode, several phases, flat + hills,
# plus a few robot looks. Deterministic: position/heading/springs reset before every pose.
JS=r"""()=>{const out={};const r=v=>Math.round(v*1000)/1000;
 const snap=()=>prims.map(q=>[q.t,...(q.a||[]).map(r),...(q.b&&q.b!==q.a?q.b:[]).map(r),...(q.pts?q.pts.flat().map(r):[]),q.col||""]);
 if(playing)$("play").onclick();
 const looks=[{},{segs:3,skin:"dino"},{segs:2,skin:"sergal",mid:1.5}];
 for(const ch of ["sergal","robot"]){$("charSel").value=ch;$("charSel").onchange();
  for(const ter of ["flat","hills"]){TER.type=ter;
   for(const [li,lk] of (ch==="robot"?looks:[{}]).entries()){Object.assign(RLOOK,{segs:1,skin:"robot",mid:1},lk);
    for(const [m] of MODES){mode=m;Object.assign(cur,P[m]);from={...P[m]};blendU=1;BLENDFROM=null;
     for(const ph of [0,0.13,0.25,0.5,0.77]){
      POS=[0,0];HEAD=HEAD_T=0;OMEGA=0;TURNM=null;TRAVK=1;SKIDLEAN=0;BOOST=0;FLIP=null;GECKO=false;SWAP=false;groundOff=0;
      SPR.init=false;HRAW.length=0;HS.length=0;for(const L of [...LEGS,...RLIMBS])L.ik=null;
      phase=ph;const p={...cur};p.bobWave=Math.sin(2*Math.PI*ph*Math.round(cur.bobMul||1));
      (ch==="robot"?buildRobot:buildRig)(p,ph);
      out[`${ch}|${ter}|${li}|${m}|${ph}`]=snap()}}}}}
 return out}"""
mode=sys.argv[1]; url=sys.argv[2] if len(sys.argv)>2 else 'http://localhost:8765/Mixmo.html'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(400)
    data=pg.evaluate(JS);b.close()
if errs:print('PAGE ERRORS',errs[:3])
if mode=='record':
    json.dump(data,open('golden.json','w'));print('recorded',len(data),'poses')
else:
    base=json.load(open('golden.json'));diff=[]
    for k,v in base.items():
        w=data.get(k)
        if w is None:diff.append((k,'missing'));continue
        if len(w)!=len(v):diff.append((k,f'part count {len(v)} -> {len(w)}'));continue
        worst=0
        for a,c in zip(v,w):
            for x,y in zip(a,c):
                if isinstance(x,(int,float)) and isinstance(y,(int,float)):worst=max(worst,abs(x-y))
                elif x!=y:worst=max(worst,999)
        if worst>0.01:diff.append((k,f'max change {worst:.3f}'))
    print('compared',len(base),'poses; changed:',len(diff))
    for d in diff[:15]:print(' -',*d)
