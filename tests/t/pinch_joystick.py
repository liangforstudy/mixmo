#!/usr/bin/env python3
"""A pinch is never stolen by the Game-mode joystick (real multi-touch, phone size).

  A: a finger on the view, then one in the joystick area, spread: zooms, joystick stays off
  B: a finger in the joystick area, then one on the view straight after, spread: zooms
  C: steering with the joystick, then one finger on the view: still steering, and the view orbits
  D: the joystick alone still works

Run from the tests folder with the server going:  python3 t/pinch_joystick.py [URL]
"""
import asyncio
import os
import sys
import time

from playwright.async_api import async_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/Mixmo.html"


async def main():
    t_all = time.time()
    fails = []
    async with async_playwright() as p:
        exe = os.environ.get("CHROME") or next((c for c in ("/usr/bin/google-chrome", "/usr/bin/chromium") if os.path.exists(c)), None)
        try:
            b = await p.chromium.launch()
        except Exception:
            b = await p.chromium.launch(executable_path=exe)
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        pg = await ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        await pg.wait_for_function("typeof STICK!=='undefined'&&document.getElementById('stickZone').offsetParent")
        cdp = await ctx.new_cdp_session(pg)
        zr = await pg.evaluate("(()=>{const r=document.getElementById('stickZone').getBoundingClientRect();return[r.left,r.top,r.right,r.bottom]})()")
        vr = await pg.evaluate("(()=>{const r=document.getElementById('view').getBoundingClientRect();return[r.left,r.top,r.right,r.bottom]})()")
        my = (zr[1] + zr[3]) / 2
        zx = zr[0] + 70          # inside the joystick area
        vx = vr[2] - 70          # on the view, outside the joystick area

        async def touch(kind, pts):
            await cdp.send("Input.dispatchTouchEvent", {"type": kind, "touchPoints": [{"x": x, "y": y, "id": i} for i, (x, y) in pts]})

        async def st():
            return await pg.evaluate("({zoom:zoom,stick:STICK.on,yaw:yaw})")

        def check(name, ok, detail):
            print(f"  {'ok  ' if ok else 'FAIL'} {name}: {detail}")
            if not ok:
                fails.append(name)

        # A
        t = time.time()
        await pg.evaluate("zoom=1;panX=panY=0")
        await touch("touchStart", [(0, (vx, my))]); await pg.wait_for_timeout(60)
        await touch("touchStart", [(0, (vx, my)), (1, (zx, my))]); await pg.wait_for_timeout(60)
        for k in range(1, 8):
            await touch("touchMove", [(0, (vx + k * 5, my)), (1, (zx - k * 5, my))]); await pg.wait_for_timeout(25)
        s = await st(); await touch("touchEnd", []); await pg.wait_for_timeout(150)
        check("A view finger, then joystick-area finger", s["zoom"] > 1.1 and not s["stick"], f"zoom {s['zoom']:.2f}, joystick {'on' if s['stick'] else 'off'} ({time.time()-t:.1f}s)")
        # B
        t = time.time()
        await pg.evaluate("zoom=1;panX=panY=0")
        await touch("touchStart", [(0, (zx, my))]); await pg.wait_for_timeout(50)
        await touch("touchStart", [(0, (zx, my)), (1, (vx, my))]); await pg.wait_for_timeout(50)
        for k in range(1, 8):
            await touch("touchMove", [(0, (zx - k * 5, my)), (1, (vx + k * 5, my))]); await pg.wait_for_timeout(25)
        s = await st(); await touch("touchEnd", []); await pg.wait_for_timeout(150)
        check("B joystick-area finger, then view finger", s["zoom"] > 1.1 and not s["stick"], f"zoom {s['zoom']:.2f}, joystick {'on' if s['stick'] else 'off'} ({time.time()-t:.1f}s)")
        # C
        t = time.time()
        await pg.evaluate("zoom=1;panX=panY=0")
        await touch("touchStart", [(0, (zx, my))]); await pg.wait_for_timeout(100)
        for k in range(1, 6):
            await touch("touchMove", [(0, (zx, my - k * 8))]); await pg.wait_for_timeout(60)
        await pg.wait_for_timeout(300); y0 = (await st())["yaw"]
        await touch("touchStart", [(0, (zx, my - 40)), (1, (vx, my))]); await pg.wait_for_timeout(60)
        for k in range(1, 6):
            await touch("touchMove", [(0, (zx, my - 40)), (1, (vx - k * 8, my))]); await pg.wait_for_timeout(25)
        s = await st(); await touch("touchEnd", []); await pg.wait_for_timeout(150)
        check("C steering, then a view finger orbits", s["stick"] and abs(s["yaw"] - y0) > 0.1 and abs(s["zoom"] - 1) < 1e-6, f"joystick {'on' if s['stick'] else 'off'}, yaw moved {s['yaw']-y0:.2f}, zoom {s['zoom']:.2f} ({time.time()-t:.1f}s)")
        # D
        t = time.time()
        await touch("touchStart", [(0, (zx, my))]); await pg.wait_for_timeout(100)
        await touch("touchMove", [(0, (zx, my - 30))]); await pg.wait_for_timeout(100)
        on = await pg.evaluate("STICK.on&&STICK.y>0.3"); await touch("touchEnd", [])
        check("D joystick alone", on, f"steering {'yes' if on else 'no'} ({time.time()-t:.1f}s)")
        check("no page errors", not errs, errs or "none")
        await b.close()
    print(f"failures: {len(fails)}  ({time.time()-t_all:.1f}s)")
    sys.exit(1 if fails else 0)


asyncio.run(main())
