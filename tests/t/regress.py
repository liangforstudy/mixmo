import sys,json,math,hashlib
sys.path.insert(0,"t")
from lib import *
SC=[]
for ch,modes in [("sergal",["idle","idleTail","walk","run","gallop"]),("sergal2",["idle","walk","run","gallop"]),("robot",["idle","tpose","walk","walk2","run","runTail","dino","roo","run4dog","run4","run5b","run5f","run5head","run6"])]:
    for m in modes:SC.append((f"{ch}/{m}",f"setChar('{ch}','{m}')",None,90))
SC+= [("robot walk->run6->idle",  "setChar('robot','walk')","goMode('run6')",150),
      ("robot flip ends","setChar('robot','walk')","startFlip('ends')",120),
      ("robot ceiling up+down","setChar('robot','walk')","startFlip('up')",200),
      ("robot lying rise run6->run5b front","setChar('robot','run6')","STANDEND='front';goMode('run5b');STANDEND='keep'",150),
      ("robot run6 180 swap","setChar('robot','run6')","startTurn('U')",200),
      ("robot walk 90 + 180","setChar('robot','walk')","startTurn('L')",150),
      ("robot run skid","setChar('robot','run')","startTurn('U')",150),
      ("robot spin","setChar('robot','walk')","toggleSpin()",150),
      ("robot hills run6","TER.type='hills';setChar('robot','run6')","goMode('walk')",150),
      ("robot run6 reversed -> walk front (older rise)","setChar('robot','run6')","DIR=-1;STANDEND='front';goMode('walk');STANDEND='keep'",200)]
def go(url):
    out={}
    with sync_playwright() as pw:
        b,pg,errs=open_page(pw,url)
        for name,setup,act,n in SC:
            pg.evaluate("TER.type='flat';SWAP=false;GECKO=false;FLIP=null;WALKOVER=null;STANDEND='keep';HEAD=0;HEAD_T=0;OMEGA=0;POS=[0,0];groundOff=0;phase=0;TURNM=null;SPIN=null;DIR=1;TRAVK=1;BOOST=0;SKIDLEAN=0;SPR.init=false;HS.length=0;setChar('sergal','idle');for(const L of [...LEGS,...RLIMBS,...LEGS2]){L.ik=null;L.yaw=undefined}")
            pg.evaluate(setup+";blendU=1;from={...P[mode]};cur={...P[mode]}")
            hs=[]
            for i in range(n):
                if act and i==40:pg.evaluate(act)
                if act and "ceiling" in name and i==120:pg.evaluate("startFlip('down')")
                pg.evaluate("simStep(1/60)")
                hs.append(pg.evaluate("JSON.stringify(prims.map(q=>[q.t,(q.a||[]).map(v=>+v.toFixed(4)),(q.b||[]).map(v=>+v.toFixed(4)),(q.pts||[]).map(p=>p.map(v=>+v.toFixed(4)))]))+POS.map(v=>v.toFixed(4))+HEAD.toFixed(5)"))
            out[name]=hs
        print("page errors:",errs);b.close()
    return out
A=go(sys.argv[1]);B=go(sys.argv[2]);tot=0;diff=0
SC_=SC
for name,_,_,n in SC:
    d=sum(1 for x,y in zip(A[name],B[name]) if x!=y);tot+=n;diff+=d
    if d:print("DIFFERENT %-50s %d of %d frames (first at %d)"%(name,d,n,next(i for i,(x,y) in enumerate(zip(A[name],B[name])) if x!=y)))
print("poses compared",tot,"different",diff)
