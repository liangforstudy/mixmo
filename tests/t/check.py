import sys,json,math
sys.path.insert(0,"t")
from lib import *
url=sys.argv[1]
def run(pg,start,pre="",trigger="$('tF').onclick()",terrain=None,label=None,during=None):
    pg.evaluate("location.reload()") if False else None
    pg.evaluate(f"setChar('sergal','idle');setChar('robot','{start}');SWAP=false;GECKO=false;FLIP=null;WALKOVER=null;STANDEND='keep';TER.type='{terrain or 'flat'}';RLOOK.skin='robot';HEAD=0;HEAD_T=0;POS=[0,0];groundOff=0;phase=0;TURNM=null;SPIN=null;DIR=1")
    if pre:pg.evaluate(pre)
    for i in range(150):pg.evaluate("simStep(1/60)")
    pg.evaluate(trigger)
    fr=[];n=0
    for i in range(900):
        if during and i==during[0]:pg.evaluate(during[1])
        pg.evaluate("simStep(1/60)");s=pg.evaluate("snap()");s["lo"]=pg.evaluate("Math.min(...prims.filter(q=>q.t!==2).flatMap(q=>(q.pts||[q.a,q.b||q.a]).map(v=>v[1]-ground(...(()=>{const c=Math.cos(-HEAD),s=Math.sin(-HEAD);return[v[0]*c+v[2]*s,-v[0]*s+v[2]*c]})()))))");s["segmax"]=pg.evaluate("Math.max(...SEGDBG.flat().map(v=>Math.abs(v-1)),0)");fr.append(s)
        if s["kind"] is None and s["wo"]==0:
            n+=1
            if n>30:break
    rise=[f for f in fr if f["kind"]=="rise"]
    worst=0;wbad=0;lo=1e9;seg=0;jump=0;prev=None;nu=any(f["nu"] for f in rise);PM=[3,4,5,0,1,2];lowj=1e9
    for s in fr:
        W=[world(s,c[3]) for c in s["W"]];cl=s["cl"]
        if s["kind"]=="rise":
            wbad=max(wbad,s["bad"]);lo=min(lo,s["lo"]);seg=max(seg,s["segmax"])
            lowj=min(lowj,min(c[k][1] for c in s["W"] for k in (1,2,3,4)) if not terrain else min(cl))
        if prev is not None and (s["kind"]=="rise" or pk=="rise"):
            swap=(pk=="rise" and s["kind"]!="rise")
            for k in range(6):
                kk=PM[k] if swap else k
                d=math.hypot(W[k][0]-prev[kk][0],W[k][2]-prev[kk][2])
                if cl[k]<3.25 and pcl[kk]<3.25 and d>worst:worst=d;wat=(s['ft'],k,swap,cl[k],pcl[kk])
                dd=math.dist(W[k],prev[kk])
                if dd>jump:jump=dd;jat=(s['ft'],k,swap,[round(v,1) for v in prev[kk]],[round(v,1) for v in W[k]])
        prev=W;pcl=cl;pk=s["kind"]
    print("%-34s rise frames %3d nu=%s  planted slide %.2f  biggest paw move/frame %.1f  bones bad %d (%.4f)  lowest drawn point %.1f, joint %.1f"%(label or start,len(rise),nu,worst,jump,wbad,seg,lo,lowj));print("      at",jat) if jump>24 else None;print('      slide at',wat) if worst>1 else None
    return fr
with sync_playwright() as pw:
    b,pg,errs=open_page(pw,url)
    for m in ["walk","idle","tpose","run","walk2","runTail","dino","roo"]:run(pg,m)
    run(pg,"run6",trigger="STANDEND='front';goMode('idle')",label="run6 -> idle, stand on front end")
    run(pg,"run6",trigger="STANDEND='front';goMode('run5b')",label="run6 -> run5b (lying), front end")
    run(pg,"walk",terrain="hills",label="walk, hills")
    run(pg,"walk",terrain="steps",label="walk, steps")
    run(pg,"walk",pre="RLOOK.skin='sergal'",label="walk, sergal skin")
    run(pg,"walk",pre="RLOOK.mid=1.4;BODY_L=140;for(const L of RLIMBS)if(L.end==='T')L.v[1]=BODY_L",label="walk, long body + long middle limbs")
    pg.evaluate("RLOOK.mid=1;BODY_L=100;for(const L of RLIMBS)if(L.end==='T')L.v[1]=BODY_L")
    run(pg,"walk",label="walk, 90 turn mid-rise",during=(90,"startTurn('L')"))
    run(pg,"walk",pre="$('blend').value=2",label="walk, slow 2 s blend")
    pg.evaluate("$('blend').value=0.6")
    print("errs",errs)
    b.close()
