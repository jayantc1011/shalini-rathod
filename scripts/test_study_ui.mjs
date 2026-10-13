import {chromium} from 'playwright';
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const expect=(condition,message)=>{if(!condition)throw Error('UI smoke test failed: '+message);};
try{
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
  const initial=await page.evaluate(()=>{
    const stage=document.querySelector('.learn-video').getBoundingClientRect();
    const action=document.querySelector('#complete-and-next').getBoundingClientRect();
    const video=document.querySelector('#lesson-media');
    return {stageRatio:stage.width/stage.height,stageWidth:stage.width,stageHeight:stage.height,
      actionY:action.y,actionBottom:action.bottom,locked:document.querySelectorAll('.learn-day-btn:disabled').length,
      btnDisabled:document.querySelector('#complete-and-next').disabled,
      videoControls:video.controls,playbackRate:video.playbackRate,
      speedControls:document.querySelectorAll('select').length,
      oldUIElements:document.querySelectorAll('.sr-study,.sr-lesson-details,.sr-resources-section,.sr-player-actions').length};
  });
  console.log('Desktop geometry',JSON.stringify(initial));
  expect(Math.abs(initial.stageRatio-9/16)<.005,'video must be precisely 9:16');
  expect(initial.stageWidth<=310&&initial.stageWidth>200,'video must be compact');
  expect(initial.actionBottom<=900,'desktop completion action must be in first viewport');
  expect(initial.locked===20,'20 future days locked at start');
  expect(initial.btnDisabled,'completion locked before video ends');
  expect(!initial.videoControls && initial.speedControls===0,'no seek UI or speed control');
  expect(initial.oldUIElements===0,'legacy learner UI removed');
  await page.click('#open-worksheet');
  expect(await page.locator('#worksheet-dialog').evaluate(el=>el.open),'PDF should open inside modal');
  const src=await page.locator('#worksheet-frame').getAttribute('src');
  expect(src.startsWith('assets/lms/pdfs/day-01.pdf'),'PDF local to site');
  await page.click('#close-worksheet');
  expect(!(await page.locator('#worksheet-dialog').evaluate(el=>el.open)),'PDF should close');
  await page.waitForFunction(()=>document.querySelector('#lesson-media').readyState>=1,{timeout:25000});
  await page.evaluate(()=>{const v=document.querySelector('#lesson-media');v.currentTime=v.duration-3;});
  await page.waitForTimeout(250);
  const seekTime=await page.locator('#lesson-media').evaluate(v=>v.currentTime);
  console.log('Seek guard:',seekTime);
  expect(seekTime<10,'skip-ahead must be blocked');
  await page.click('#large-play');
  await page.waitForTimeout(1900);
  await page.evaluate(()=>{
    const v=document.querySelector('#lesson-media');
    Object.defineProperty(v,'duration',{configurable:true,get:()=>1});
    v.dispatchEvent(new Event('timeupdate'));
    v.dispatchEvent(new Event('ended'));
  });
  expect(!(await page.locator('#complete-and-next').isDisabled()),'completion should unlock only after a full lesson');
  await page.click('#complete-and-next');
  const after=await page.evaluate(()=>({
    label:document.querySelector('#day-number').textContent,
    day3locked:document.querySelector('[data-day="2"]').disabled,
    day2unlocked:!document.querySelector('[data-day="1"]').disabled
  }));
  console.log('Completion flow',JSON.stringify(after));
  expect(after.label.includes('02 / 21'),'completion click opens Day 2');
  expect(after.day2unlocked&&after.day3locked,'sequential access is enforced');
  await page.setViewportSize({width:390,height:844});
  await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
  const mobile=await page.evaluate(()=>({
    rect:(()=>{const a=document.querySelector('#complete-and-next').getBoundingClientRect();return {top:a.top,bottom:a.bottom}})(),
    viewport:innerHeight,
    videoRatio:(()=>{const r=document.querySelector('.learn-video').getBoundingClientRect();return r.width/r.height})(),
    cols:getComputedStyle(document.querySelector('.learn-layout')).gridTemplateColumns
  }));
  console.log('Mobile geometry',JSON.stringify(mobile));
  expect(mobile.rect.bottom<=mobile.viewport&&mobile.rect.top>=0,'completion visible/sticky on mobile');
  expect(Math.abs(mobile.videoRatio-9/16)<.005,'mobile 9:16 video');
  console.log('PASSED: portrait-only player, in-page PDF, sequential completion, no speed/seek, mobile action');
}finally{await browser.close();}
