import {chromium} from 'playwright';
const assert=(ok,msg)=>{if(!ok)throw new Error('Fullscreen/player regression: '+msg)};
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
  for(const viewport of [
    {width:1440,height:900},{width:1366,height:768},
    {width:1280,height:720},{width:1100,height:800}
  ]){
    const page=await browser.newPage({viewport});
    await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
    const state=await page.evaluate(()=>{
      const r=sel=>{let x=document.querySelector(sel).getBoundingClientRect();return {x:x.x,y:x.y,width:x.width,height:x.height,bottom:x.bottom}};
      return {screen:innerHeight,page:document.documentElement.scrollHeight,
        hasFooter:!!document.querySelector('footer'),
        video:r('#video-stage'),sidebar:r('.learn-outline'),controls:r('.learn-video-bar'),
        nested:document.querySelector('#video-stage').contains(document.querySelector('.learn-video-bar')),
        htmlVideoControls:document.querySelector('video').controls,
        hasSkip:!!document.querySelector('#qa-skip-video')
      };
    });
    console.log('DESKTOP',JSON.stringify({viewport,...state}));
    assert(!state.hasFooter,'footer must remain removed');
    assert(state.page<=state.screen+3,'must still fit full viewport');
    assert(state.nested,'player controls must be children of video stage');
    assert(state.video.bottom<=state.screen+1,'video must fit');
    assert(Math.abs(state.video.width/state.video.height - 9/16)<0.01,'portrait ratio 9:16');
    assert(state.controls.bottom<=state.video.bottom+1 && state.controls.bottom>=state.video.bottom-15,'controls at bottom INSIDE video');
    assert(state.video.height>=state.sidebar.height-42,'video and sidebar heights should be similar');
    assert(!state.htmlVideoControls,'cannot skip video with native scrubber');
    assert(state.hasSkip,'temporary skip button must remain');
    if (viewport.width===1440){
      await page.waitForFunction(()=>document.querySelector('#lesson-media').readyState>=1,{timeout:30000});
      const before=await page.locator('#volume-toggle').getAttribute('aria-label');
      assert(before==='Mute video','mute label initial');
      await page.locator('#volume-toggle').click();
      assert(await page.locator('#volume-toggle').getAttribute('aria-label')==='Unmute video','mute works');
      await page.locator('#volume-toggle').click();
      assert(await page.locator('#volume-toggle').getAttribute('aria-label')==='Mute video','unmute works');
      await page.locator('#full-screen').click();
      await page.waitForFunction(()=>document.fullscreenElement?.id==='video-stage');
      const expanded=await page.evaluate(()=>({
        label:document.querySelector('#full-screen').getAttribute('aria-label'),
        full:document.fullscreenElement?.id,
        controls:document.querySelector('.learn-video-bar').getBoundingClientRect().bottom,
        screen:innerHeight
      }));
      console.log('FULLSCREEN',JSON.stringify(expanded));
      assert(expanded.full==='video-stage','stage enters fullscreen, not just video');
      assert(expanded.label==='Exit full screen','exit control visible');
      assert(Math.abs(expanded.controls-expanded.screen)<12,'fullscreen controls at bottom');
      await page.locator('#full-screen').click();
      await page.waitForFunction(()=>!document.fullscreenElement);
      assert(await page.locator('#full-screen').getAttribute('aria-label')==='Full screen','button exits fullscreen');
      await page.locator('#qa-skip-video').click();
      await page.waitForFunction(()=>document.querySelector('#day-number').textContent.includes('DAY 02 / 21'));
      await page.locator('#open-worksheet').click();
      assert((await page.locator('#worksheet-frame').getAttribute('src')).includes('day-02.pdf'),'day2 PDF works');
      await page.locator('#close-worksheet').click();
    }
    await page.close();
  }
  const page=await browser.newPage({viewport:{width:390,height:844}});
  await page.goto('http://127.0.0.1:8877/lms-learn.html?course=speakathon&lesson=1',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.querySelectorAll('.learn-day-btn').length===21);
  const m=await page.evaluate(()=>({width:document.documentElement.scrollWidth,screen:innerWidth,
    stageWidth:document.querySelector('#video-stage').clientWidth,
    nested:document.querySelector('#video-stage').contains(document.querySelector('.learn-video-bar')),
    controls:document.querySelector('.learn-video-bar').getBoundingClientRect().bottom,
    stage:document.querySelector('#video-stage').getBoundingClientRect().bottom,
    missingDay12:!Array.from(document.querySelectorAll('source')).some(x=>x.src.includes('day-12'))
  }));
  console.log('MOBILE',JSON.stringify(m));
  assert(m.width<=m.screen+2,'no horizontal scroll');
  assert(m.nested,'mobile player controls inside');
  assert(m.controls<=m.stage+2,'mobile controls inside frame');
  console.log('PASS inline fullscreen controls, 9:16 taller player, mute, day2 PDF, retained test skip');
  await page.close();
}finally{await browser.close()}
