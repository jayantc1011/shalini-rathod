#!/usr/bin/env python3
"""Replace only Shalini's learner page with a clean, focused on-site course workspace."""
from pathlib import Path
import re,sys
root=Path(sys.argv[1]).resolve()
html_path=root/"lms-learn.html"
base=html_path.read_text(encoding="utf-8")
header=re.search(r"<header\b[^>]*>.*?</header>",base,re.S|re.I)
footer=re.search(r"<footer\b[^>]*>.*?</footer>",base,re.S|re.I)
assert header and footer, "Shared header/footer must remain intact"
# The earlier rebuild appended all its styles after this unique marker.
css_path=root/"style.css"
css=css_path.read_text(encoding="utf-8")
marker="/* ==============================================================\n   SPEAKATHON STUDY SPACE"
start=css.find(marker)
assert start>=0, "Expected previous LMS styling marker"
css_path.write_text(css[:start].rstrip()+"\n",encoding="utf-8")
legacy_js=root/"lms-player.js"
if legacy_js.exists(): legacy_js.unlink()
html=r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Your 21-Day Speakathon learning space: watch, practise, and complete each challenge.">
  <title>Speakathon Learning | Shalini Rathod</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="academy-learn.css">
</head>
<body class="academy-page lms-shell fresh-learn" data-lms-page="academy-player">
__HEADER__
<main class="learn" id="main-content">
  <div class="learn-container">
    <div class="learn-top">
      <a href="lms.html" class="learn-back" aria-label="Back to courses"><span aria-hidden="true">←</span> All courses</a>
      <div class="learn-course-brand"><span class="learn-course-mark" aria-hidden="true">S</span><span>21-Day Speakathon</span></div>
      <div class="learn-overall">
        <span id="overall-count">0 of 21 complete</span>
        <div class="learn-overall-track" role="progressbar" id="overall-meter" aria-label="Course completion" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span id="overall-fill"></span></div>
      </div>
    </div>

    <div class="learn-layout">
      <section class="learn-video-column" aria-label="Video lesson">
        <div class="learn-video" id="video-stage">
          <video id="lesson-media" playsinline preload="metadata" disablepictureinpicture controlslist="nodownload noplaybackrate noremoteplayback" aria-label="Current Speakathon lesson video"></video>
          <button id="large-play" class="learn-big-play" type="button" aria-label="Play video"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 4.6a1 1 0 0 1 1.52-.85l10 7.4a1 1 0 0 1 0 1.7l-10 7.4A1 1 0 0 1 8 19.4Z"/></svg></button>
          <div id="video-missing" class="learn-media-missing" hidden><span aria-hidden="true">▶</span><strong>Video not uploaded</strong><p>This day's recording is not on the website yet.</p></div>
        </div>
        <div class="learn-video-bar">
          <button id="toggle-play" type="button" class="learn-icon-button" aria-label="Play video" title="Play or pause">
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path id="play-icon" d="M8 4.6a1 1 0 0 1 1.52-.85l10 7.4a1 1 0 0 1 0 1.7l-10 7.4A1 1 0 0 1 8 19.4Z"/></svg>
          </button>
          <div class="learn-duration"><span id="elapsed">0:00</span><span class="learn-duration-divider">/</span><span id="duration">0:00</span></div>
          <div class="learn-playback-progress" role="progressbar" id="watch-meter" aria-label="Lesson playback progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span id="watch-fill"></span></div>
          <button id="full-screen" class="learn-icon-button" type="button" aria-label="Full screen" title="Full screen"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 3H3v5M16 3h5v5M21 16v5h-5M3 16v5h5"/></svg></button>
        </div>
      </section>

      <section class="learn-lesson" aria-label="Current challenge">
        <div class="learn-lesson-top"><span id="day-number" class="learn-eyebrow">DAY 01 / 21</span><span id="week-tag" class="learn-week-tag">WEEK 1</span></div>
        <h1 id="lesson-title">Get comfortable speaking on camera</h1>
        <p id="lesson-summary" class="learn-summary">Build confidence through short daily practice.</p>
        <div class="learn-practice">
          <h2><span class="learn-practice-icon" aria-hidden="true">✦</span> Today's challenge</h2>
          <p id="lesson-practice"></p>
        </div>
        <button id="open-worksheet" class="learn-pdf-link" type="button">
          <span class="learn-pdf-icon" aria-hidden="true">▤</span><span>View daily worksheet</span><span class="learn-pdf-arrow" aria-hidden="true">↗</span>
        </button>
        <button id="watch-example" class="learn-pdf-link" type="button" hidden>
          <span class="learn-pdf-icon" aria-hidden="true">▶</span><span>Watch example video</span><span class="learn-pdf-arrow" aria-hidden="true">↗</span>
        </button>
        <div class="learn-complete" aria-live="polite">
          <span id="completion-note" class="learn-completion-note">Watch the full video to continue.</span>
          <button id="complete-and-next" class="learn-complete-btn" type="button" disabled><span id="complete-label">Finish video to continue</span><span aria-hidden="true">→</span></button>
        </div>
        <div class="learn-next-link">
          <button id="previous-day" type="button" aria-label="Go to previous lesson">← Previous day</button>
          <span id="next-hint">Up next: Day 2</span>
        </div>
      </section>

      <aside class="learn-outline" aria-label="21-day course outline">
        <div class="learn-outline-header"><div><span class="learn-eyebrow">YOUR LEARNING PATH</span><h2>21 days to confidence.</h2></div><button id="outline-toggle" class="learn-outline-toggle" type="button" aria-expanded="false" aria-controls="outline-list">Lessons <span aria-hidden="true">⌄</span></button></div>
        <nav class="learn-outline-list" id="outline-list" aria-label="Course lessons"></nav>
      </aside>
    </div>
  </div>
