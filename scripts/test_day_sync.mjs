import {chromium} from 'playwright';
const assert=(ok,msg)=>{if(!ok)throw Error('Day-sync regression: '+msg)};
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:1440,height:900}});
 await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
 for(let i=1;i<=21;i++){
  const day=String(i).padStart(2,'0');
  await page.waitForFunction(day=>document.querySelector('#day-number')?.textContent?.includes('DAY '+day+' / 21'),day);
  const state=await page.evaluate(()=>{
   const video=document.querySelector('#lesson-media');
   const title=document.querySelector('#lesson-title').textContent;
   const practice=document.querySelector('#lesson-practice').textContent;
   const number=document.querySelector('#day-number').textContent;
   return {
     lessonDay:document.querySelector('#video-stage').dataset.lessonDay,
     heading:document.querySelector('#challenge-day').textContent,
     worksheet:document.querySelector('#worksheet-link-label').textContent,
     source:video.getAttribute('src'),
     title,practice,number,
     footer:!!document.querySelector('footer'),
     documentHeight:document.documentElement.scrollHeight,
     height:innerHeight
   };
  });
  console.log('DAY SYNC',JSON.stringify({day:i,...state}));
  assert(state.lessonDay===day,'stage day '+day);
  assert(state.heading===day,'challenge day '+day);
  assert(state.worksheet==='View Day '+day+' worksheet','worksheet label '+day);
  assert(state.source==='assets/lms/videos/day-'+day+'.mp4','MP4 source '+day);
  assert(!state.footer,'no footer');
  assert(state.documentHeight<=state.height+2,'page scroll');
  await page.locator('#open-worksheet').click();
  const pdf=await page.locator('#worksheet-frame').getAttribute('src');
  assert(pdf.startsWith('assets/lms/pdfs/day-'+day+'.pdf'),'PDF source '+day);
  await page.locator('#close-worksheet').click();
  if(i<21)await page.locator('#qa-skip-video').click();
 }
 await page.reload({waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
 assert(await page.locator('#challenge-day').textContent()==='21','refresh should keep selected day 21');
 await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.querySelector('#challenge-day')?.textContent==='01');
 const before=await page.locator('#lesson-practice').textContent();
 assert(before.includes('Read the provided passage'),'Day 1 matches original PDF');
 await page.locator('#qa-skip-video').click();
 await page.waitForFunction(()=>document.querySelector('#challenge-day').textContent==='02');
 const second=await page.locator('#lesson-practice').textContent();
 assert(second.includes('unscripted talk'),'Day 2 matches original PDF');
 await page.close();
 console.log('PASS all 21 sequential day labels, video src, challenge copy, PDFs, reload and viewport');
}finally{await browser.close()}
