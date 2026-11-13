#!/usr/bin/env python3
"""GLB checks for the Pooltoy Water Lab (2026-11-13).

Usage:
  python3 glb_tests.py pooltoy-water-lab.html baller_fox_body.glb [--three node_modules/three] [--chrome /path/to/chrome] [--out shots]

What it does:
  1. Loads the GLB into the lab twice: normally, and with the Claude chat preview's limits simulated
     (blob: URLs broken, fetch(data:) refused). PASS if all textures load in both.
  2. Takes screenshots of the GLB model from three angles (from above, front-low, the tail) into --out,
     to compare the water surface by eye between two copies of the lab.

Needs: pip install playwright (and a Chrome/Chromium), and three.js r170 on disk
(npm i three@0.170.0) so jsDelivr requests are served locally (works offline, same version as the lab).
"""
import argparse, asyncio, os, re, sys
from playwright.async_api import async_playwright

ap = argparse.ArgumentParser()
ap.add_argument('lab'); ap.add_argument('glb')
ap.add_argument('--three', default='node_modules/three')
ap.add_argument('--chrome', default=None)
ap.add_argument('--out', default='shots')
A = ap.parse_args()
ROOT = os.path.abspath(A.three) + '/'
BASE = 'https://cdn.jsdelivr.net/npm/three@0.170.0/'
BLOCK = """URL.createObjectURL=()=> 'blob-request://fake/'+Math.random();
const _f=window.fetch;window.fetch=(u,...a)=>String(u).startsWith('data:')?Promise.reject(new TypeError('Load failed')):_f(u,...a);"""

async def route(r):
    # serve jsDelivr's three@0.170.0 (including /+esm URLs) from the local copy, imports rewritten to absolute URLs
    p = r.request.url.split('three@0.170.0/')[1].replace('/+esm', '')
    if p in ('', '+esm'): p = 'build/three.module.js'
    src = open(ROOT + p).read(); d = os.path.dirname(p)
    def fix(m):
        q = m.group(2)
        if q == 'three': return m.group(1) + BASE + '+esm' + m.group(3)
        if q.startswith('.'): return m.group(1) + BASE + os.path.normpath(os.path.join(d, q)) + m.group(3)
        return m.group(0)
    await r.fulfill(body=re.sub(r"""(from\s*['"])([^'"]+)(['"])""", fix, src), content_type='text/javascript')

async def session(pw, block, shots):
    b = await pw.chromium.launch(executable_path=A.chrome, args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = await b.new_page(viewport={'width': 430, 'height': 900}, device_scale_factor=2)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    if block: await pg.add_init_script(BLOCK)
    await pg.route('**/cdn.jsdelivr.net/**', route)
    await pg.goto('file://' + os.path.abspath(A.lab)); await pg.wait_for_timeout(2500)
    await pg.set_input_files('#glbFile', A.glb)
    await pg.wait_for_function("/Room inside|couldn't|wrong|isn't/.test(document.getElementById('glbMsg').textContent)", timeout=120000)
    msg = await pg.inner_text('#glbMsg'); await pg.wait_for_timeout(2000)
    if shots:
        os.makedirs(A.out, exist_ok=True); tag = os.path.splitext(os.path.basename(A.lab))[0]
        for name, dx, dy, zoom in [('above', -40, 90, 6), ('front-low', 0, -60, 6), ('tail', 330, 110, 0)]:
            bx = await pg.locator('#view').bounding_box(); x = bx['x'] + bx['width'] * 0.6; y = bx['y'] + bx['height'] * 0.5
            await pg.mouse.dblclick(x, y); await pg.wait_for_timeout(300)   # double-click resets the camera
            await pg.mouse.move(x, y); await pg.mouse.down(); await pg.mouse.move(x + dx, y + dy, steps=10); await pg.mouse.up()
            for _ in range(zoom): await pg.mouse.wheel(0, -250); await pg.wait_for_timeout(100)
            await pg.wait_for_timeout(1200)
            await pg.locator('#view').screenshot(path=f'{A.out}/{tag}_{name}.png')
    await b.close()
    return msg, errs

async def main():
    fails = 0
    async with async_playwright() as pw:
        for block in (False, True):
            msg, errs = await session(pw, block, shots=not block)
            label = 'chat-preview limits' if block else 'normal'
            ok = 'Room inside' in msg and "couldn't be read" not in msg and not errs
            fails += not ok
            print(('PASS' if ok else 'FAIL'), label, '-', msg[:160], *(['errors: ' + '; '.join(errs)] if errs else []))
    print(f'Screenshots in {A.out}/' if not fails else '', 'failures:', fails)
    sys.exit(1 if fails else 0)
asyncio.run(main())
