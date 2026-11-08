from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':850});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://cdn.jsdelivr.net/**',lambda r:r.abort())
    pg.goto('file:///home/claude/Mixmo.html');pg.wait_for_timeout(1000)
    pg.evaluate('()=>{document.querySelector(\'#rendSw [data-r="canvas"]\').click();document.querySelector(\'#tierSw [data-t="game"]\').click()}');pg.wait_for_timeout(300)
    print('Game on:',pg.evaluate('document.documentElement.classList.contains("game")'),'| animation menu hidden',pg.evaluate('!$("modeSel").offsetParent'),'| turn buttons hidden',pg.evaluate('!$("tL").offsetParent'),'| tip shown',pg.evaluate('!!$("gameTip").offsetParent'))
    pg.mouse.click(600,300)   # focus the page (not a control)
    def hold(keys,ms):
        for k in keys:pg.keyboard.down(k)
        pg.wait_for_timeout(ms)
        r=pg.evaluate('()=>({mode,head:HEAD,pos:[...POS]})')
        for k in reversed(keys):pg.keyboard.up(k)
        return r
    for ch in ['sergal','robot']:
        pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").onchange();yaw=0.7}}');pg.wait_for_timeout(600)
        pg.evaluate('''()=>{window.SL={worst:0,prev:null};const f=window.render;window.render=function(){if(CHAR==="robot"&&typeof ROBFEET!=="undefined"){const sh=ROBFEET.map(f=>({g:f.w>0.5&&f.p[1]<3.25,x:f.p[0]+POS[0],z:f.p[2]+POS[1]}));
          if(SL.prev&&SL.prev.length===sh.length)sh.forEach((s,k)=>{const q=SL.prev[k];if(s.g&&q.g)SL.worst=Math.max(SL.worst,Math.hypot(s.x-q.x,s.z-q.z))});SL.prev=sh}return f.apply(this,arguments)}}''')
        for keys,label in [(['w'],'W'),(['d'],'D'),(['s'],'S'),(['a'],'A'),(['Shift','w'],'Shift+W'),(['ArrowUp'],'Up arrow'),(['w','d'],'W+D')]:
            p0=pg.evaluate('[...POS]');r=hold(keys,1600)
            d=pg.evaluate('a=>{const v=rotY([a[0],0,a[1]],yaw);return [v[0],v[2]]}',[r["pos"][0]-p0[0],r["pos"][1]-p0[1]])
            sx,sz=d;dirn=('right' if sx>abs(sz)*0.5 else 'left' if sx<-abs(sz)*0.5 else '')+(' away' if sz<-abs(sx)*0.5 else ' towards' if sz>abs(sx)*0.5 else '')
            print(f'  {ch:6s} {label:8s}: mode {r["mode"]:5s}, moved on screen: {dirn.strip():14s} (right {sx:6.1f}, toward camera {sz:6.1f})')
        pg.wait_for_timeout(1200);print(f'  {ch} after letting go: mode {pg.evaluate("mode")}', '| worst planted-paw slide %.3f (limit 0.05)'%pg.evaluate('SL.worst') if ch=='robot' else '')
    print(errs);b.close()
