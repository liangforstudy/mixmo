import sys,math
sys.path.insert(0,"t")
from lib import *
url=sys.argv[1]
def run(pg,start,pre="",wait=150,ter="flat"):
    pg.evaluate(f"setChar('sergal','idle');setChar('robot','{start}');SWAP=false;GECKO=false;FLIP=null;WALKOVER=null;STANDEND='keep';TER.type='{ter}';RLOOK.skin='robot';HEAD=0;HEAD_T=0;POS=[0,0];groundOff=0;phase=0;TURNM=null;SPIN=null;DIR=1")
    if pre:pg.evaluate(pre)
    for i in range(wait):pg.evaluate("simStep(1/60)")
    pg.evaluate("$('tF').onclick()");pd=pg.evaluate("!!(WALKOVER&&WALKOVER.pd)")
    prev=None;worst=0;jump=0;bad=0;lo=1e9;land=None;relift=0;n=0;pos0=pg.evaluate("POS[1]")
    for i in range(200):
        pg.evaluate("simStep(1/60)");s=pg.evaluate("snap()")
        if s["wo"]!=1:break
        n+=1;W=[world(s,c[3]) for c in s["W"]];cl=s["cl"];bad=max(bad,s["bad"])
        lo=min(lo,min(c[k][1]-0 for c in s["W"] for k in (1,2,3)) if ter=="flat" else min(cl))
        if prev:
            for k in range(6):
                d=math.hypot(W[k][0]-prev[k][0],W[k][2]-prev[k][2])
                if cl[k]<3.25 and pcl[k]<3.25:worst=max(worst,d)
                jump=max(jump,math.dist(W[k],prev[k]))
        if land is None and all(v<3.25 for v in cl[3:]):land=s["blendU"]
        if land is not None:relift=max(relift,max(cl[3:])-3.2)
        prev=W;pcl=cl
    # start of the rise: do red paws hop?
    hop=0
    for i in range(30):
        pg.evaluate("simStep(1/60)");s=pg.evaluate("snap()");hop=max(hop,max(s["cl"][3:])-3.2)
    print("%-22s planted drop %-5s frames %3d coast %5.1f | red paws all down at %s of the drop, lift again by %.1f; hop in first 0.5 s of the rise %.1f | planted slide %.2f, biggest move/frame %.1f, bones bad %d, lowest joint %.1f"%(start+(" "+ter if ter!="flat" else ""),pd,n,pg.evaluate("WALKOVER&&WALKOVER.pd?WALKOVER.pd.Dc:-1"),("%.0f%%"%(100*land)) if land else "never",relift,hop,worst,jump,bad,lo))
with sync_playwright() as pw:
    b,pg,errs=open_page(pw,url)
    for m in ["walk","idle","tpose","run","walk2","runTail","dino","roo"]:run(pg,m)
    run(pg,"walk",wait=163);run(pg,"run",wait=171)
    run(pg,"walk",ter="hills");run(pg,"walk",ter="steps")
    run(pg,"walk",pre="RLOOK.skin='sergal'")
    run(pg,"walk",pre="RLOOK.segs=3;segUI&&segUI()")
    run(pg,"run5b");run(pg,"run6")
    print("errs",errs);b.close()
