const {open}=require('./lib');
(async()=>{const file=process.argv[2],tag=process.argv[3];const {b,pg,errs}=await open(file,{w:600,h:900});
 await pg.waitForTimeout(800);
 await pg.evaluate(()=>document.querySelector('#rendSw [data-r]:not([data-r="three"])').click());await pg.waitForTimeout(300);
 await pg.selectOption('#charSel','robot');await pg.evaluate(()=>{const s=$("modeSel");s.value="walk";s.onchange()});await pg.waitForTimeout(1500);
 await pg.evaluate(()=>{window.requestAnimationFrame=()=>0;yaw=Math.PI/2;pitch=0.08});
 await pg.click('#tF');const want=new Set(process.argv[4]?process.argv[4].split(',').map(Number):[10,14,18,22,26,31]);const got=new Set();
 for(let i=0;i<220&&got.size<want.size;i++){const st=await pg.evaluate(()=>{frame(last+16.67);render();return $("stText").textContent});
  const m=st.match(/Rise onto front end, frame (\d+)\/53/);if(m&&want.has(+m[1])&&!got.has(+m[1])){got.add(+m[1]);await pg.locator('#cv').screenshot({path:`over/${tag}_r${m[1]}.png`})}}
 console.log(errs);await b.close()})();
