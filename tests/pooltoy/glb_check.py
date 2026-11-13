#!/usr/bin/env python3
"""GLB water checks for the lab (stand-in for lab.py --glb, which the attached lab.py lacks).
usage: glb_check.py lab.html model.glb [--save t.json] [--against t.json]"""
import sys, os, json, asyncio
sys.path.insert(0, os.path.dirname(__file__))
args=sys.argv[1:]
def opt(n):
    if n in args: i=args.index(n); v=args[i+1]; del args[i:i+2]; return v
save,against=opt('--save'),opt('--against'); LABF,GLB=args[:2]
src=open(os.path.join(os.path.dirname(__file__),'shots.py')).read().split('async def main')[0]
sys.argv=['x','-','-','/tmp']; exec(src)
LABH=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lab.py')).read().split('HELPERS = r"""')[1].split('"""')[0]
fails=[]
def check(ok,w): print(('  ok   ' if ok else '  FAIL ')+w); (None if ok else fails.append(w))
async def main():
    async with async_playwright() as pw:
        b,pg,errs=await page(pw,LABF)
        await pg.wait_for_function("window.LAB&&LAB.R3&&LAB.R3.ok",timeout=120000,polling=250)
        await pg.evaluate(LABH)
        await pg.set_input_files('#glbFile',GLB)
        await pg.wait_for_function("/Room inside|couldn't|wrong|isn't/.test(document.getElementById('glbMsg').textContent)",timeout=300000,polling=500)
        print(' ', (await pg.inner_text('#glbMsg'))[:120])
        a=await pg.evaluate("()=>{for(let i=0;i<120;i++)LAB.step(4);return LAB.amounts()}")
        check(all(q['room']>0 for q in a['parts']),'every container has room: '+', '.join('%s %.1f'%(q['name'],q['room']/1000) for q in a['parts']))
        check(abs(a['water']-0.45*a['room'])<1e-6*a['room'],'45%% poured exactly (%.3f of %.3f L)'%(a['water']/1000,a['room']/1000))
        r=await pg.evaluate("()=>{const tr=[];const r=T.testRun(tr);r.trace=tr;return r}")
        check(not r['bad'] and r['hi']-r['lo']<1e-6*r['hi'],'Test run: no bad numbers, water constant')
        check(r['tilt']<0.5 and r['wave']<0.05,'Test run: settles flat (tilt %.3f, waves %.3f)'%(r['tilt'],r['wave']))
        s=await pg.evaluate("T.shake()")
        check(not s['bad'] and s['hi']-s['lo']<1e-6*s['hi'] and s['tilt']<0.5,'hard shake: water constant, settles flat')
        t=await pg.evaluate("""()=>{T.slider(0.1);const f=document.querySelector('#slFlat input');f.value=1;f.dispatchEvent(new Event('input',{bubbles:true}));
          const w0=T.tot().w;for(let i=0;i<600;i++)LAB.step(4);const a=LAB.amounts();
          f.value=0;f.dispatchEvent(new Event('input',{bubbles:true}));for(let i=0;i<600;i++)LAB.step(4);const z=T.tot();
          return {w0,w1:a.water,flats:a.parts.map(q=>[q.name,q.flat]),wz:z.w,az:z.air,rz:z.room}}""")
        check(abs(t['w1']-t['w0'])<1e-6*max(1,t['w0']),'10% water at Flat 1: water constant; flat per part: '+', '.join('%s %.2f'%(n,f) for n,f in t['flats']))
        check(abs(t['rz']-t['wz']-t['az'])<1e-6*t['rz'],'back to round: water + air = room')
        check(not errs,'no page errors'+(' '+errs[0][:80] if errs else ''))
        await b.close()
        if save: json.dump(r['trace'],open(save,'w')); print('saved',save)
        if against:
            old=json.load(open(against)); tr=r['trace']; worst=max(abs(x-y) for fo,fn in zip(old,tr) for po,pn in zip(fo,fn) for x,y in zip(po,pn))
            check(len(old)==len(tr) and worst<1e-6,'Test run matches %s (biggest difference %.2e)'%(against,worst))
asyncio.run(main()); print('\n%d failures'%len(fails)); sys.exit(1 if fails else 0)
