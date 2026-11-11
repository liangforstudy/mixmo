const {open}=require('./lib');
(async()=>{const {b,pg,errs}=await open(require('path').resolve(process.env.MIXMO||'Mixmo.html'),{w:430,h:900});
 await pg.waitForTimeout(800);const r={};
 const ph=()=>pg.evaluate(()=>({phase:+phase.toFixed(3),HPOS,playing}));
 // speed: phase advance over 1 s at each rate
 for(const rt of ["1","0.5","0.25"]){await pg.click(`#rateSeg [data-r="${rt}"]`);const a=(await ph()).phase;await pg.waitForTimeout(1000);r["rate "+rt]=+((await ph()).phase-a).toFixed(2)}
 await pg.click('#rateSeg [data-r="1"]');
 // tap prev: pauses, steps once
 await pg.click('#prevF');r.tap=await ph();
 // hold prev 1.2 s
 const box=await pg.locator('#prevF').boundingBox();await pg.mouse.move(box.x+box.width/2,box.y+box.height/2);
 const h0=await ph();await pg.mouse.down();await pg.waitForTimeout(1200);await pg.mouse.up();await pg.waitForTimeout(200);const h1=await ph();
 r.holdBack={from:h0.HPOS,to:h1.HPOS};
 // hold next 0.6 s
 const nb=await pg.locator('#nextF').boundingBox();await pg.mouse.move(nb.x+nb.width/2,nb.y+nb.height/2);
 await pg.mouse.down();await pg.waitForTimeout(700);await pg.mouse.up();await pg.waitForTimeout(200);r.holdFwd=(await ph()).HPOS;
 // rewound + change speed keeps history position
 const before=(await ph()).HPOS;await pg.click('#rateSeg [data-r="0.5"]');r.rateWhileRewound={before,after:(await ph()).HPOS};
 await pg.locator('#status').screenshot({path:'status.png'});
 console.log(JSON.stringify(r));console.log(errs);await b.close()})();
