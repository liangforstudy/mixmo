import sys,json,math,io
sys.path.insert(0,"t")
from lib import *
from PIL import Image,ImageDraw
url=sys.argv[1];start=sys.argv[2];out=sys.argv[3];cams=json.loads(sys.argv[4]) if len(sys.argv)>4 else [[0.9,0.35]]
pre=sys.argv[5] if len(sys.argv)>5 else ""
import os
want=json.loads(os.environ.get("WANT","[0.01,0.07,0.13,0.19,0.25,0.31,0.38,0.46,0.54,0.62,0.72,0.82,0.9,0.96,0.995]"));ZOOM=os.environ.get("ZOOM","0.62");COLS=int(os.environ.get("COLS","5"));SC=float(os.environ.get("SC","0.5"))
with sync_playwright() as pw:
    b,pg,errs=open_page(pw,url,w=420,h=900)
    pg.evaluate(f"setChar('robot','{start}')")
    if pre:pg.evaluate(pre)
    for i in range(120):pg.evaluate("simStep(1/60)")
    pg.evaluate("$('tF').onclick()")
    rows=[[] for _ in cams];k=0;lab=[]
    for i in range(900):
        pg.evaluate("simStep(1/60)");s=pg.evaluate("({ft:FLIP&&FLIP.kind==='rise'?flipT():null,wo:WALKOVER?1:0})")
        if s["ft"] is not None and k<len(want) and pg.evaluate("FLIP&&FLIP.nu?riseTau():flipT()")>=want[k]:
            for ci,(y,p) in enumerate(cams):
                pg.evaluate(f"yaw={y};pitch={p};zoom={ZOOM};panX=0;panY=0;render()")
                import base64;rows[ci].append(Image.open(io.BytesIO(base64.b64decode(pg.evaluate("cv.toDataURL('image/png')").split(',')[1]))).convert('RGBA'))
            lab.append("%.2f"%pg.evaluate("FLIP&&FLIP.nu?riseTau():flipT()"));k+=1
        if k>=len(want):break
    print("errs",errs,"n",k)
    w,h=rows[0][0].size;cw=w//2*2;sc=SC
    tw,th=int(w*sc),int(h*sc);cols=COLS
    for ci,r in enumerate(rows):
        nr=(len(r)+cols-1)//cols
        sheet=Image.new("RGB",(tw*cols,th*nr),"white");d=ImageDraw.Draw(sheet)
        for n,im in enumerate(r):
            im2=Image.new('RGBA',im.size,(240,228,200,255));im2.alpha_composite(im);sheet.paste(im2.convert('RGB').resize((tw,th)),((n%cols)*tw,(n//cols)*th));d.text(((n%cols)*tw+4,(n//cols)*th+4),lab[n],fill="black")
        sheet.save(f"{out}_{ci}.png")
    b.close()
