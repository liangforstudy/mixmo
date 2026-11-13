#!/usr/bin/env python3
"""lab.py - kept test for the Pooltoy Water Lab (pooltoy-water-lab.html).

  python3 lab.py <file-or-url>                    run every check (own limbs, one shared surface, a hard
                                                  shake, the Capsule, the amounts)
  python3 lab.py <file-or-url> --save t.json      also save the Test run's water levels
  python3 lab.py <file-or-url> --against t.json   also compare the Test run with a saved one
  --unit   (with --save / --against) count every part 1:1, as the lab did before P2-a,
           to prove that nothing but the counting changed

It never draws: the page's own frame loop is switched off and the lab is driven through
LAB.step, so results are the same on every run and three.js is not needed.
Takes about 20-40 seconds. Run after large changes only.
"""
import sys, json, os
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
def opt(name):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
    return None
save, against = opt("--save"), opt("--against")
unit = "--unit" in args
if unit: args.remove("--unit")
target = args[0] if args else "pooltoy-water-lab.html"
url = target if "://" in target else "file://" + os.path.abspath(target)

HELPERS = r"""
window.T = {
  click(sel){ const e = document.querySelector(sel); if (e) e.click(); return !!e; },   // a control an older or newer lab lacks is skipped
  // totals in the lab's real litres when it has them (P2-a on), else its old count
  tot(){ if (LAB.amounts){ const a = LAB.amounts(); return {w:a.water, air:a.air, room:a.room, sp:a.spilled}; }
         let w = 0; for (const C of LAB.CO) w += C.V; return {w, air:NaN, room:NaN, sp:0}; },
  bad(){ for (const C of LAB.CO){ for (const k of ["V","c","k","full"]) if (!isFinite(C[k])) return "container " + k;
           for (const v of C.n) if (!isFinite(v)) return "normal"; }
         for (const v of LAB.B.P) if (!isFinite(v)) return "body"; return ""; },
  tilt(){ return Math.acos(Math.max(-1, Math.min(1, LAB.CO[0].n[1]))) * 180 / Math.PI; },
  // step the lab, 4 small steps a picture; watch the totals; optionally keep a trace of every part
  run(pictures, trace, each){ let lo = 1e99, hi = -1e99, alo = 1e99, ahi = -1e99, bad = "", sum = 1e99;
    for (let f = 0; f < pictures; f++){ if (each) each(f); LAB.step(4);
      const t = T.tot(); lo = Math.min(lo, t.w); hi = Math.max(hi, t.w);
      if (isFinite(t.air)){ alo = Math.min(alo, t.air); ahi = Math.max(ahi, t.air); sum = Math.min(sum, t.room - t.w - t.air); }
      if (!bad) bad = T.bad();
      if (trace && f % 6 === 0) trace.push(LAB.CO.map(C => [C.V / (C.full || 1), C.c, C.n[0], C.n[1], C.n[2]])); }
    return {lo, hi, alo, ahi, bad, slackMin: sum}; },
  setup(version, limbs, phys, shape){
    T.click('#shapeSeg button[data-v="' + shape + '"]'); T.click('#verSeg button[data-v="' + version + '"]');
    T.click('#limbSeg button[data-v="' + limbs + '"]'); T.click('#physSeg button[data-v="' + phys + '"]');
    for (let i = 0; i < 120; i++) LAB.step(4); },   // small steps: one big step would be one 2-second picture
  testRun(trace){ T.click('#bTest'); const r = T.run(2500, trace); const s = T.run(240); r.bad = r.bad || s.bad;
    r.tilt = T.tilt(); r.wave = LAB.WV.amp; r.seq = !!LAB.seq; return r; },
  shake(){ let s = 7; const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296 - 0.5; };
    const r = T.run(360, null, f => { if (f % 8 === 0) LAB.B.grab = {tgt:[rnd() * 300, rnd() * 200, rnd() * 300]}; });
    LAB.B.grab = null; const s2 = T.run(1500); r.bad = r.bad || s2.bad; r.lo = Math.min(r.lo, s2.lo); r.hi = Math.max(r.hi, s2.hi);
    r.tilt = T.tilt(); r.wave = LAB.WV.amp; return r; },
  slider(v){ const r = document.querySelector('#slWater input'); r.value = v; r.dispatchEvent(new Event('input', {bubbles:true})); for (let i = 0; i < 60; i++) LAB.step(4); return T.tot(); }
};
"""

fails, notes = [], []
def check(ok, what):
    print(("  ok   " if ok else "  FAIL ") + what)
    if not ok: fails.append(what)

