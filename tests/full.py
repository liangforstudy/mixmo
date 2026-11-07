from playwright.sync_api import sync_playwright
JS=r"""async()=>{
 const fails=[],note=[];const bad=()=>prims.some(q=>(q.a&&q.a.some(v=>!isFinite(v)))||(q.pts&&q.pts.some(v=>v.some(x=>!isFinite(x)))));
 const tick=()=>{showFrame();showStatus();(CHAR==="robot"?buildRobot:buildRig)(cur,phase)};
 const frameBlend=()=>{const tg=P[mode],u=ease(blendU);for(const k in tg)cur[k]=from[k]+(tg[k]-from[k])*u;const th0=2*Math.PI*phase,fb=Math.sin(th0*Math.round(from.bobMul||1));cur.bobWave=fb+(Math.sin(th0*Math.round(tg.bobMul||1))-fb)*u;springStep(1/60);flipStep();if(typeof walkoverStep==="function")walkoverStep()};
 const step=d=>{stepFrame(d);frameBlend();tick()};
 const scrub=v=>{$("scrub").value=v;$("scrub").dispatchEvent(new Event("input"));frameBlend();tick()};
 const chk=(lbl)=>{if(bad())fails.push(lbl+": NaN/Infinity in pose");};
 if(playing)$("play").onclick();STEPBLEND=true;
 for(const ch of ["sergal","robot"]){
  $("charSel").value=ch;$("charSel").onchange();
  const modes=MODES.map(m=>m[0]);
  // 1) every pair of modes: blend forward by steps, back by steps, scrub to middle/start/end
  for(const a of modes)for(const b of modes){if(a===b)continue;
   const sel=$("modeSel");sel.value=a;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;frameBlend();tick();
   sel.value=b;sel.onchange();await new Promise(r=>setTimeout(r,0));frameBlend();tick();
   const lbl=`${ch} ${a}->${b}`;
   if(!morphNow()&&b!==a){ if(!(FLIP))fails.push(lbl+": no morph after switch");}
   const u0=blendU;for(let i=0;i<4;i++)step(1);const u1=blendU;if(!(u1>u0))fails.push(lbl+": stepping forward did not advance blend");
   for(let i=0;i<2;i++)step(-1);if(!(blendU<u1))fails.push(lbl+": stepping back did not rewind blend");
   if(morphNow()&&morphNow().name==="blend"){scrub(0.5);if(Math.abs(blendU-0.5)>0.02)fails.push(lbl+": scrub to 0.5 gave "+blendU.toFixed(2));
    scrub(0.1);if(Math.abs(blendU-0.1)>0.02)fails.push(lbl+": scrub back gave "+blendU.toFixed(2));}
   // finish everything (blend + any rise flip)
   for(let i=0;i<400&&(morphNow()||FLIP||WALKOVER);i++)step(1);
   if(morphNow()||FLIP)fails.push(lbl+": morph never finished");
   if($("stTag").textContent!=="LOOP")fails.push(lbl+": status not LOOP at end ("+$("stText").textContent+")");
   if(mode!==b)fails.push(lbl+": ended in "+mode);
   chk(lbl)}
  // 2) turns in every mode: forward steps complete them; back steps must not break
  for(const m of modes){const sel=$("modeSel");sel.value=m;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;
   for(const k of ["L","R","U"]){HEAD=HEAD_T=0;OMEGA=0;TURN={st:null,t:0};TRAVK=1;SKIDLEAN=0;BOOST=0;TURNM=null;
    const want={L:90,R:-90,U:180,S:360}[k],L=`${ch} ${m} turn ${k}`;
    if(ch==="robot"&&LYING.has(m)&&k==="U"){LYTURN="swap";   // on all six a 180 swaps which end leads instead of spinning round
     DIR=1;startTurn("U");if(!morphNow()||morphNow().name!=="turn")fails.push(L+": swap-ends turn is not a morph");
     for(let i=0;i<5;i++)step(1);const d1=DIR;for(let i=0;i<2;i++)step(-1);if(!(DIR>d1))fails.push(L+": stepping back did not undo");
     for(let i=0;i<200&&TURNM;i++)step(-1);if(TURNM||DIR!==1)fails.push(L+": stepping back past start did not cancel");
     startTurn("U");for(let i=0;i<900&&TURNM;i++)step(1);
     if(DIR!==-1||Math.abs(HEAD)>1e-6)fails.push(L+": ended DIR "+DIR+" head "+HEAD);
     tick();if($("stTag").textContent!=="LOOP")fails.push(L+": status not LOOP at end");chk(L);DIR=1;
     LYTURN="turn";HEAD=HEAD_T=0;startTurn("U");for(let i=0;i<1500&&TURNM;i++)step(1);   // the other choice: swing the body round
     if(Math.round(HEAD*180/Math.PI)!==180)fails.push(L+" (turn round): ended at "+Math.round(HEAD*180/Math.PI));
     LYTURN="swap";HEAD=HEAD_T=0;continue}
    startTurn(k);if(!morphNow()||morphNow().name!=="turn")fails.push(L+": turn is not a morph");
    if($("stTag").textContent!=="MORPH"){tick();if($("stTag").textContent!=="MORPH")fails.push(L+": status not MORPH")}
    for(let i=0;i<3;i++)step(1);const h1=Math.abs(HEAD);for(let i=0;i<2;i++)step(-1);
    if(!(Math.abs(HEAD)<h1||h1<1e-3))fails.push(L+": stepping back did not unturn");
    scrub(0.5);const hm=HEAD*180/Math.PI;scrub(0.2);const hb=HEAD*180/Math.PI;
    if(!(Math.abs(hb)<Math.abs(hm)))fails.push(L+": scrubbing back did not unturn ("+hm.toFixed(0)+" -> "+hb.toFixed(0)+")");
    for(let i=0;i<200&&TURNM;i++)step(-1);if(TURNM||Math.abs(HEAD)>1e-6)fails.push(L+": stepping back past start did not cancel (head "+(HEAD*57.3).toFixed(1)+")");
    startTurn(k);for(let i=0;i<900&&TURNM;i++)step(1);
    const got=Math.round(HEAD*180/Math.PI);if(got!==want)fails.push(L+": ended at "+got+" (want "+want+")");
    if(TURNM||TURN.st)fails.push(L+": still turning");
    tick();if($("stTag").textContent!=="LOOP")fails.push(L+": status not LOOP at end");
    chk(`${ch} ${m} turn ${k}`)}
   // spin is a loop: toggled on, keeps turning, status stays LOOP, steps back un-spin, toggled off holds heading
   HEAD=HEAD_T=0;TURNM=null;SPIN=null;startTurn("S");for(let i=0;i<10;i++)step(1);const h10=HEAD;
   if(!(h10>0.1))fails.push(`${ch} ${m} spin: not turning`);tick();if($("stTag").textContent!=="LOOP")fails.push(`${ch} ${m} spin: status not LOOP`);
   for(let i=0;i<5;i++)step(-1);if(!(HEAD<h10))fails.push(`${ch} ${m} spin: stepping back did not unspin`);
   for(let i=0;i<60;i++)step(1);startTurn("S");const hOff=HEAD;for(let i=0;i<10;i++)step(1);if(Math.abs(HEAD-hOff)>1e-6)fails.push(`${ch} ${m} spin: kept turning after stop`);
   chk(`${ch} ${m} spin`);SPIN=null;HEAD=HEAD_T=0}

  HEAD=HEAD_T=0;OMEGA=0;TURNM=null;BOOST=0;SPIN=null;
  if(ch!=="robot")continue;
  // 3) robot moves in every mode: ceiling up/down, over, with forward + backward stepping and scrubbing
  for(const m of modes){const sel=$("modeSel");sel.value=m;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;GECKO=false;SWAP=false;WALKOVER=null;
   const lbl=`robot ${m}`;
   // ceiling
   startFlip("up");if(!FLIP){fails.push(lbl+": ceiling did not start");continue}
   for(let i=0;i<5;i++)step(1);const t1=flipT();step(-1);step(-1);if(!(flipT()<t1))fails.push(lbl+": ceiling step back did not rewind");
   scrub(0.6);if(Math.abs(flipT()-0.6)>0.03)fails.push(lbl+": ceiling scrub 0.6 -> "+flipT().toFixed(2));
   scrub(0.2);if(Math.abs(flipT()-0.2)>0.03)fails.push(lbl+": ceiling scrub back -> "+flipT().toFixed(2));
   for(let i=0;i<20;i++)step(-1);if(FLIP)fails.push(lbl+": stepping back past start did not cancel ceiling flip");
   if(GECKO)fails.push(lbl+": on ceiling after cancelling");
   startFlip("up");scrub(1);if(FLIP||!GECKO)fails.push(lbl+": scrubbing to end did not land on ceiling");
   for(let i=0;i<10;i++)step(1);chk(lbl+" on ceiling");
   startFlip("down");for(let i=0;i<400&&FLIP;i++)step(1);if(GECKO)fails.push(lbl+": drop did not return to floor");
   // over (walkover)
   const sw0=SWAP;$("tF").onclick();for(let i=0;i<3;i++)step(1);for(let i=0;i<2;i++)step(-1);
   for(let i=0;i<900&&(WALKOVER||FLIP||morphNow());i++)step(1);
   if(WALKOVER||FLIP)fails.push(lbl+": over never finished");
   if(SWAP===sw0)fails.push(lbl+": over did not swap ends");
   const expect=m==="run6"?"run":m;if(mode!==expect)fails.push(lbl+": over ended in "+mode+" (want "+expect+")");
   chk(lbl+" over")}
  // 4) leaving six legs with each stand-up choice
  for(const se of ["keep","front","A","B"]){const sel=$("modeSel");SWAP=false;GECKO=false;FLIP=null;
   sel.value="run6";sel.onchange();blendU=1;BLENDFROM=null;STANDEND=se;const b0=bottomEnd();
   sel.value="walk";sel.onchange();await new Promise(r=>setTimeout(r,0));
   for(let i=0;i<5;i++)step(1);for(let i=0;i<3;i++)step(-1);
   for(let i=0;i<600&&(FLIP||morphNow());i++)step(1);
   const want=se==="keep"?b0:se==="front"?(b0==="A"?"B":"A"):se;
   if(bottomEnd()!==want)fails.push(`robot leave-six ${se}: bottom ${bottomEnd()} want ${want}`)}
  STANDEND="keep";}
 return {fails,count:fails.length}}"""

