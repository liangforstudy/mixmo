const {open}=require('./lib');
(async()=>{const res=[];for(const w of [40,55,70,85,100,115,130,145]){const {b,pg}=await open(process.argv[2],{w:600,h:900,stopLoop:true});
 await pg.selectOption('#charSel','robot');
 await pg.evaluate(w=>{let t=last;for(let i=0;i<w;i++){t+=16.67;frame(t)}},w);await pg.click('#tF');
 const r=await pg.evaluate(()=>{let lo=1e9,nm='';for(let i=0;i<40;i++){frame(last+16.67);for(const q of prims){if(q.t===2)continue;for(const v of (q.pts||[q.a]))if(v[1]<lo){lo=v[1];nm=q.nm}}}return lo.toFixed(1)+' '+nm});
 res.push(w+':'+r);await b.close()}console.log(res.join(' | '))})();
