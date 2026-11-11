import sys,io,base64
sys.path.insert(0,"t")
from lib import *
from PIL import Image,ImageDraw
url=sys.argv[1];start=sys.argv[2];out=sys.argv[3];yaw=float(sys.argv[4]) if len(sys.argv)>4 else 0.9
with sync_playwright() as pw:
    b,pg,errs=open_page(pw,url,w=420,h=900)
    pg.evaluate(f"setChar('robot','{start}')")
    for i in range(150):pg.evaluate("simStep(1/60)")
    pg.evaluate("$('tF').onclick()");ims=[];lab=[]
    for i in range(1,61):
        pg.evaluate("simStep(1/60)")
        if i%5==0:
            pg.evaluate(f"yaw={yaw};pitch=0.28;zoom=1.25;panX=0;panY=0;render()")
            im=Image.open(io.BytesIO(base64.b64decode(pg.evaluate("cv.toDataURL('image/png')").split(',')[1]))).convert('RGBA')
            bg=Image.new('RGBA',im.size,(240,228,200,255));bg.alpha_composite(im);ims.append(bg.convert('RGB'));lab.append(pg.evaluate("(WALKOVER?'stage '+WALKOVER.stage:'')+' u '+blendU.toFixed(2)+(FLIP?' rise '+riseTau().toFixed(2):'')"))
    w,h=ims[0].size;sc=0.72;tw,th=int(w*sc),int(h*sc);cols=4
    sheet=Image.new("RGB",(tw*cols,th*3),"white");d=ImageDraw.Draw(sheet)
    for n,im in enumerate(ims):sheet.paste(im.resize((tw,th)),((n%cols)*tw,(n//cols)*th));d.text(((n%cols)*tw+4,(n//cols)*th+4),lab[n],fill="black")
    sheet.save(out);print(errs)
    b.close()
