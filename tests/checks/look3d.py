import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
tag=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    for ch,mode in [('sergal','walk'),('robot','walk'),('robot','run6')]:
      for limbs in ['smooth','capsule']:
        for ol in ['on']:
          pg=b.new_page(viewport={'width':520,'height':700})
          errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
          pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
          pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1500)
          pg.evaluate(f'''()=>{{document.querySelector('#rendSw [data-r="three"]').click();R3.look.limbs="{limbs}";R3.look.outline="{ol}";r3applyLook();
            $("charSel").value="{ch}";$("charSel").onchange();$("modeSel").value="{mode}";$("modeSel").onchange();if(!playing)$("play").onclick()}}''')
          pg.wait_for_timeout(2500)
          pg.evaluate('()=>{if(playing)$("play").onclick();yaw=0.9;pitch=0.3;zoom=1.3}');pg.wait_for_timeout(400)
          box=pg.evaluate('()=>{const r=$("view").getBoundingClientRect();return [r.x,r.y,r.width,r.height]}')
          pg.screenshot(path=S+f'l3_{tag}_{ch}_{mode}_{limbs}.png',clip={'x':box[0],'y':box[1],'width':box[2],'height':min(box[3],520)})
          if errs:print(ch,mode,limbs,errs[:3])
          pg.close()
    b.close()
print('done')