</main>
<dialog id="worksheet-dialog" class="learn-pdf-dialog" aria-labelledby="worksheet-title">
  <div class="learn-dialog-head"><div><span class="learn-eyebrow" id="worksheet-tag">WORKSHEET · DAY 01</span><h2 id="worksheet-title">Practice worksheet</h2></div><button type="button" id="close-worksheet" aria-label="Close PDF viewer">×</button></div>
  <iframe id="worksheet-frame" title="Day challenge PDF" loading="lazy"></iframe>
  <div id="worksheet-error" class="learn-pdf-error" hidden>This PDF isn't available on the website yet.</div>
</dialog>
__FOOTER__
<script src="courses-data.js"></script>
<script src="academy-learn.js"></script>
<script src="script.js"></script>
</body>
</html>
'''
html_path.write_text(html.replace("__HEADER__",header.group()).replace("__FOOTER__",footer.group()),encoding="utf-8")
css_new=r'''/* Shalini Academy — focused learning player, October 2026.
   Fresh, page-scoped layout. Shared header, footer, global pages remain untouched. */
.fresh-learn{--learn-ink:#233b30;--learn-muted:#7a8479;--learn-accent:#bfeb69;--learn-border:#e6ebe3;background:#f8f9f5;color:var(--learn-ink)}
.fresh-learn .learn,.fresh-learn .learn *{box-sizing:border-box}
.fresh-learn .learn{font-family:"DM Sans",system-ui,-apple-system,sans-serif;min-height:75vh;padding:0 0 65px;background:#f8f9f5}
.fresh-learn .learn [hidden],.fresh-learn .learn-pdf-dialog [hidden]{display:none!important}
.fresh-learn .learn-container{width:min(1460px,calc(100% - 80px));margin:auto}
.fresh-learn .learn-top{min-height:76px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:22px;border-bottom:1px solid var(--learn-border)}
.fresh-learn .learn-back{font-size:12px;font-weight:700;color:#66816d;text-decoration:none;display:flex;align-items:center;gap:9px;width:max-content}
.fresh-learn .learn-back>span{font-size:19px}
.fresh-learn .learn-course-brand{font-size:13px;font-weight:800;letter-spacing:-.02em;display:flex;gap:10px;align-items:center;color:#284434}
.fresh-learn .learn-course-mark{width:29px;height:29px;border-radius:9px;background:#d9eeab;color:#294e2f;display:grid;place-items:center;font-size:17px;font-weight:800}
.fresh-learn .learn-overall{justify-self:end;width:177px;display:grid;gap:7px;color:#758473;font-size:11px;font-weight:700;text-align:right}
.fresh-learn .learn-overall-track{height:4px;background:#e4ebdb;border-radius:20px;overflow:hidden}
.fresh-learn .learn-overall-track>span{height:100%;display:block;width:0;background:#80ae5b;transition:width .2s}
.fresh-learn .learn-layout{display:grid;grid-template-columns:minmax(250px,340px) minmax(360px,1fr) minmax(260px,310px);align-items:start;gap:clamp(20px,2.8vw,44px);padding-top:33px}
.fresh-learn .learn-video-column{display:flex;flex-direction:column;align-items:center;width:100%;min-width:0}
.fresh-learn .learn-video{width:min(100%,306px);aspect-ratio:9/16;position:relative;background:#050605;overflow:hidden;border-radius:13px;isolation:isolate;display:grid;place-items:center;box-shadow:0 15px 36px #17271917}
.fresh-learn .learn-video video{display:block;position:absolute;inset:0;width:100%;height:100%;aspect-ratio:9/16;object-fit:contain;object-position:center;background:#050605}
.fresh-learn .learn-big-play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);display:grid;place-items:center;width:66px;height:66px;border:1px solid #ffffff73;border-radius:50%;background:#1319139e;color:#fff;cursor:pointer;backdrop-filter:blur(10px);transition:background .18s}
.fresh-learn .learn-big-play:hover{background:#2a3a2ace}
.fresh-learn .learn-big-play svg{width:23px;height:23px;margin-left:4px}
.fresh-learn .learn-media-missing{position:absolute;inset:0;padding:20px;background:#101810;color:#e6eee0;display:flex;gap:11px;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.fresh-learn .learn-media-missing>span{width:47px;height:47px;display:grid;place-items:center;border:1px solid #ffffff2c;border-radius:50%;margin-bottom:5px;font-size:17px}
.fresh-learn .learn-media-missing strong{font-size:15px}
.fresh-learn .learn-media-missing p{max-width:200px;color:#b3c0b3;font-size:12px;line-height:1.55;margin:0}
.fresh-learn .learn-video-bar{display:flex;align-items:center;gap:11px;width:min(100%,306px);padding:10px 2px 0}
.fresh-learn .learn-icon-button{border:0;background:transparent;color:#36503b;width:29px;height:28px;display:grid;place-items:center;cursor:pointer;padding:3px}
.fresh-learn .learn-icon-button svg{width:18px;height:18px}
.fresh-learn .learn-duration{display:flex;gap:4px;white-space:nowrap;color:#45584b;font-size:11px;font-weight:700;font-variant-numeric:tabular-nums}
.fresh-learn .learn-duration-divider{color:#9aa79c}
.fresh-learn .learn-playback-progress{height:4px;background:#e4e9dd;flex:1;border-radius:10px;overflow:hidden}
.fresh-learn .learn-playback-progress span{display:block;width:0;height:100%;background:#82b45b}
.fresh-learn .learn-lesson{padding:18px 0 0;min-width:0}
.fresh-learn .learn-lesson-top{display:flex;align-items:center;gap:13px}
.fresh-learn .learn-eyebrow{font-size:10px;letter-spacing:.12em;font-weight:800;color:#729765}
.fresh-learn .learn-week-tag{background:#ecf4df;border-radius:5px;font-size:10px;padding:5px 7px;color:#60804d;font-weight:800}
.fresh-learn .learn-lesson h1{font-size:clamp(30px,3.1vw,47px);line-height:1.09;letter-spacing:-.052em;font-weight:800;margin:15px 0 14px;color:#203a2d;max-width:500px}
.fresh-learn .learn-summary{font-size:14px;line-height:1.65;color:#7c897f;margin:0 0 30px;max-width:450px}
.fresh-learn .learn-practice{border-top:1px solid var(--learn-border);padding-top:21px}
.fresh-learn .learn-practice h2{font-size:13px;letter-spacing:-.01em;margin:0 0 10px;display:flex;align-items:center;gap:8px;color:#315341;font-weight:800}
.fresh-learn .learn-practice-icon{font-size:18px;color:#72a84d}
.fresh-learn .learn-practice p{font-size:14px;line-height:1.72;margin:0 0 19px;color:#5f7066}
.fresh-learn .learn-pdf-link{border:1px solid var(--learn-border);background:#fff;padding:13px 15px;border-radius:10px;color:#284b36;display:flex;align-items:center;gap:13px;width:100%;font-size:12px;font-weight:800;cursor:pointer;text-align:left;margin:9px 0}
.fresh-learn .learn-pdf-link:hover{border-color:#9fbd8d;background:#f7fbf3}
.fresh-learn .learn-pdf-icon{font-size:20px;color:#7e9c69}
.fresh-learn .learn-pdf-arrow{margin-left:auto;font-size:16px;color:#8a9c87}
.fresh-learn .learn-complete{padding:23px 0 0}
.fresh-learn .learn-completion-note{display:block;min-height:20px;font-size:12px;font-weight:700;color:#7a8b7a;margin-bottom:10px}
.fresh-learn .learn-completion-note.is-ready{color:#4b8653}
.fresh-learn .learn-complete-btn{width:100%;display:flex;align-items:center;justify-content:space-between;border:0;border-radius:10px;background:#254b35;color:white;padding:16px 19px;font-size:14px;font-weight:800;cursor:pointer;transition:background .2s}
.fresh-learn .learn-complete-btn>span:last-child{font-size:19px;font-weight:500}
.fresh-learn .learn-complete-btn:hover:enabled{background:#193e2b}
.fresh-learn .learn-complete-btn:disabled{background:#e2e9de;color:#92a28e;cursor:not-allowed}
.fresh-learn .learn-next-link{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:19px 0;font-size:11px;color:#9aa59a}
.fresh-learn .learn-next-link button{border:0;background:transparent;padding:3px 0;color:#668368;cursor:pointer;font-size:11px;font-weight:800}
.fresh-learn .learn-next-link button:disabled{opacity:.35;cursor:not-allowed}
.fresh-learn .learn-outline{border-left:1px solid var(--learn-border);padding:17px 0 0 25px}
.fresh-learn .learn-outline-header{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:0 0 18px}
.fresh-learn .learn-outline-header h2{font-size:19px;line-height:1.2;margin:8px 0 0;letter-spacing:-.045em;color:#254334}
.fresh-learn .learn-outline-toggle{display:none}
.fresh-learn .learn-outline-list{overflow-y:auto;max-height:calc(100vh - 205px);scrollbar-color:#cad7c3 transparent;scrollbar-width:thin}
.fresh-learn .learn-week-block{margin:0 0 20px}
.fresh-learn .learn-week-name{display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:10px;letter-spacing:.04em;text-transform:uppercase;color:#7d9976;padding:13px 0 10px;border-top:1px solid var(--learn-border)}
.fresh-learn .learn-week-name span:last-child{font-weight:700;color:#a5b09f}
.fresh-learn .learn-day-btn{border:0;background:transparent;width:100%;display:flex;text-align:left;align-items:center;gap:11px;padding:12px 9px;border-radius:8px;cursor:pointer;color:#758376;font-size:12px;line-height:1.5;transition:background .15s}
.fresh-learn .learn-day-btn:hover:enabled{background:#eef4e8}
.fresh-learn .learn-day-btn[aria-current="step"]{background:#e9f2dc;color:#2d5535;font-weight:800}
.fresh-learn .learn-day-btn:disabled{cursor:not-allowed;color:#aab2aa}
.fresh-learn .learn-day-bullet{width:27px;height:27px;display:grid;place-items:center;border-radius:8px;border:1px solid #dfe9d8;color:#95a48d;font-size:11px;flex:none;font-weight:800}
.fresh-learn .learn-day-btn.is-completed .learn-day-bullet{background:#d6eabd;color:#346d3a;border-color:#d6eabd}
.fresh-learn .learn-day-title{flex:1}
.fresh-learn .learn-day-lock{color:#b4bbb1;font-size:12px}
.fresh-learn .learn-pdf-dialog{padding:0;border:0;border-radius:16px;box-shadow:0 24px 80px #0c1b164f;width:min(980px,95vw);max-width:980px;max-height:94vh;background:#fff;overflow:hidden;font-family:"DM Sans",sans-serif}
.fresh-learn .learn-pdf-dialog::backdrop{background:#132319b8}
.fresh-learn .learn-dialog-head{display:flex;justify-content:space-between;align-items:center;padding:16px 22px;gap:10px;border-bottom:1px solid #e6e9e1}
.fresh-learn .learn-dialog-head h2{margin:4px 0 0;font-size:17px;letter-spacing:-.025em;color:#284235}
.fresh-learn #close-worksheet{width:35px;height:35px;border:0;border-radius:10px;background:#f2f5ed;color:#415b44;font-size:23px;cursor:pointer}
.fresh-learn #worksheet-frame{display:block;width:100%;height:min(80vh,880px);border:0;background:#f2f4ef}
.fresh-learn .learn-pdf-error{padding:38px 20px;text-align:center;color:#758678;font-size:13px}
.fresh-learn #video-stage:fullscreen{width:100vw;height:100vh;aspect-ratio:auto;border-radius:0;background:#000;display:grid;place-items:center}
.fresh-learn #video-stage:fullscreen video{position:relative;width:auto;height:100%;max-width:100vw;max-height:100vh;object-fit:contain}
.fresh-learn #video-stage:fullscreen .learn-big-play{z-index:4}
@media(max-width:1200px){.fresh-learn .learn-container{width:min(100% - 44px,1460px)}.fresh-learn .learn-layout{grid-template-columns:minmax(240px,310px) minmax(290px,1fr) 250px;gap:22px}.fresh-learn .learn-video{width:min(100%,285px)}.fresh-learn .learn-video-bar{width:min(100%,285px)}.fresh-learn .learn-outline{padding-left:15px}}
@media(max-width:1000px){.fresh-learn .learn-layout{grid-template-columns:minmax(230px,300px) minmax(320px,1fr)}.fresh-learn .learn-outline{grid-column:1/-1;position:static;border:0;border-top:1px solid var(--learn-border);padding:20px 0}.fresh-learn .learn-outline-list{max-height:360px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.fresh-learn .learn-week-block{margin:0}.fresh-learn .learn-video{width:min(100%,285px)}}
@media(max-width:690px){.fresh-learn .learn-container{width:calc(100% - 28px)}.fresh-learn .learn-top{min-height:62px;grid-template-columns:1fr auto;gap:6px}.fresh-learn .learn-course-brand{font-size:12px}.fresh-learn .learn-back{grid-column:1/-1;display:none}.fresh-learn .learn-overall{width:105px;font-size:10px}.fresh-learn .learn-layout{grid-template-columns:1fr;gap:12px;padding-top:20px}.fresh-learn .learn-video{width:min(100%,275px)}.fresh-learn .learn-video-bar{width:min(100%,275px)}.fresh-learn .learn-lesson{padding:18px 1px 0}.fresh-learn .learn-lesson h1{font-size:31px}.fresh-learn .learn-summary{margin-bottom:21px}.fresh-learn .learn-complete{position:sticky;bottom:0;background:#f8f9f5;padding:12px 0 16px;z-index:6;box-shadow:0 -12px 20px #f8f9f5e8}.fresh-learn .learn-outline-list{grid-template-columns:1fr;max-height:350px;display:none}.fresh-learn .learn-outline.is-open .learn-outline-list{display:block}.fresh-learn .learn-outline-toggle{display:inline-flex;gap:7px;align-items:center;background:#edf4e5;border:0;color:#40633d;border-radius:8px;font-size:12px;font-weight:800;padding:9px 11px;cursor:pointer}.fresh-learn .learn-outline{grid-column:auto;margin-top:10px}.fresh-learn #worksheet-frame{height:74vh}.fresh-learn .learn-dialog-head{padding:13px}.fresh-learn .learn-dialog-head h2{font-size:15px}}
@media(max-width:360px){.fresh-learn .learn-course-brand>span:last-child{font-size:11px}.fresh-learn .learn-video{width:min(100%,250px)}.fresh-learn .learn-video-bar{width:min(100%,250px)}}
'''
(root/"academy-learn.css").write_text(css_new,encoding="utf-8")
js=r'''(() => {
  'use strict';
  const data=window.SHALINI_COURSES||{};
  const params=new URLSearchParams(location.search);
  const slug=data[params.get('course')]?params.get('course'):'speakathon';
  const course=data[slug];if(!course)return;
  const $=id=>document.getElementById(id);
  const lessons=(course.modules||[]).flatMap((module,week)=>module.lessons.map((lesson)=>({...lesson,week,weekTitle:module.title})));
  const video=$('lesson-media'),stage=$('video-stage');
  const status=$('completion-note'),completeBtn=$('complete-and-next');
  const completed=new Set();
  const watched=new Set();
  let current=0,limit=0,mediaMode='lesson',isMissing=false;
  const storeKey='shalini-study-v3:'+slug;
  try{
    const saved=JSON.parse(localStorage.getItem(storeKey)||'{}');
    (saved.done||[]).filter(n=>Number.isInteger(n)&&n>=0&&n<lessons.length).forEach(n=>completed.add(n));
    (saved.watched||[]).filter(n=>Number.isInteger(n)&&n>=0&&n<lessons.length).forEach(n=>watched.add(n));
    if(Number.isInteger(saved.active))current=saved.active;
  }catch(_){}
  const unlocked=n=>n===0||Array.from({length:n},(_,i)=>i).every(i=>completed.has(i));
  const save=()=>{try{localStorage.setItem(storeKey,JSON.stringify({done:[...completed],watched:[...watched],active:current}));}catch(_){}};
  const time=n=>{if(!Number.isFinite(n))return '0:00';n=Math.max(0,Math.floor(n));return Math.floor(n/60)+':'+String(n%60).padStart(2,'0');};
  const setStatus=(message,ready=false)=>{status.textContent=message;status.classList.toggle('is-ready',ready);};
  const setProgress=()=>{
    const percent=Math.round(completed.size/Math.max(1,lessons.length)*100);
    $('overall-count').textContent=completed.size+' of '+lessons.length+' complete';
    $('overall-meter').setAttribute('aria-valuenow',String(percent));
    $('overall-fill').style.width=percent+'%';
  };
  const setWatchProgress=()=>{
    const duration=Number.isFinite(video.duration)?video.duration:0;
    const percent=duration?Math.round(video.currentTime/duration*100):0;
    $('elapsed').textContent=time(video.currentTime);
    $('duration').textContent=time(duration);
    $('watch-fill').style.width=percent+'%';
    $('watch-meter').setAttribute('aria-valuenow',String(percent));
  };
  const updatePlayLabel=()=>{
    const playing=!video.paused&&!video.ended;
    $('toggle-play').setAttribute('aria-label',playing?'Pause video':'Play video');
    $('toggle-play').setAttribute('title',playing?'Pause video':'Play video');
    $('play-icon').setAttribute('d',playing?'M7 5h4v14H7zm6 0h4v14h-4z':'M8 4.6a1 1 0 0 1 1.52-.85l10 7.4a1 1 0 0 1 0 1.7l-10 7.4A1 1 0 0 1 8 19.4Z');
    $('large-play').hidden=playing||isMissing||video.ended;
  };
  const updateCompletion=()=>{
    const done=completed.has(current),seen=watched.has(current),last=current===lessons.length-1;
    completeBtn.disabled=!(done||seen)||isMissing;
    if(isMissing){setStatus('Recording awaiting upload.');$('complete-label').textContent='Video required';}
    else if(done){setStatus('Day completed ✓',true);$('complete-label').textContent=last?'Course completed ✓':'Continue to Day '+(current+2);}
    else if(seen){setStatus('Video watched — ready to continue.',true);$('complete-label').textContent=last?'Mark course complete':'Mark complete & continue';}
    else{setStatus('Watch the full video to continue.');$('complete-label').textContent='Finish video to continue';}
    $('next-hint').textContent=last?'Final challenge':'Up next: Day '+(current+2);
    $('previous-day').disabled=current===0;
  };
  const updateOutline=()=>{
    document.querySelectorAll('.learn-day-btn').forEach(button=>{
      const n=Number(button.dataset.day),done=completed.has(n);
      button.disabled=!unlocked(n);
      button.classList.toggle('is-completed',done);
      button.setAttribute('aria-current',n===current?'step':'false');
      button.querySelector('.learn-day-bullet').textContent=done?'✓':String(n+1).padStart(2,'0');
      button.querySelector('.learn-day-lock').textContent=unlocked(n)?'':'⌁';
    });
  };
  const showMissing=()=>{
    isMissing=true;video.pause();video.hidden=true;
    $('large-play').hidden=true;$('video-missing').hidden=false;
    $('toggle-play').disabled=true;setWatchProgress();updateCompletion();
  };
  const openVideo=(path,mode)=>{
    mediaMode=mode;limit=0;isMissing=false;video.pause();
    video.removeAttribute('src');video.load();
    video.hidden=false;$('video-missing').hidden=true;
    $('toggle-play').disabled=false;
    video.src=path;video.defaultPlaybackRate=1;video.playbackRate=1;
    video.load();setWatchProgress();updatePlayLabel();
  };
  const select=n=>{
    if(n<0||n>=lessons.length||!unlocked(n))return;
    current=n;const lesson=lessons[n];
    $('day-number').textContent='DAY '+String(n+1).padStart(2,'0')+' / '+lessons.length;
    $('week-tag').textContent='WEEK '+(lesson.week+1);
    $('lesson-title').textContent=lesson.title.replace(/^Day\s*\d+\s*[·:–-]\s*/i,'');
    $('lesson-summary').textContent=lesson.summary||'Your next speaking challenge.';
    $('lesson-practice').textContent=lesson.practice||'Watch the video and practise with purpose.';
    $('watch-example').hidden=!lesson.solutionUrl;
    openVideo(lesson.videoUrl,'lesson');
    updateCompletion();updateOutline();setProgress();
    const url=new URL(location.href);
    url.searchParams.set('course',slug);url.searchParams.set('lesson',String(n+1));
    history.replaceState(null,'',url.pathname+url.search+url.hash);
    save();
    // Return focus to the immediate action area without forcing long page scrolling.
    if(window.innerWidth<=690)window.scrollTo({top:0,behavior:'instant'});
  };
  const togglePlayback=()=>{
    if(isMissing)return;
    if(video.paused){video.play().catch(()=>{});}else video.pause();
  };
  $('toggle-play').addEventListener('click',togglePlayback);
  $('large-play').addEventListener('click',togglePlayback);
  video.addEventListener('click',togglePlayback);
  video.addEventListener('play',updatePlayLabel);
  video.addEventListener('pause',updatePlayLabel);
  video.addEventListener('loadedmetadata',()=>{limit=0;setWatchProgress();updatePlayLabel();});
  video.addEventListener('timeupdate',()=>{
    if(!video.seeking && video.currentTime<=limit+1.2)limit=Math.max(limit,video.currentTime);
    setWatchProgress();
  });
  video.addEventListener('seeking',()=>{
    // Non-interactive watch bar + prevent programmatic forward seeking.
    if(video.currentTime>limit+0.9)video.currentTime=Math.max(0,limit-.05);
  });
  video.addEventListener('ratechange',()=>{
    if(video.playbackRate!==1)video.playbackRate=1;
  });
  video.addEventListener('ended',()=>{
    if(mediaMode==='lesson' && Number.isFinite(video.duration) && limit>=video.duration-1.7){
      watched.add(current);save();updateCompletion();
    }
    updatePlayLabel();
  });
  video.addEventListener('error',()=>{
    if(video.error && video.networkState!==HTMLMediaElement.NETWORK_NO_SOURCE)return;
    showMissing();
  });
  $('full-screen').addEventListener('click',()=>{
    if(document.fullscreenElement)document.exitFullscreen?.();
    else stage.requestFullscreen?.();
  });
  completeBtn.addEventListener('click',()=>{
    if(isMissing||(!watched.has(current)&&!completed.has(current)))return;
    completed.add(current);save();setProgress();updateOutline();
    if(current<lessons.length-1)select(current+1);
    else updateCompletion();
  });
  $('previous-day').addEventListener('click',()=>select(current-1));
  const outline=$('outline-list');
  course.modules.forEach((module,week)=>{
    const group=document.createElement('div');group.className='learn-week-block';
    const head=document.createElement('div');head.className='learn-week-name';
    const text=document.createElement('span');text.textContent=module.title;
    const count=document.createElement('span');count.textContent=module.lessons.length+' days';
    head.append(text,count);group.append(head);
    lessons.forEach((lesson,n)=>{
      if(lesson.week!==week)return;
      const button=document.createElement('button');button.className='learn-day-btn';
      button.type='button';button.dataset.day=n;
      const bullet=document.createElement('span');bullet.className='learn-day-bullet';bullet.textContent=String(n+1).padStart(2,'0');
      const title=document.createElement('span');title.className='learn-day-title';title.textContent=lesson.title.replace(/^Day \d+\s*[·:–-]\s*/i,'');
      const lock=document.createElement('span');lock.className='learn-day-lock';lock.setAttribute('aria-hidden','true');
      button.append(bullet,title,lock);
      button.addEventListener('click',()=>select(n));group.append(button);
    });
    outline.append(group);
  });
  $('outline-toggle').addEventListener('click',()=>{
    const parent=document.querySelector('.learn-outline');
    const opened=parent.classList.toggle('is-open');
    $('outline-toggle').setAttribute('aria-expanded',String(opened));
  });
  const dialog=$('worksheet-dialog'),pdf=$('worksheet-frame');
  $('open-worksheet').addEventListener('click',()=>{
    const lesson=lessons[current];
    $('worksheet-tag').textContent='WORKSHEET · DAY '+String(current+1).padStart(2,'0');
    $('worksheet-title').textContent=lesson.title.replace(/^Day \d+\s*[·:–-]\s*/i,'');
    pdf.hidden=false;$('worksheet-error').hidden=true;
    pdf.src=lesson.pdfUrl+'#toolbar=1';
    dialog.showModal();
  });
  const closePdf=()=>{dialog.close();pdf.removeAttribute('src');};
  $('close-worksheet').addEventListener('click',closePdf);
  dialog.addEventListener('click',event=>{if(event.target===dialog)closePdf();});
  $('watch-example').addEventListener('click',()=>{
    const lesson=lessons[current];
    if(!lesson.solutionUrl)return;
    if(mediaMode==='example'){select(current);return;}
    openVideo(lesson.solutionUrl,'example');
    setStatus('Example video — return to the main lesson to complete the day.');
    $('watch-example').querySelector('span:nth-child(2)').textContent='Return to main lesson';
  });
  const requested=Number(params.get('lesson'));
  if(Number.isInteger(requested)&&requested>=1&&requested<=lessons.length&&unlocked(requested-1))current=requested-1;
  if(!unlocked(current))current=lessons.findIndex((_,n)=>!completed.has(n));
  if(current<0)current=0;
  select(current);
})();
'''
(root/"academy-learn.js").write_text(js,encoding="utf-8")
assert "lms-player.js" not in html and "drive.google" not in html.lower()
assert "playbackRate=1" in js and "video.currentTime>limit" in js
assert "aspect-ratio:9/16" in css_new and ".learn-layout{display:grid" in css_new
print("Created fresh focused academy lesson page, separate CSS/JS, kept shared header/footer.")
