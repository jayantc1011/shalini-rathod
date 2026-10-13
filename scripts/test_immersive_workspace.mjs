import {chromium} from 'playwright';
const assert=(condition,message)=>{if(!condition)throw Error('Immersive LMS: '+message)};
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
for(const viewport of [{width:1440,height:900},{width:1366,height:768},{width:1280,height:720},{width:1100,height:800}]){
 const page=await browser.newPage({viewport});
 await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
 let m=await page.evaluate(()=>{
  const get=id=>document.querySelector(id);
  const rect=id=>{let r=get(id).getBoundingClientRect();return{top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
  return {screen:innerHeight, document:document.documentElement.scrollHeight,body:document.body.scrollHeight,
    footer:document.querySelectorAll('footer').length,video:rect('.learn-video'),out:rect('.learn-outline'),
    btn:rect('#complete-and-next'),skip:rect('#qa-skip-video'),roadmap:{
      view:get('#outline-list').clientHeight,total:get('#outline-list').scrollHeight,
      before:get('#outline-list').scrollTop
    }};
 });
 console.log('Desktop',JSON.stringify({viewport,...m}));
 assert(!m.footer,'footer must be gone');
 assert(m.document<=m.screen+2,'document must not need vertical scrolling at '+viewport.width);
 assert(m.body<=m.screen+2,'body must not need scrolling at '+viewport.width);
 assert(m.out.bottom<=m.screen+1,'roadmap must fit screen');
 assert(m.skip.bottom<=m.screen+1,'test skip must be visible');
 assert(m.roadmap.total>m.roadmap.view+100,'only lesson list should scroll');
 assert(Math.abs(m.video.width/m.video.height-9/16)<.009,'player ratio is 9:16');
 await page.evaluate(()=>{document.querySelector('#outline-list').scrollTop=100000;});
 const end=await page.evaluate(()=>{
   const parent=document.querySelector('#outline-list'),last=document.querySelector('.learn-day-btn[data-day="20"]');
   const a=parent.getBoundingClientRect(),b=last.getBoundingClientRect();
   return {scrollTop:parent.scrollTop,lastTop:b.top,lastBottom:b.bottom,containerBottom:a.bottom,windowScroll:scrollY};
 });
 console.log('Scrollable end',JSON.stringify(end));
 assert(end.lastBottom<=end.containerBottom+3,'Day 21 must be visible after sidebar-only scrolling');
 assert(end.windowScroll===0,'window must not scroll with outline');
 await page.close();
}
const page=await browser.newPage({viewport:{width:1440,height:900}});
await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
for(let i=0;i<20;i++){
 await page.locator('#qa-skip-video').click();
 await page.waitForFunction(expected=>document.querySelector('#day-number')?.textContent?.includes('DAY '+String(expected).padStart(2,'0')+' / 21'),i+2);
}
const final=await page.evaluate(()=>({
day:document.querySelector('#day-number').textContent,
count:document.querySelector('#overall-count').textContent,
day21locked:document.querySelector('.learn-day-btn[data-day="20"]').disabled,
videos:document.querySelectorAll('video').length,
footer:document.querySelectorAll('footer').length,
scrollY:scrollY
}));
console.log('Skip-through',JSON.stringify(final));
assert(final.day.includes('21 / 21'),'skip control should test Day 21');
assert(!final.day21locked,'day21 unlocked');
assert(final.scrollY===0,'no outer scrolling when skipping');
await page.locator('#open-worksheet').click();
const pdf=await page.locator('#worksheet-frame').getAttribute('src');
assert(pdf.includes('day-21.pdf'),'day21 in-page PDF');
await page.locator('#close-worksheet').click();
await page.setViewportSize({width:390,height:844});
await page.reload({waitUntil:'domcontentloaded'});
const mobile=await page.evaluate(()=>({footer:document.querySelectorAll('footer').length,
 button:!!document.querySelector('#qa-skip-video'),width:document.documentElement.scrollWidth,screen:innerWidth}));
console.log('Mobile',JSON.stringify(mobile));
assert(mobile.width<=mobile.screen+2,'mobile page should not scroll horizontally');
assert(mobile.button&&!mobile.footer,'test mode and footer removal on mobile');
console.log('PASS immersive fixed page, 21 day scrolling, portrait video, QA skipping, local PDF');
await page.close();
}finally{await browser.close()}
