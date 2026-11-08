import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
F=sys.argv[1] if len(sys.argv)>1 else 'Mixmo.html'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':520,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
    pg.goto('http://localhost:8765/'+F);pg.wait_for_timeout(3000)
    pg.evaluate('()=>{window.GAPS=[];let t=performance.now();const f=()=>{const n=performance.now();GAPS.push(n-t);t=n;requestAnimationFrame(f)};requestAnimationFrame(f)}')
    for k,v in [('style','soft'),('shadow','blob'),('outline','off'),('ground','grid'),('limbs','capsule'),('style','toon'),('shadow','real'),('outline','on'),('ground','solid'),('limbs','smooth')]:
        pg.evaluate('()=>GAPS.length=0')
        pg.evaluate(f'()=>document.querySelector(\'#r3Look [data-k="{k}"][data-v="{v}"]\').click()')
        pg.wait_for_timeout(1200)
        g=pg.evaluate('GAPS');print(f'{k}={v}: longest gap between frames {max(g):.0f} ms, over 100 ms: {sum(1 for x in g if x>100)}, look now {pg.evaluate("R3.look."+k)}')
    print(errs);b.close()
