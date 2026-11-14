#!/usr/bin/env python3
"""pt_mixmo.py - the Pooltoy character inside Mixmo (M3), live in a test browser with three.js served from disk.
usage: pt_mixmo.py Mixmo.html outdir [model.glb]   (THREE_DIR: three.js r170, default node_modules/three)"""
import asyncio,sys,os,json
MIXF,OUTD=sys.argv[1],sys.argv[2];GLBF=sys.argv[3] if len(sys.argv)>3 else None;sys.argv=['x','-','-','/tmp']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shots.py')).read().split('async def main')[0])
fails=[]
def check(ok,w): print(('  ok   ' if ok else '  FAIL ')+w); (None if ok else fails.append(w))
async def main():
    os.makedirs(OUTD,exist_ok=True)
    async with async_playwright() as pw:
        b,pg,errs=await page(pw,MIXF,"try{localStorage.setItem('mixmoTier','anim')}catch(e){}",stop=False)
        await pg.wait_for_function("typeof R3!=='undefined'&&R3.ok",timeout=120000,polling=250)
        w="const w=ms=>new Promise(r=>setTimeout(r,ms));const sel=v=>{$('charSel').value=v;$('charSel').onchange()};const ms=v=>{$('modeSel').value=v;$('modeSel').onchange()};"
        r=await pg.evaluate("async()=>{"+w+"""sel('pooltoy');await w(500);const L=PTH.L;return {on:PTH.on,panel:!$('ptPanel').hidden,view:!$('ptView').hidden,flip:!$('tF').hidden,parts:$('sergalParts').hidden,
          title:document.querySelector('#bot h1').textContent,menu:[...$('modeSel').options].map(o=>o.textContent),scrub:$('scrub').disabled,lab:!!window.LAB&&window.LAB===L}}""")
        check(r['on'] and r['panel'] and r['view'] and r['flip'] and r['parts'] and r['scrub'] and r['lab'],"Pooltoy chosen: drawn, his panel and numbers shown, Flip shown, the sergal's panels hidden, scrubbing greyed out (%s)"%r['title'])
        check(r['menu']==["Stand","Walk","Run","Jump","Drop (from high up)","Test run (pooltoy only)"],"his menu: "+", ".join(r['menu']))
        r=await pg.evaluate("async()=>{"+w+"""const L=PTH.L,B=L.B,o={};ms('walk');await w(200);o.walk=B.speedT;ms('run');await w(1500);o.run=B.speedT;o.speed=B.speed;
          o.pos=Math.hypot(POS[0]-B.x,POS[1]-B.z)<1e-6&&HEAD===B.head;o.posd=[POS,B.x,B.z,HEAD,B.head];o.moved=Math.hypot(B.x,B.z);ms('idle');await w(200);o.idle=B.speedT;
          $('tL').click();o.turn=B.headT;await w(1500);$('tS').click();await w(300);o.spin=B.spin&&$('tS').classList.contains('on');$('tS').click();await w(100);o.wind=!B.spin&&B.headT!==null;await w(2500);
          o.f0=[B.up,!!B.flip,B.vm,B.spin];$('tF').click();o.f1=[B.up,!!B.flip,B.vm];await w(1500);o.up=B.up;while(B.flip||B.vm!=='ground')await w(100);$('tF').click();await w(100);o.back=!B.up;while(B.flip||B.vm!=='ground')await w(100);
          ms('jump');await w(100);o.jump=B.vm!=='ground';o.menuBack=$('modeSel').value;await w(1500);
          ms('walk');await w(300);$('play').onclick();o.playing=playing;await w(100);const z1=B.z,x1=B.x;await w(600);o.paused=B.z===z1&&B.x===x1;$('play').onclick();ms('idle');
          return o}""")
        check(r['walk']==62 and r['run']==175 and r['idle']==0,"Stand / Walk / Run set his speed (62, 175, 0)")
        check(r['pos'] and r['moved']>20,"Mixmo follows him: its position and heading are his (ran %.0f)"%r['moved'])
        check(abs(r['turn']-1.5707963)<1e-3,"Turn left 90: he turns himself")
        check(r['spin'] and r['wind'],"Spin on, then off: winds down to the next quarter turn")
        check(r["up"] and r["back"],"Flip: upside down, then back (%s %s)"%(r["up"],r["back"]))
        check(r['jump'] and r['menuBack']=='idle',"Jump plays once, the menu goes back to Stand")
        check(r['paused'],"Pause: he stops")
        r=await pg.evaluate("async()=>{"+w+"""const L=PTH.L,o={};ms('test');await w(1200);o.seq=!!L.seq;o.status=$('stText').textContent;L.testStop();await w(300);o.after=$('modeSel').value;return o}""")
        check(r['seq'] and r['status'].startswith('Test run'),"Test run plays from the menu: "+r['status'])
        check(r['after']=='idle',"after the Test run the menu is back on Stand")
        await pg.evaluate("async()=>{"+w+"for(let i=0;i<120;i++)PTH.L.step(4);render()}")
        await pg.locator('#view').screenshot(path=os.path.join(OUTD,'m3_pooltoy_in_mixmo.png'))
        # Game mode: Mixmo's keys steer him
        r=await pg.evaluate("async()=>{"+w+"""TIER='game';devUI();gameEnter();const B=PTH.L.B,o={};
          dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW'}));await w(1500);o.run=B.speedT;o.mode=$('modeSel').value;
          dispatchEvent(new KeyboardEvent('keyup',{code:'KeyW'}));dispatchEvent(new KeyboardEvent('keydown',{code:'KeyS'}));await w(80);o.rev=!!PTREV;o.revFast=PTREV&&PTREV.fast;await w(1500);
          dispatchEvent(new KeyboardEvent('keyup',{code:'KeyS'}));await w(800);o.stop=B.speedT;TIER='anim';devUI();return o}""")
        check(r['run']==175 and r['mode']=='run',"Game mode: W runs him (menu shows Run)")
        check(r['rev'] and r['revFast'],"Game mode: a flick back on a run turns him round with a skid")
        check(r['stop']==0,"Game mode: letting go stops him")
        # back and forth: no errors, keys only reach the one on screen
        r=await pg.evaluate("async()=>{"+w+"""const o={};for(let i=0;i<10;i++){sel(i%2?'pooltoy':'sergal2');await w(80)}sel('sergal2');await w(200);
          o.off=!PTH.on&&!R3.sc.getObjectByName('pooltoy').visible&&$('ptPanel').hidden;TIER='game';devUI();gameEnter();const s0=PTH.L.B.speedT;
          dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW'}));await w(500);o.keys=PTH.L.B.speedT===s0&&mode==='run';dispatchEvent(new KeyboardEvent('keyup',{code:'KeyW'}));TIER='anim';devUI();
          o.scrub=!$('scrub').disabled;return o}""")
        check(r['off'],"ten switches, back on the sergal: the pooltoy hidden, his panel hidden")
        check(r['keys'],"Game keys on the sergal move the sergal, not the hidden pooltoy")
        check(r['scrub'],"scrubbing is back for the sergal")
        # his own animations show him on his own: a model beside him steps out of the picture during the Test run
        if GLBF:
            await pg.set_input_files('#mdlFile',GLBF)
            await pg.wait_for_function("MODELS.length>0&&MODELS[0].grp",timeout=300000,polling=500)
            r=await pg.evaluate("async()=>{"+w+"""sel('pooltoy');await w(300);const M=MODELS[0],o={};o.before=M.grp.visible;ms('test');await w(400);o.during=M.grp.visible;
              ms('idle');await w(400);o.after=M.grp.visible;sel('sergal2');await w(300);o.sergal=M.grp.visible;return o}""")
            check(r['before'] and not r['during'] and r['after'] and r['sergal'],"a model beside him: hidden during his Test run, back after it and for the sergal")
            await pg.evaluate("async()=>{"+w+"sel('pooltoy');await w(500)}")
            await pg.locator('#ptPanel').screenshot(path=os.path.join(OUTD,'m3_panel.png'))
        r=await pg.evaluate("async()=>{"+w+"""const o={};document.querySelector('#rendSw button[data-r="canvas"]').click();await w(300);o.note=$('r3msg').textContent;o.shown=$('r3msg').style.display;
          document.querySelector('#rendSw button[data-r="three"]').click();await w(800);o.back=PTH.on&&$('r3msg').style.display==='none';return o}""")
        check(r['note'].startswith('The Pooltoy is drawn in 3D only') and r['shown']=='block' and r['back'],"2D renderer: a note in the view; back to 3D he's drawn again ("+r['note'][:60]+")")
        check(not errs,"no page errors"+(" "+errs[0][:100] if errs else ""))
        await b.close()
    print("\n%d failures"%len(fails));sys.exit(1 if fails else 0)
asyncio.run(main())
