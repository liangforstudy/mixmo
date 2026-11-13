#!/usr/bin/env python3
"""Deterministic pictures of the lab and of Mixmo (three.js served from node_modules).
usage: shots.py lab.html mixmo.html outdir  (either may be '-')"""
import sys, os, re, asyncio
from playwright.async_api import async_playwright
LAB, MIX, OUT = sys.argv[1:4]
ROOT = os.environ.get('THREE_DIR','node_modules/three') + '/'
BASE = 'https://cdn.jsdelivr.net/npm/three@0.170.0/'
async def route(r):
    p = r.request.url.split('three@0.170.0/')[1].replace('/+esm', '')
    if p in ('', '+esm'): p = 'build/three.module.js'
    src = open(ROOT + p).read(); d = os.path.dirname(p)
    def fix(m):
        q = m.group(2)
        if q == 'three': return m.group(1) + BASE + '+esm' + m.group(3)
        if q.startswith('.'): return m.group(1) + BASE + os.path.normpath(os.path.join(d, q)) + m.group(3)
        return m.group(0)
    await r.fulfill(body=re.sub(r"""(from\s*['"])([^'"]+)(['"])""", fix, src), content_type='text/javascript')
async def page(pw, url, init="", stop=True):
    b = await pw.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg = await b.new_page(viewport={'width':430,'height':900}, device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.add_init_script(("window.requestAnimationFrame=()=>0;" if stop else "")+init)
    await pg.route('**/cdn.jsdelivr.net/**', route)
    await pg.goto('file://'+os.path.abspath(url)); return b, pg, errs
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        if LAB != '-':
            b, pg, errs = await page(pw, LAB)
            await pg.wait_for_function("window.LAB&&LAB.R3&&(LAB.R3.ok||LAB.R3.failed)", timeout=120000, polling=250)
            await pg.evaluate("()=>{for(let i=0;i<120;i++)LAB.step(4);LAB.draw()}")
            await pg.locator('#view').screenshot(path=f'{OUT}/lab_toy.png')
            await pg.evaluate("()=>{document.querySelector('#shapeSeg button[data-v=\"capsule\"]').click();const r=document.querySelector('#slFlat input');r.value=0.5;r.dispatchEvent(new Event('input',{bubbles:true}));for(let i=0;i<240;i++)LAB.step(4);LAB.draw()}")
            await pg.locator('#view').screenshot(path=f'{OUT}/lab_capsule_flat05.png')
            print('lab errors', errs); await b.close()
        if MIX != '-':
            b, pg, errs = await page(pw, MIX, "try{localStorage.setItem('mixmoTier','anim')}catch(e){}")
            await pg.wait_for_function("typeof R3!=='undefined'&&R3.ok", timeout=90000, polling=250)
            await pg.evaluate("()=>{window.requestAnimationFrame=()=>0}"); await pg.wait_for_timeout(300)
            for ch in ['sergal','sergal2','robot']:
                await pg.evaluate("""(ch)=>{if(playing)$("play").onclick();$("charSel").value=ch;$("charSel").onchange();
                 const m=P.walk?"walk":"idle";mode=m;Object.assign(cur,P[m]);from={...P[m]};blendU=1;BLENDFROM=null;
                 POS=[0,0];HEAD=HEAD_T=0;OMEGA=0;TURNM=null;FLIP=null;SPR.init=false;phase=0.25;
                 const p={...cur};p.bobWave=Math.sin(2*Math.PI*0.25*Math.round(cur.bobMul||1));charDef().build(p,0.25);render()}""", ch)
                await pg.wait_for_timeout(300)
                await pg.locator('#view').screenshot(path=f'{OUT}/mixmo_{ch}.png')
            print('mixmo errors', errs); await b.close()
asyncio.run(main())
