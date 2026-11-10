import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for F in sys.argv[1:]:
        ctx=b.new_context(**p.devices['iPhone 13']);pg=ctx.new_page()
        pg.goto('http://localhost:8765/'+F);pg.wait_for_timeout(2500)
        pg.tap('#play');pg.wait_for_timeout(300)
        n0=pg.evaluate('HIST.length');pg.tap('#prevF');pg.wait_for_timeout(250);n1=pg.evaluate('HIST.length');h1=pg.evaluate('HPOS')
        pg.tap('#prevF');pg.wait_for_timeout(250);n2=pg.evaluate('HIST.length');pg.tap('#nextF');pg.wait_for_timeout(250);n3=pg.evaluate('HIST.length')
        print(F,'hist',n0,n1,n2,n3,'HPOS after first back',h1,'now',pg.evaluate('HPOS'),'branches',pg.evaluate('typeof HBR!=="undefined"?HBR:"-"'))
        ctx.close()
    b.close()
