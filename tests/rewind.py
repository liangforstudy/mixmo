# Rewind test: plays a session per character, then rewinds to many points and checks the restored pose matches what
# played (within 0.05), that stepping back 5 / forward 5 returns to the same frame, that Play from the middle reaches
# "now", and that a change while rewound cuts the history there. Run with: python3 -m http.server 8765 + python3 rewind.py
from playwright.sync_api import sync_playwright
KEY='()=>prims.map(q=>[...(q.a||[]),...(q.b&&q.b!==q.a?q.b:[]),...(q.pts?q.pts.flat():[])])'
with sync_playwright() as p:
    b=p.chromium.launch();errs=[]
    for ch,steps in [('robot',[('mode','walk',1200),('mode','run6',1500),('turn','U',1800),('mode','walk',1500),('js','startFlip("up")',2200),('js','startFlip("down")',2200)]),
                     ('sergal',[('mode','walk',1200),('turn','L',1500),('mode','idle',1200),('js','setCycle(2)',1500),('mode','run',1500)])]:
        pg=b.new_page(viewport={'width':1200,'height':800});pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(500)
        pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").dispatchEvent(new Event("change"));$("charSel").onchange();window.POSES=[];const orig=hRecord;window.hRecord=function(dt){{const n=HIST.length,last=HIST[n-1];orig(dt);if(HIST.length!==n||HIST[HIST.length-1]!==last)POSES[HIST.length-1]=({KEY})()}};if(!playing)$("play").onclick()}}')
        for kind,arg,wait in steps:
            if kind=='mode':pg.evaluate(f'()=>{{$("modeSel").value="{arg}";$("modeSel").onchange()}}')
            elif kind=='turn':pg.evaluate(f'()=>startTurn("{arg}")')
            else:pg.evaluate(f'()=>{{{arg}}}')
            pg.wait_for_timeout(wait)
        pg.evaluate('()=>{if(playing)$("play").onclick()}');pg.wait_for_timeout(100)
        n=pg.evaluate('HIST.length');bad=[]
        for i in range(0,n-1,max(1,n//40)):
            pg.evaluate(f'()=>{{const s=$("scrub");s.value={i}/(HIST.length-1);s.dispatchEvent(new Event("input",{{bubbles:true}}))}}');pg.wait_for_timeout(30)
            w=pg.evaluate(f'(()=>{{const a=({KEY})(),b=POSES[{i}];if(!b)return -1;if(a.length!==b.length)return 999;let w=0;a.forEach((r,k)=>r.forEach((v,j)=>{{w=Math.max(w,Math.abs(v-b[k][j]))}}));return w}})()')
            if w>0.05:bad.append((i,round(w,3)))
        print(ch,'frames recorded',n,'| rewound poses that differ:',len(bad),bad[:8])
        # step back 5, forward 5 returns to the same frame; play from rewound reaches live
        pg.evaluate('()=>{const s=$("scrub");s.value=0.5;s.dispatchEvent(new Event("input",{bubbles:true}))}');h0=pg.evaluate('HPOS')
        pg.evaluate('()=>{for(let i=0;i<5;i++)hStep(-1);for(let i=0;i<5;i++)hStep(1)}');h1=pg.evaluate('HPOS')
        print('  step back 5 then forward 5: from',h0,'to',h1)
        pg.evaluate('()=>$("play").onclick()');pg.wait_for_timeout(int(1000*n/8)+2000);print('  play from the middle reaches now:',pg.evaluate('HPOS===-1'),'| label',pg.evaluate('$("scrubV").textContent'))
        # branching: rewind, change animation -> history cut there
        pg.evaluate('()=>{if(playing)$("play").onclick();const s=$("scrub");s.value=0.3;s.dispatchEvent(new Event("input",{bubbles:true}))}');k=pg.evaluate('HPOS')
        pg.locator('#modeSel').select_option(index=0);pg.wait_for_timeout(200)
        print('  branch at',k,'-> history length',pg.evaluate('HIST.length'),'live:',pg.evaluate('HPOS===-1'))
        pg.close()
    print('errors',errs);b.close()
