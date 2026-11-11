import sys,math
sys.path.insert(0,"t")
from lib import *
url=sys.argv[1];start=sys.argv[2]
with sync_playwright() as pw:
    b,pg,errs=open_page(pw,url)
    pg.evaluate(f"setChar('robot','{start}')")
    for i in range(150):pg.evaluate("simStep(1/60)")
    pg.evaluate("$('tF').onclick()");prev=None
    for i in range(40):
        pg.evaluate("simStep(1/60)");s=pg.evaluate("snap()")
        if s["wo"]!=1:break
        W=[world(s,c[3]) for c in s["W"]];cl=s["cl"];out=[]
        for k in range(6):
            d=math.hypot(W[k][0]-prev[k][0],W[k][2]-prev[k][2]) if prev else 0
            lowj=min(s["W"][k][j][1] for j in (1,2))
            out.append("%d:h%5.1f d%4.1f j%5.1f w%.2f"%(k,cl[k]-3.2,d,lowj,s["w"][k]))
        print("%2d u%.2f "%(i,s["blendU"])+" | ".join(out));prev=W
    b.close()
