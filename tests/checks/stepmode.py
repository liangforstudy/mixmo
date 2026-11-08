from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for vib in [True,False]:
        pg=b.new_page(viewport={'width':1200,'height':900});pg.goto('http://localhost:8765/Mixmo.html');pg.wait_for_timeout(1200)
        if not vib:pg.evaluate('()=>{delete navigator.__proto__.vibrate}')
        pg.click('#play');pg.wait_for_timeout(300);pg.select_option('#modeSel','run');pg.wait_for_timeout(300)
        for i in range(3):pg.click('#nextF');pg.wait_for_timeout(120)
        for i in range(5):pg.click('#prevF');pg.wait_for_timeout(120)
        for i in range(5):pg.click('#nextF');pg.wait_for_timeout(120)
        print('iPhone-style tick' if not vib else 'Android-style buzz',': after 3 fwd, 5 back, 5 fwd -> mode',pg.evaluate('mode'),'| select shows',pg.input_value('#modeSel'))
        pg.close()
    b.close()
