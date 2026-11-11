const {open}=require('./lib');
(async()=>{const {b,pg,errs}=await open(require('path').resolve(process.env.MIXMO||'Mixmo.html'),{w:430,h:900});
 await pg.waitForFunction(()=>R3.ok,null,{timeout:60000});await pg.waitForTimeout(1500);
 const r={};
 r.hiddenForOC=await pg.evaluate(()=>$("presetBox").hidden);
 await pg.selectOption('#charSel','sergal2');
 r.shownFor2=await pg.evaluate(()=>!$("presetBox").hidden);
 await pg.click('#presetSeg [data-p=fox]');await pg.waitForTimeout(300);
 r.after=await pg.evaluate(()=>({PRESET2,on:[...document.querySelectorAll('#presetSeg button.on')].map(b=>b.dataset.p),note:$("presetNote").textContent.slice(0,60),stored:localStorage.getItem("mixmoPreset2"),thigh:P.idle.thigh,run:P.run.speed+"/"+P.run.travel}));
 await pg.locator('#presetBox').screenshot({path:'ui/panel.png'});
 // save text includes preset; load it back from sergal preset
 r.save=await pg.evaluate(()=>{syncJSON();const o=JSON.parse($("json").value);setPreset2("sergal");const msg=applyCharacterFile(o);return{preset:o.preset,msg,now:PRESET2,thigh:P.idle.thigh}});
 // reload keeps it
 await pg.reload();await pg.waitForTimeout(800);await pg.selectOption('#charSel','sergal2');
 r.reload=await pg.evaluate(()=>PRESET2);
 // look at him: side, walking
 await pg.evaluate(()=>{const s=$("modeSel");s.value="walk";s.onchange();yaw=Math.PI/2;pitch=0.12});await pg.waitForTimeout(1500);
 await pg.locator('#view').screenshot({path:'ui/fox_walk.png'});
 await pg.evaluate(()=>{const s=$("modeSel");s.value="run";s.onchange()});await pg.waitForTimeout(1500);
 await pg.locator('#view').screenshot({path:'ui/fox_run.png'});
 // 2D renderer
 await pg.evaluate(()=>document.querySelector('#rendSw [data-r]:not([data-r="three"])').click());await pg.waitForTimeout(800);
 await pg.locator('#view').screenshot({path:'ui/fox_run_2d.png'});
 // game: hold W
 await pg.evaluate(()=>{const t=document.querySelector('#tierSw [data-t="game"]')||[...document.querySelectorAll('#tierSw button')][0];t.click()});
 await pg.keyboard.down('KeyW');await pg.waitForTimeout(1500);r.game=await pg.evaluate(()=>({mode,PRESET2,travel:+cur.travel.toFixed(0)}));await pg.keyboard.up('KeyW');
 console.log(JSON.stringify(r,null,1));console.log(errs);await b.close()})();
