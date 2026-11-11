import sys
sys.path.insert(0,"t")
from lib import *
with sync_playwright() as pw:
    b,pg,errs=open_page(pw,sys.argv[1])
    for wait in (150,163):
        pg.evaluate("setChar('sergal','idle');setChar('robot','roo');POS=[0,0];groundOff=0;phase=0")
        for i in range(wait):pg.evaluate("simStep(1/60)")
        pg.evaluate("$('tF').onclick()");prev=None
        for i in range(40):
            pg.evaluate("simStep(1/60)");s=pg.evaluate("snap()")
            if s["wo"]!=1:break
            pg.evaluate("showStatus()");st=pg.evaluate("$('stText').textContent")
            y=pg.evaluate("Math.max(...prims.filter(q=>q.t!==2).flatMap(q=>(q.pts||[q.a,q.b||q.a]).map(v=>v[1])))")
            lo=min(c[k][1] for c in s["W"] for k in (1,2,3))
            if prev is not None and (abs(y-prev)>12 or lo<2):print("press@%d sim frame %d u=%.2f top moved %.1f lowest joint %.1f | %s | tailCurve %.2f"%(wait,i,s["blendU"],y-prev,lo,st[-12:],pg.evaluate("cur.tailCurve")))
            prev=y
    b.close()
