from playwright.sync_api import sync_playwright
import sys
JS=r"""(spin)=>{const out=[];if(playing)$("play").onclick();STEPBLEND=true;
 const frameBlend=()=>{const tg=P[mode],u=ease(blendU);for(const k in tg)cur[k]=from[k]+(tg[k]-from[k])*u;const th0=2*Math.PI*phase,fb=Math.sin(th0*Math.round(from.bobMul||1));cur.bobWave=fb+(Math.sin(th0*Math.round(tg.bobMul||1))-fb)*u;springStep(1/60);flipStep()};
 for(const ch of ["robot"]){$("charSel").value=ch;$("charSel").onchange();
 for(const m of MODES.map(x=>x[0])){const sel=$("modeSel");sel.value=m;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;GECKO=false;
  HEAD=HEAD_T=0;OMEGA=0;TURNM=null;SPIN=null;TRAVK=1;BOOST=0;frameBlend();buildRobot(cur,phase);if(spin)startTurn("S");
  let prev=null,worst=0,wk="",gc=0;
  for(let i=0;i<240;i++){stepFrame(1);frameBlend();if(typeof turnStep==="function"&&!spin)0;(CHAR==="robot"?buildRobot:buildRig)(cur,phase);
   const sh=ROBFEET.map(f=>({g:f.w>0.5&&f.p[1]<3.25,x:f.p[0]+POS[0],z:f.p[2]+POS[1]}));
   gc+=sh.filter(s=>s.g).length;if(prev&&i>30)sh.forEach((s,k)=>{const p=prev[k];if(s.g&&p.g){const d=Math.hypot(s.x-p.x,s.z-p.z);if(d>worst){worst=d;wk=k+"@"+i}}});
   prev=sh}
  out.push(ch+" "+m+" "+worst.toFixed(2)+" head "+(HEAD*57.3).toFixed(0)+" "+wk+" "+JSON.stringify(ROBFEET[0].p.map(v=>+v.toFixed(1))));SPIN=null}}
 return out}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('http://localhost:8765/'+(sys.argv[1] if len(sys.argv)>1 else 'Mixmo.html'));pg.wait_for_timeout(400)
    for s in [False,True]:
        print('SPIN' if s else 'STRAIGHT');[print(' ',x) for x in pg.evaluate(JS,s)]
    b.close()
