# every robot mode pair + flips: report max raw bone violation (before the clamp) via BONEBAD and SEGDBG
from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page()
    pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(500)
    print(pg.evaluate('''()=>{if(playing)$("play").onclick();STEPBLEND=true;$("charSel").value="robot";$("charSel").onchange();const o={};BONETOL=1;
     const fb=()=>{const tg=P[mode],u=ease(blendU);for(const k in tg)cur[k]=from[k]+(tg[k]-from[k])*u;cur.bobWave=Math.sin(2*Math.PI*phase);springStep(1/60);flipStep();if(typeof walkoverStep==="function")walkoverStep()};
     const run=(lbl,n)=>{for(let i=0;i<n;i++){stepFrame(1);fb();buildRobot(cur,phase);chains_check(lbl)}};
     window.chains_check=lbl=>{for(let k=0;k<SEGDBG.length;k++)for(let j=0;j<SEGDBG[k].length;j++){const r=SEGDBG[k][j];const e=Math.abs(r-1);if(!(lbl in o)||e>o[lbl].e)o[lbl]={e:+e.toFixed(3),limb:RLIMBS[k].k,seg:j}}};
     const modes=MODES.map(m=>m[0]),sel=$("modeSel");
     for(const a of modes)for(const bb of modes){if(a===bb)continue;sel.value=a;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;GECKO=false;SWAP=false;run(a,3);sel.value=bb;sel.onchange();run(a+">"+bb,150)}
     for(const m of modes){sel.value=m;sel.onchange();blendU=1;BLENDFROM=null;FLIP=null;GECKO=false;SWAP=false;run(m,5);startFlip("up");run(m+" ceil",60);startFlip("down");run(m+" drop",60);$("tF").onclick();run(m+" over",300);startTurn("S");run(m+" spin",100);startTurn("S")}
     return Object.entries(o).filter(([k,v])=>v.e>0.03).map(([k,v])=>k+" "+JSON.stringify(v)).join("\\n")||"all bones within 3%"}'''))
    b.close()
