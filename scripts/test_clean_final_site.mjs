import {chromium} from 'playwright';
const assert=(condition,msg)=>{if(!condition)throw Error('Clean site test: '+msg)};
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
try{
 const page=await browser.newPage({viewport:{width:1440,height:900}});
 const base='http://127.0.0.1:8877/';
 const valid=['index.html','services.html','about.html','contact.html','package.html','lms.html','lms-auth.html','lms-course.html','lms-learn.html'];
 const removed=['course.html','courses.html','dashboard.html','enrollment.html','login.html','programs.html','communication-course.html'];
 for(const name of valid){
   const r=await page.goto(base+name,{waitUntil:'domcontentloaded'});
   assert(r.status()===200,name+' must exist');
 }
 for(const name of removed){
   const r=await page.goto(base+name,{waitUntil:'domcontentloaded'});
   assert(r.status()===404,name+' must be gone');
 }
 await page.goto(base+'lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
 assert(!await page.locator('footer').count(),'no footer in classroom');
 assert(await page.locator('#qa-skip-video').isVisible(),'test button preserved');
 await page.click('#qa-skip-video');
 await page.waitForFunction(()=>document.querySelector('#day-number')?.textContent.includes('DAY 02 / 21'));
 const path=await page.evaluate(()=>document.querySelector('#lesson-media').getAttribute('src'));
 console.log('DAY 2 VIDEO SOURCE',path);
 assert(path==='assets/lms/videos/day-02.mp4','Day 2 local MP4 path correct');
 await page.waitForFunction(()=>{
   const v=document.querySelector('#lesson-media');return v.readyState>=1 || Boolean(v.error)
 },{timeout:25000});
 const loaded=await page.evaluate(()=>{
   const v=document.querySelector('#lesson-media');
   return {size:[v.videoWidth,v.videoHeight],duration:v.duration,error:v.error?.code||null,
    source:v.currentSrc,readyState:v.readyState,missing:!document.querySelector('#video-missing').hidden};
 });
 console.log('DAY 2 LOADED',JSON.stringify(loaded));
 assert(!loaded.error&&!loaded.missing&&loaded.duration>20,'Day 2 MP4 must decode correctly');
 assert(loaded.size[0]>0&&loaded.size[1]>0,'Day 2 valid dimensions');
 await page.click('#open-worksheet');
 assert((await page.locator('#worksheet-frame').getAttribute('src')).includes('day-02.pdf'),'Day 2 worksheet local');
 await page.click('#close-worksheet');
 await page.click('#full-screen');
 await page.waitForFunction(()=>document.fullscreenElement?.id==='video-stage');
 assert(await page.locator('#full-screen').getAttribute('aria-label')==='Exit full screen','exit button inside fullscreen');
 await page.click('#full-screen');
 await page.waitForFunction(()=>!document.fullscreenElement);
 console.log('PASS: 9 pages retained, 7 old pages removed, Day2 playable, PDF local, fullscreen exit');
}finally{await browser.close()}
