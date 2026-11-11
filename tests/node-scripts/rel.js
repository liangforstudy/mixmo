const {open}=require('./lib');
(async()=>{for(const out of [0])for(const wait of [150,170,190]){const {b,pg}=await open(require('path').resolve(process.env.MIXMO||'Mixmo.html'),{w:600,h:900});
 await pg.waitForTimeout(800);await pg.evaluate(()=>document.querySelector('#rendSw [data-r]:not([data-r="three"])').click());
 await pg.selectOption('#charSel','robot');
 {
  await pg.evaluate(w=>{window.requestAnimationFrame=()=>0;window.WAIT=w},wait);
  await pg.evaluate(o=>{const s=$("modeSel");s.value="walk";s.onchange();let t=last;for(let i=0;i<window.WAIT;i++){t+=16.67;frame(t)}},out);
  await pg.click('#tF');
  const r=await pg.evaluate(()=>{const prev={};let worst=0,sinks=0,after=0,cnt=0;
   for(let i=0;i<320;i++){frame(last+16.67);const st=$("stText").textContent,m=st.match(/Rise onto front end, frame (\d+)\/53/),f=m?+m[1]:0;
    const inRise=f>=30,afterRise=!FLIP&&cnt>0;if(m)cnt++;if(!inRise&&!afterRise)continue;if(afterRise&&++after>40)break;
    const by={};for(const q of prims){if(q.t!==5||q.col!==RLOOK.pawB)continue;(by[q.nm]=by[q.nm]||[]).push(...q.pts)}
    for(const [n,pts] of Object.entries(by)){const lo=Math.min(...pts.map(v=>v[1])),c=pts.reduce((a,v)=>[a[0]+v[0]/pts.length,a[1]+v[2]/pts.length],[0,0]),w=[c[0],c[1]+groundOff];
     sinks=Math.min(sinks,lo);if(prev[n]&&lo<4&&prev[n].lo<4)worst=Math.max(worst,Math.hypot(w[0]-prev[n].w[0],w[1]-prev[n].w[1]));prev[n]={w,lo}}}
   return{worst:+worst.toFixed(2),sink:+sinks.toFixed(1)}});
  console.log('release',out*100+'%','start',wait,'-> worst planted red-paw slip/frame (rise 30-53 + 40 frames after):',r.worst,' deepest sink:',r.sink);
  }
 await b.close()}})();