# ---- merged checks: bone lengths (was bones.py) and planted-paw slide (was slide.py) ----
BONES=r"""()=>{if(playing)$("play").onclick();STEPBLEND=true;$("charSel").value="robot";$("charSel").onchange();const o={};const tol0=BONETOL;BONETOL=1;
 const fb=()=>{const tg=P[mode],u=ease(blendU);for(const k in tg)cur[k]=from[k]+(tg[k]-from[k])*u;cur.bobWave=Math.sin(2*Math.PI*phase);springStep(1/60);flipStep();if(typeof walkoverStep==="function")walkoverStep()};
 const chk=lbl=>{for(let k=0;k<SEGDBG.length;k++)for(let j=0;j<SEGDBG[k].length;j++){const e=Math.abs(SEGDBG[k][j]-1);if(!(lbl in o)||e>o[lbl].e)o[lbl]={e:+e.toFixed(3),limb:RLIMBS[k].k,seg:j}}};
 const run=(lbl,n)=>{for(let i=0;i<n;i++){stepFrame(1);fb();buildRobot(cur,phase);chk(lbl)}};
 const modes=MODES.map(m=>m[0]),sel=$("modeSel");
 for(const a of modes)for(const bb of modes){if(a===bb)continue;sel.value=a;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;GECKO=false;SWAP=false;run(a,3);sel.value=bb;sel.onchange();run(a+">"+bb,150)}
 for(const m of modes){sel.value=m;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;GECKO=false;SWAP=false;run(m,5);startFlip("up");run(m+" ceil",60);startFlip("down");run(m+" drop",60);$("tF").onclick();run(m+" over",300);startTurn("S");run(m+" spin",100);startTurn("S")}
 BONETOL=tol0;const worst=Math.max(0,...Object.values(o).map(v=>v.e));
 return {worst,bad:Object.entries(o).filter(([k,v])=>v.e>0.03).map(([k,v])=>"bones "+k+" "+JSON.stringify(v))}}"""
