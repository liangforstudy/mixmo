const {open}=require('./lib');
(async()=>{const {b,pg,errs}=await open(require('path').resolve(process.env.MIXMO||'Mixmo.html'),{w:430,h:900});
 await pg.waitForTimeout(1500);await pg.evaluate(()=>document.querySelector('#rendSw [data-r]:not([data-r="three"])').click());await pg.waitForTimeout(1500);
 await pg.evaluate(()=>{window.LOG=[];const o=hStep;hStep=d=>{LOG.push(["step",d,HPOS]);return o(d)};for(const ev of ["pointerdown","pointerup","pointerleave","pointercancel","click"])$("prevF").addEventListener(ev,()=>LOG.push([ev,HPOS]),true)});
 const box=await pg.locator('#prevF').boundingBox();await pg.mouse.move(box.x+box.width/2,box.y+box.height/2);
 await pg.mouse.down();await pg.waitForTimeout(1200);await pg.mouse.up();await pg.waitForTimeout(200);
 console.log(JSON.stringify(await pg.evaluate(()=>LOG)));console.log(errs);await b.close()})();
