import json,sys
from playwright.sync_api import sync_playwright
SIM=r"""
window.requestAnimationFrame=()=>0;R3.want="2d";
window.simStep=(dt)=>{const bt=+$("blend").value;
 if(playing||!STEPBLEND)blendU=bt<=0?1:Math.min(1,blendU+dt/bt);
 const u=ease(blendU),tg=P[mode];for(const k in tg)cur[k]=from[k]+(tg[k]-from[k])*u;
 const th0=2*Math.PI*phase,fb=Math.sin(th0*Math.round(from.bobMul));cur.bobWave=fb+(Math.sin(th0*Math.round(tg.bobMul))-fb)*u;
 springStep(dt);turnStep();gameStep(dt);walkoverStep();if(playing)advance(dt*effSpeed());flipStep();hPre();charDef().build({...cur},phase)};
window.setChar=(c,m)=>{$("charSel").value=c;$("charSel").onchange();if(m){$("modeSel").value=m;$("modeSel").onchange()}};
window.snap=()=>({ft:FLIP?flipT():null,kind:FLIP?FLIP.kind:null,mode,blendU,phase,POS:[...POS],HEAD,go:groundOff,W:globalThis.ROBWORLD||(typeof ROBCH!=='undefined'&&ROBCH?ROBCH.ch:null),w:globalThis.ROBW||(typeof ROBCH!=='undefined'&&ROBCH?ROBCH.w:null),nu:!!(FLIP&&FLIP.nu),cl:(typeof ROBCH!=='undefined'&&ROBCH?ROBCH.ch.map(c=>c[3][1]-ground(c[3][0],c[3][2])):null),bad:BONEBAD,seg:SEGDBG,wo:WALKOVER?WALKOVER.stage:0,sw:SWAP});
"""
def open_page(pw,url,w=390,h=844):
    b=pw.chromium.launch()
    pg=b.new_page(viewport={"width":w,"height":h})
    pg.route("**/*jsdelivr*",lambda r:r.abort())
    errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(600)
    pg.evaluate(SIM)
    return b,pg,errs
def world(s,p):
    import math
    c,sn=math.cos(s["HEAD"]),math.sin(s["HEAD"])
    return [s["POS"][0]+p[0]*c+p[2]*sn,p[1],s["POS"][1]-p[0]*sn+p[2]*c]