SLIDE=r"""(spin)=>{const out=[];if(playing)$("play").onclick();STEPBLEND=true;$("charSel").value="robot";$("charSel").onchange();
 const fb=()=>{const tg=P[mode],u=ease(blendU);for(const k in tg)cur[k]=from[k]+(tg[k]-from[k])*u;const th0=2*Math.PI*phase,f0=Math.sin(th0*Math.round(from.bobMul||1));cur.bobWave=f0+(Math.sin(th0*Math.round(tg.bobMul||1))-f0)*u;springStep(1/60);flipStep()};
 let all=0;
 for(const m of MODES.map(x=>x[0])){const sel=$("modeSel");sel.value=m;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;GECKO=false;
  HEAD=HEAD_T=0;OMEGA=0;TURNM=null;SPIN=null;TRAVK=1;BOOST=0;fb();buildRobot(cur,phase);if(spin)startTurn("S");
  let prev=null,worst=0,wk="";
  for(let i=0;i<240;i++){stepFrame(1);fb();buildRobot(cur,phase);
   // planted = full weight and at rest height; a paw that has started to rise is lifting off, not sliding
   const sh=ROBFEET.map(f=>({g:f.w>0.5&&f.p[1]<3.25,x:f.p[0]+POS[0],z:f.p[2]+POS[1]}));
   if(prev&&i>30)sh.forEach((s,k)=>{const q=prev[k];if(s.g&&q.g){const d=Math.hypot(s.x-q.x,s.z-q.z);if(d>worst){worst=d;wk=k+"@"+i}}});prev=sh}
  all=Math.max(all,worst);if(worst>0.05)out.push((spin?"spin ":"straight ")+m+" slide "+worst.toFixed(3)+" paw "+wk);SPIN=null}
 return {worst:all,bad:out}}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(400)
    r=pg.evaluate(JS)
    bo=pg.evaluate(BONES);r['fails']+=bo['bad']
    sl=[pg.evaluate(SLIDE,False),pg.evaluate(SLIDE,True)];[r['fails'].extend(x['bad']) for x in sl]
    r['count']=len(r['fails'])
    print('failures:',r['count'])
    print(f"worst bone change {bo['worst']*100:.2f}% (limit 3%); worst planted-paw slide {max(x['worst'] for x in sl):.3f} (limit 0.05)")
    for f in r['fails'][:60]:print(' -',f)
    print('PAGE ERRORS',errs[:5]);b.close()