with sync_playwright() as p:
    b = p.chromium.launch()
    def fresh():
        ctx = b.new_context(viewport={"width": 390, "height": 844})
        ctx.add_init_script("window.requestAnimationFrame=()=>0;")           # the page's own loop never runs
        ctx.route("**cdn.jsdelivr.net/**", lambda r: r.abort())               # no three.js: nothing is drawn
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(url); pg.wait_for_function("window.LAB"); pg.evaluate(HELPERS)
        return ctx, pg, errs

    ctx, pg, errs = fresh()
    new = pg.evaluate("!!LAB.amounts")
    print("Lab:", target, "(amounts in real litres)" if new else "(old counting)")
    if new:
        a = pg.evaluate("LAB.amounts()")
        print("  room %.1f L, water %.1f L, air %.1f L; parts: %s" % (a["room"]/1000, a["water"]/1000, a["air"]/1000,
              ", ".join("%s %.1f" % (q["name"], q["room"]/1000) for q in a["parts"])))
    ctx.close()

    # 1. every test move, every combination
    trace = None
    # the Standard fake water and the "As before" physics were removed from the lab on 2026-11-12; a lab that still
    # has them gets them tested too
    ctx, pg, errs = fresh(); old_modes = pg.evaluate("!!document.querySelector('#verSeg')"); ctx.close()
    combos = [("researched","own","new"), ("researched","shared","new")]
    if old_modes: combos += [("researched","own","old"), ("standard","own","new")]
    for version, limbs, phys in combos:
        ctx, pg, errs = fresh()
        name = ("%s / %s / %s" % (version, limbs, phys)) if old_modes else ("own limbs" if limbs == "own" else "one shared surface")
        main = (version, limbs, phys) == ("researched", "own", "new")
        if unit and new: pg.evaluate("LAB.unitFactors(true)")
        pg.evaluate("([a,b,c])=>T.setup(a,b,c,'toy')", [version, limbs, phys])
        r = pg.evaluate("(keep)=>{const tr=keep?[]:null;const r=T.testRun(tr);r.trace=tr;return r}", main)
        if main: trace = r["trace"]
        check(not r["bad"], name + ": no bad numbers" + (" (" + r["bad"] + ")" if r["bad"] else ""))
        check(not r["seq"] and r["tilt"] < 0.5 and r["wave"] < 0.05, name + ": settles flat after the Test run (tilt %.3f deg, waves %.3f)" % (r["tilt"], r["wave"]))
        if version == "researched" and limbs == "own":
            check(r["hi"] - r["lo"] < 1e-6 * max(1, r["hi"]), name + ": water constant through the Test run (%.6f to %.6f L)" % (r["lo"]/1000, r["hi"]/1000))
            if new:
                check(r["ahi"] - r["alo"] < 1e-6 * max(1, r["ahi"]), name + ": air constant (%.6f to %.6f L)" % (r["alo"]/1000, r["ahi"]/1000))
                check(r["slackMin"] > -1e-6, name + ": water + air never more than the room")
            s = pg.evaluate("T.shake()")
            check(not s["bad"] and s["hi"] - s["lo"] < 1e-6 * max(1, s["hi"]), name + ": water constant through a hard shake")
            check(s["tilt"] < 0.5 and s["wave"] < 0.05, name + ": settles flat after the shake (tilt %.3f, waves %.3f)" % (s["tilt"], s["wave"]))
        check(not errs, name + ": no page errors" + (" " + errs[0][:80] if errs else ""))
        ctx.close()

    # 2. the Capsule body: one container, no limbs
    ctx, pg, errs = fresh()
    pg.evaluate("T.setup('researched','own','new','capsule')")
    r = pg.evaluate("(()=>{LAB.jump(1);const a=T.run(300);LAB.flip();const b=T.run(600);LAB.flip();const c=T.run(900);return {bad:a.bad||b.bad||c.bad,lo:Math.min(a.lo,b.lo,c.lo),hi:Math.max(a.hi,b.hi,c.hi),tilt:T.tilt(),n:LAB.CO.filter(C=>C.on).length}})()")
    check(not r["bad"] and not errs, "capsule: jump and flip, no bad numbers or page errors" + (" " + errs[0][:80] if errs else ""))
    check(r["hi"] - r["lo"] < 1e-6 * max(1, r["hi"]) and r["tilt"] < 0.5, "capsule: water constant, settles flat (%d container)" % r["n"])
    ctx.close()

    # 3. P2-a: the Water slider pours once; amounts add up
    if new:
        ctx, pg, errs = fresh()
        pg.evaluate("T.setup('researched','own','new','toy')")
        t0 = pg.evaluate("T.tot()")
        check(abs(t0["w"] - 0.45 * t0["room"]) < 1e-6 * t0["room"], "start: 45%% of the real room is water (%.2f of %.2f L)" % (t0["w"]/1000, t0["room"]/1000))
        check(abs(t0["room"] - t0["w"] - t0["air"]) < 1e-6 * t0["room"], "start: water + air = room (sealed, firm)")
        t1 = pg.evaluate("T.slider(0.6)")
        check(abs(t1["w"] - 0.6 * t1["room"]) < 1e-6 * t1["room"] and abs(t1["room"] - t1["w"] - t1["air"]) < 1e-6 * t1["room"], "slider to 0.6: pours in the difference, the same amount of air leaves")
        pg.evaluate("LAB.flip()"); r = pg.evaluate("T.run(900)")
        check(r["hi"] - r["lo"] < 1e-6 * r["hi"], "after pouring, a flip changes nothing: the slider is not topped up every frame")
        pa = pg.evaluate("LAB.amounts().parts")
        check(all(q["water"] <= q["room"] * (1 + 1e-9) and q["water"] >= -1e-9 for q in pa), "no part holds more water than its room")
        t2 = pg.evaluate("T.slider(0)"); t3 = pg.evaluate("T.slider(1)")
        check(t2["w"] < 1e-6 and abs(t3["w"] - t3["room"]) < 1e-6 * t3["room"], "slider to 0 empties him, to 1 fills him")
        check(t3["sp"] == 0, "nothing spilled")
        ctx.close()
    b.close()

if save:
    json.dump(trace, open(save, "w")); print("saved the Test run's levels to", save)
if against:
    old = json.load(open(against)); worst = 0.0; where = None
    n = min(len(old), len(trace))
    for f in range(n):
        for i in range(min(len(old[f]), len(trace[f]))):
            for k in range(5):
                d = abs(old[f][i][k] - trace[f][i][k])
                if d > worst: worst, where = d, (f, i, k)
    check(len(old) == len(trace) and worst < 1e-6, "Test run matches %s: biggest difference %.2e over %d pictures x %d parts" % (against, worst, n, len(trace[0])))

print("\n%d failure%s" % (len(fails), "" if len(fails) == 1 else "s"))
sys.exit(1 if fails else 0)
