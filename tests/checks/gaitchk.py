import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':850})
    pg.goto('http://localhost:8765/'+F);pg.wait_for_timeout(800)
    pg.evaluate('()=>document.querySelector(\'#tierSw [data-t="dev"]\').click()');pg.wait_for_timeout(500)
    for ch in ['sergal2','robot','sergal']:
        pg.evaluate(f'()=>{{$("charSel").value="{ch}";$("charSel").dispatchEvent(new Event("change"))}}');pg.wait_for_timeout(700)
        print(F,ch,'main chart key has char:',pg.evaluate(f'(()=>{{const g=$("gait");return (g._key||"").startsWith("{ch}|")}})()'),
              '| mini on live canvas:',pg.evaluate(f'(()=>{{const g=document.querySelector(".gaitMini");return (g._key||"").startsWith("{ch}|")}})()'))
    b.close()
