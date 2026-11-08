import sys
FILE=sys.argv[1]
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/9b8c3389-c9fc-524a-8264-10da380c42ec/scratchpad/'
TJS=open(S+'three/node_modules/three/build/three.module.js').read()
WRAP=r'''()=>{window.PROF={};const wrap=(name,get,set)=>{const f=get();set(function(...a){const t=performance.now();const r=f.apply(this,a);const d=performance.now()-t;const p=PROF[name]||(PROF[name]={n:0,ms:0});p.n++;p.ms+=d;return r})};
 wrap("record (save snapshot)",()=>hRecord,f=>window.hRecord=f);wrap("restore (rewind)",()=>hRestore,f=>window.hRestore=f);
 wrap("pose: sergal",()=>buildRig,f=>window.buildRig=f);wrap("pose: robot",()=>buildRobot,f=>window.buildRobot=f);
 wrap("draw: 3D (three.js)",()=>r3render,f=>window.r3render=f);wrap("draw: built-in",()=>render,f=>window.render=f);
 wrap("  of which three.js render()",()=>R3.rd.render.bind(R3.rd),f=>R3.rd.render=f);wrap("whole frame",()=>frame,f=>window.frame=f);wrap("gait chart + status",()=>drawGait,f=>window.drawGait=f)}'''
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    for ch in ['sergal','robot','sergal','robot']:
        for rend in ['three']:
            for scen in ['playing']:
                pg=b.new_page(viewport={'width':390,'height':844})
                pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,body=TJS,headers={'content-type':'application/javascript','access-control-allow-origin':'*'}))
                pg.goto('http://localhost:8765/'+FILE);pg.wait_for_timeout(1500)
                pg.evaluate(f'()=>{{document.querySelector(\'#rendSw [data-r="{rend}"]\').click();$("charSel").value="{ch}";$("charSel").onchange();hClear();if(!playing)$("play").onclick();$("modeSel").value="walk";$("modeSel").onchange()}}')
                pg.wait_for_timeout(2500)
                if scen=='rewinding (replay)':pg.evaluate('()=>{const s=$("scrub");if(playing)$("play").onclick();s.value=0.05;s.dispatchEvent(new Event("input",{bubbles:true}));$("play").onclick()}')
                pg.evaluate(WRAP)
                if scen=='switching animations':
                    pg.evaluate('()=>{const ms=MODES.map(m=>m[0]);let i=0;window.SW=setInterval(()=>{$("modeSel").value=ms[i++%ms.length];$("modeSel").onchange()},400)}')
                pg.wait_for_timeout(3000)
                r=pg.evaluate('PROF');pg.close()
                fr=r.get('whole frame',{'n':1,'ms':0});print(f'\n{ch} | {rend} | {scen}: {fr["n"]} frames, {fr["ms"]/max(1,fr["n"]):.2f} ms per frame')
                for k,v in sorted(r.items(),key=lambda kv:-kv[1]['ms']):
                    if k=='whole frame' or v['n']==0:continue
                    print(f'   {k:24s} {v["ms"]/max(1,fr["n"]):6.2f} ms/frame  ({100*v["ms"]/max(1e-9,fr["ms"]):4.0f}%)')
    b.close()
