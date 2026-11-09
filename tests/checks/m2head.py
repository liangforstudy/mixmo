import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':900,'height':700})
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(800)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="three"]\').click();$("charSel").value="sergal2";$("charSel").onchange();$("modeSel").value="idle";$("modeSel").onchange()}')
    pg.set_input_files('#mdlFile',S+'real/'+F+'.glb')
    for i in range(120):
        pg.wait_for_timeout(500)
        if pg.evaluate('!!MDL.info'):break
    pg.click('#mdlPlace [data-p="in"]')
    out=[]
    for mv in ['statue','move']:
        pg.click(f'#mdlMove [data-m="{mv}"]');pg.wait_for_timeout(1500)
        pg.evaluate('()=>{if(playing)$("play").onclick();yaw=1.57;pitch=0.05;zoom=2.2;panY=110}');pg.wait_for_timeout(500)
        box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
        fn=S+f'head_{mv}.png';pg.screenshot(path=fn,clip={'x':box[0],'y':box[1],'width':box[2],'height':box[3]*0.6});out.append(fn)
        print(mv,pg.evaluate('''()=>{const T=R3.T,h=MDL.rig.head,n=MDL.rig.neck,q=h.getWorldQuaternion(new T.Quaternion()),e=new T.Euler().setFromQuaternion(q,"YXZ");
          const a=n.getWorldPosition(new T.Vector3()),c=h.getWorldPosition(new T.Vector3());return {headEuler:[e.x,e.y,e.z].map(v=>(v*57.3).toFixed(1)),neckDir:c.sub(a).normalize().toArray().map(v=>v.toFixed(2))}}'''))
        pg.evaluate('()=>{if(!playing)$("play").onclick()}')
    print(pg.evaluate('()=>({up:REC.head.up.map((v,i)=>(v-REC.head.o[i]).toFixed(2)),fw:REC.head.fw.map((v,i)=>(v-REC.head.o[i]).toFixed(2)),neck:[0,1,2].map(i=>(REC.head.top[i]-REC.head.base[i]).toFixed(1))})'))
    b.close()
from PIL import Image
ims=[Image.open(f) for f in out];w,h=ims[0].size;o=Image.new('RGB',(w*2,h));[o.paste(im,(i*w,0)) for i,im in enumerate(ims)];o.save(S+'head_cmp.png')
