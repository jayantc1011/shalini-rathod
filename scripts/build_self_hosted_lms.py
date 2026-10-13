#!/usr/bin/env python3
"""Upgrade the CURRENT Shalini website snapshot, preserving all other pages."""
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
assert (root / "lms-learn.html").is_file()
assert (root / "courses-data.js").is_file()
src = (root / "courses-data.js").read_text(encoding="utf-8")
assert src.lstrip().startswith("/* Offline-friendly")
payload = src[src.index("window.SHALINI_COURSES =") + len("window.SHALINI_COURSES ="):].strip().rstrip(";")
catalog = json.loads(payload)
speak = catalog["speakathon"]
for module in speak["modules"]:
    for item in module["lessons"]:
        n = int(item["id"].split("-")[-1])
        item["videoUrl"] = f"assets/lms/videos/day-{n:02d}.mp4"
        item["pdfUrl"] = f"assets/lms/pdfs/day-{n:02d}.pdf"
        item["source"] = "Shalini Rathod Academy · hosted course media"
        if item.get("solutionUrl"):
            item["solutionUrl"] = f"assets/lms/videos/day-{n:02d}-solution.mp4"
resource_paths = {
    "Welcome · Introduction video":"assets/lms/videos/introduction.mp4",
    "Guide for Course":"assets/lms/resources/course-guide.jpg",
    "Printable Progress Tracker":"assets/lms/pdfs/progress-tracker.pdf",
    "Templates":"assets/lms/pdfs/templates.pdf",
    "Mastering Posture & Body Language":"assets/lms/pdfs/mastering-posture.pdf",
    "Introvert to Influencer · Book":"assets/lms/pdfs/introvert-to-influencer.pdf",
    "25 Gems to Influence Anyone · Brochure":"assets/lms/pdfs/25-gems.pdf",
    "The End · Closing video":"assets/lms/videos/closing.mp4",
}
for resource in speak.get("resources", []):
    resource["url"] = resource_paths.get(resource["title"], "")
speak["description"] = ("21 practical challenges, video lessons and downloadable practice worksheets. "
                        "Watch, practise and track your confidence journey in one learning space.")
(root / "courses-data.js").write_text("/* Self-hosted course catalog · no Google Drive URLs. */\nwindow.SHALINI_COURSES = " +
    json.dumps(catalog,ensure_ascii=False,indent=2) + ";\n", encoding="utf-8")
old = (root / "lms-learn.html").read_text(encoding="utf-8")
header = re.search(r"<header\b[^>]*>.*?</header>",old,re.S|re.I)
footer = re.search(r"<footer\b[^>]*>.*?</footer>",old,re.S|re.I)
assert header and footer, "Original shared header/footer not found; refuse destructive replacement."
html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Watch the 21-Day Speakathon Challenge videos, read your daily PDF worksheets and practise with Shalini Rathod Academy.">
<title>21-Day Speakathon Learning Studio | Shalini Rathod Academy</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body class="academy-page lms-shell sr-academy-player-page" data-lms-page="lms-learn">
__HEADER__
<main id="main-content" class="sr-study">
  <div class="sr-study-topbar">
    <div class="sr-study-wrap sr-study-top-inner">
      <div class="sr-study-breadcrumb"><a href="lms.html">Academy</a><span>›</span><a id="sr-study-overview" href="lms-course.html?course=speakathon">Course overview</a><span>›</span><strong>Learning studio</strong></div>
      <span class="sr-study-chip">SELF-PACED LEARNING</span>
    </div>
  </div>
  <div class="sr-study-wrap">
    <div class="sr-study-heading">
      <div><span class="sr-study-kicker">SHALINI RATHOD ACADEMY · YOUR LEARNING PATH</span>
        <h1 id="sr-course-title">21-Day Speakathon Challenge</h1>
        <p>One small speaking challenge every day. Watch the lesson, use your worksheet and practise with purpose.</p>
      </div>
      <div class="sr-study-progress"><div><span>Your progress</span><strong id="sr-progress-label">0 / 21</strong></div>
        <div class="sr-study-track" role="progressbar" aria-label="Course progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="sr-progress-meter"><span id="sr-progress-fill"></span></div>
        <small>Saved on this device</small>
      </div>
    </div>
    <div class="sr-study-layout">
      <div class="sr-study-content">
        <section class="sr-watch-card" aria-label="Lesson content">
          <div class="sr-player-meta"><span id="sr-active-week">WEEK 01 · FIND YOUR VOICE</span><span id="sr-lesson-count">LESSON 01 OF 21</span></div>
          <div class="sr-video-shell" id="sr-video-shell">
            <video id="sr-lesson-video" controls playsinline preload="metadata" poster="assets/lms/demo-poster.jpg" aria-label="Speakathon lesson video">Your browser does not support HTML5 video.</video>
            <div id="sr-media-warning" class="sr-media-warning" hidden>
              <span aria-hidden="true">▶</span><strong>Recording awaiting upload</strong>
              <p>This lesson is ready. Add its MP4 to the website's <code>assets/lms/videos/</code> folder to enable playback here.</p>
            </div>
          </div>
          <div class="sr-player-actions">
            <div class="sr-view-tabs" role="tablist" aria-label="Lesson materials">
              <button id="sr-tab-video" role="tab" aria-selected="true" type="button">▶ Video lesson</button>
              <button id="sr-tab-pdf" role="tab" aria-selected="false" type="button">▤ Daily worksheet</button>
            </div>
            <label class="sr-speed-control" for="sr-playback-rate">Speed <select id="sr-playback-rate" aria-label="Video playback speed"><option value="1">1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></label>
          </div>
        </section>
        <section id="sr-inline-pdf" class="sr-inline-pdf" hidden aria-label="Daily worksheet viewer">
          <div class="sr-pdf-header"><div><span class="sr-study-kicker">WORKBOOK</span><h2>Today's practice worksheet</h2></div><a id="sr-pdf-download" class="sr-button sr-button-outline" href="#" download>↓ Download PDF</a></div>
          <iframe id="sr-pdf-frame" title="Daily challenge PDF" loading="lazy"></iframe>
          <p id="sr-pdf-fallback" class="sr-pdf-fallback" hidden>Worksheet not yet added to the website. Upload the matching PDF to <code>assets/lms/pdfs/</code>.</p>
        </section>
        <section class="sr-lesson-details">
          <div class="sr-lesson-heading"><span id="sr-current-tag" class="sr-study-kicker">DAY 01 · LEARN & PRACTISE</span><h2 id="sr-current-title">Get comfortable speaking on camera</h2><p id="sr-current-summary">Build confidence one speaking exercise at a time.</p></div>
          <div class="sr-task-block"><span class="sr-task-icon" aria-hidden="true">✦</span><div><h3>Your challenge</h3><p id="sr-current-practice"></p></div></div>
          <div class="sr-lesson-extras"><div class="sr-extras-label">Supporting recordings</div><div id="sr-extra-videos" class="sr-extra-videos"></div></div>
          <div class="sr-lesson-completion"><span>Finish your practice before moving forward.</span><button id="sr-complete" class="sr-button sr-button-main" type="button">Mark lesson complete ✓</button></div>
        </section>
        <div class="sr-prevnext"><button id="sr-prev" type="button">← Previous lesson</button><button id="sr-next" type="button">Next lesson →</button></div>
        <section class="sr-resources-section" aria-label="Extra learning resources">
          <div><span class="sr-study-kicker">YOUR RESOURCE LIBRARY</span><h2>Everything for your journey</h2><p>Welcome lesson, templates, study resources and more — view them within your learning space.</p></div>
          <div id="sr-extra-resources" class="sr-resource-grid"></div>
        </section>
      </div>
      <aside class="sr-study-sidebar" aria-label="Course navigation">
        <div class="sr-sidebar-heading"><div><span class="sr-study-kicker">YOUR CURRICULUM</span><h2>Course content</h2></div><span id="sr-lessons-total">21 lessons</span></div>
        <label class="sr-lesson-search-label"><span aria-hidden="true">⌕</span><input id="sr-search-lessons" type="search" placeholder="Find a lesson…" aria-label="Search lessons"></label>
        <div id="sr-module-list" class="sr-module-list"></div>
      </aside>
    </div>
  </div>
</main>
<dialog id="sr-resource-dialog" class="sr-resource-dialog" aria-labelledby="sr-resource-title">
  <div class="sr-resource-modal-head"><h2 id="sr-resource-title">Learning resource</h2><button id="sr-resource-close" type="button" aria-label="Close resource">×</button></div>
  <div id="sr-resource-viewer"></div>
</dialog>
__FOOTER__
<script src="courses-data.js"></script>
<script src="lms-player.js"></script>
<script src="script.js"></script>
</body></html>
'''
html = html.replace("__HEADER__",header.group()).replace("__FOOTER__",footer.group())
(root / "lms-learn.html").write_text(html,encoding="utf-8")
style = r'''
/* ==============================================================
   SPEAKATHON STUDY SPACE  ·  self-hosted video + PDF reader
   Scoped to the learner page; original shared website remains.
   ============================================================== */
.sr-academy-player-page{--sr-ink:#253126;--sr-muted:#687269;--sr-forest:#304e39;--sr-green:#d9ec89;--sr-border:#e5e9dd;background:#f7f8f2;color:var(--sr-ink)}
.sr-academy-player-page button,.sr-academy-player-page input,.sr-academy-player-page select{font:inherit}
.sr-academy-player-page [hidden]{display:none!important}
.sr-academy-player-page a{text-decoration:none}
.sr-study{padding:0 0 86px;font-family:"Bricolage Grotesque",sans-serif}
.sr-study-wrap{width:min(1480px,calc(100% - 72px));margin:0 auto}
.sr-study-topbar{background:#fff;border-bottom:1px solid var(--sr-border)}
.sr-study-top-inner{display:flex;align-items:center;justify-content:space-between;min-height:56px;gap:15px}
.sr-study-breadcrumb{display:flex;align-items:center;gap:10px;flex-wrap:wrap;color:#809083;font-size:13px}
.sr-study-breadcrumb a{color:#5d6b60}
.sr-study-breadcrumb strong{color:#324638;font-weight:600}
.sr-study-chip{background:#eaf1d9;color:#38513a;padding:7px 11px;border-radius:8px;font-size:10px;font-weight:800;letter-spacing:.09em;white-space:nowrap}
.sr-study-heading{padding:43px 0 31px;display:flex;justify-content:space-between;gap:40px;align-items:end}
.sr-study-kicker{font-size:11px;letter-spacing:.16em;font-weight:800;color:#729049;display:inline-block}
.sr-study-heading h1{font-size:clamp(33px,4vw,57px);line-height:1.05;letter-spacing:-.045em;margin:11px 0 12px;color:#24382b}
.sr-study-heading p{max-width:650px;color:var(--sr-muted);line-height:1.65;font-size:15px;margin:0}
.sr-study-progress{width:240px;flex:none}
.sr-study-progress>div:first-child{display:flex;justify-content:space-between;font-size:13px;color:#738072;margin-bottom:12px}
.sr-study-progress strong{font-size:15px;color:#314a35}
.sr-study-progress small{color:#91a08b;font-size:11px;display:block;text-align:right;margin-top:8px}
.sr-study-track{background:#e5e9dd;border-radius:100px;height:9px;overflow:hidden}
.sr-study-track span{background:linear-gradient(90deg,#78a267,#b6d26b);display:block;width:0%;height:100%;border-radius:100px;transition:width .25s}
.sr-study-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(295px,350px);gap:26px;align-items:start}
.sr-study-content{min-width:0}
.sr-watch-card,.sr-lesson-details,.sr-study-sidebar,.sr-resources-section,.sr-inline-pdf{background:#fff;border:1px solid #e6e9df;border-radius:20px;box-shadow:0 13px 35px rgba(38,56,35,.035);overflow:hidden}
.sr-player-meta{display:flex;justify-content:space-between;gap:10px;padding:17px 22px;font-size:11px;font-weight:800;letter-spacing:.12em;color:#667761}
.sr-video-shell{position:relative;background:#121c18;width:100%;aspect-ratio:16/9;overflow:hidden;display:grid;place-items:center}
.sr-video-shell video{width:100%;height:100%;display:block;object-fit:contain;background:#121c18}
.sr-media-warning{position:absolute;inset:0;background:linear-gradient(140deg,#1a2c21,#101b15);color:white;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:28px;gap:13px}
.sr-media-warning>span{height:72px;width:72px;border-radius:999px;background:rgba(218,236,137,.15);display:grid;place-items:center;color:#d9ec89;font-size:28px}
.sr-media-warning strong{font-size:21px}
.sr-media-warning p{max-width:400px;font-size:13px;line-height:1.6;color:#c5cfbc}
.sr-media-warning code{font-size:12px;color:#d9ec89}
.sr-player-actions{padding:13px 20px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.sr-view-tabs{background:#f1f4eb;border-radius:10px;padding:4px;display:flex;gap:4px}
.sr-view-tabs button{border:0;background:transparent;color:#778476;border-radius:7px;padding:10px 15px;font-size:12px;font-weight:800;cursor:pointer;transition:.2s}
.sr-view-tabs button[aria-selected="true"]{background:#fff;color:#304c38;box-shadow:0 2px 6px #263c2410}
.sr-speed-control{display:flex;align-items:center;gap:9px;font-size:12px;font-weight:700;color:#7a887c}
.sr-speed-control select{border:1px solid #e4eade;border-radius:8px;padding:8px;background:#f8faf5;color:#3d523f}
.sr-inline-pdf{margin-top:18px;padding:24px}
.sr-pdf-header{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:16px}
.sr-pdf-header h2{font-size:20px;letter-spacing:-.02em;margin:5px 0 0}
.sr-inline-pdf iframe{border:1px solid #dde4d8;border-radius:12px;display:block;width:100%;height:min(75vh,850px);background:#f4f7ef}
.sr-pdf-fallback{background:#fff5df;padding:15px;border-radius:10px;color:#6e5335}
.sr-lesson-details{margin-top:20px;padding:30px}
.sr-lesson-heading h2{font-size:clamp(24px,2.8vw,33px);font-weight:800;letter-spacing:-.035em;margin:11px 0}
.sr-lesson-heading p{color:#7b8779;line-height:1.65;font-size:14px;margin:0 0 22px}
.sr-task-block{border:1px solid #e9eedc;background:#f8fbef;display:flex;gap:15px;align-items:start;padding:23px;border-radius:14px}
.sr-task-icon{width:35px;height:35px;border-radius:10px;background:#e1eebf;display:grid;place-items:center;color:#48683a;flex:none}
.sr-task-block h3{font-size:15px;margin:0 0 7px;color:#35523b}
.sr-task-block p{font-size:14px;line-height:1.75;color:#657661;margin:0}
.sr-lesson-extras{margin-top:21px}
.sr-extras-label{font-size:11px;color:#80917f;letter-spacing:.1em;font-weight:800;text-transform:uppercase;margin-bottom:9px}
.sr-extra-videos{display:flex;gap:10px;flex-wrap:wrap}
.sr-extra-videos button{border:1px solid #dae4d5;background:#fff;padding:10px 13px;border-radius:9px;color:#405e44;font-size:12px;font-weight:700;cursor:pointer}
.sr-lesson-completion{margin-top:25px;border-top:1px solid #edf0e9;padding-top:22px;display:flex;justify-content:space-between;gap:18px;align-items:center}
.sr-lesson-completion span{font-size:13px;color:#8c978a}
.sr-button{display:inline-flex;align-items:center;justify-content:center;padding:11px 18px;min-height:42px;border-radius:10px;font-size:12px;font-weight:800;letter-spacing:.005em;cursor:pointer;border:1px solid transparent}
.sr-button-main{background:#304f39;color:#fff}
.sr-button-outline{border-color:#dbe5d7;color:#365440;background:#fff}
.sr-prevnext{display:flex;align-items:center;justify-content:space-between;margin:14px 2px 34px;gap:12px}
.sr-prevnext button{background:transparent;border:0;color:#3f6046;padding:9px;font-size:13px;font-weight:800;cursor:pointer}
.sr-prevnext button:disabled{opacity:.35;cursor:not-allowed}
.sr-study-sidebar{position:sticky;top:24px;padding:22px;max-height:min(1000px,calc(100vh - 42px));overflow:auto}
.sr-sidebar-heading{display:flex;justify-content:space-between;align-items:center;gap:10px}
.sr-sidebar-heading h2{font-size:21px;letter-spacing:-.025em;margin:7px 0 20px}
.sr-sidebar-heading>span{font-size:11px;color:#738572;background:#eef4e4;border-radius:6px;padding:7px;white-space:nowrap}
.sr-lesson-search-label{display:flex;gap:10px;align-items:center;border:1px solid #e8ecdf;border-radius:10px;padding:10px 13px;margin-bottom:20px;background:#f9fbf7}
.sr-lesson-search-label span{font-size:19px;color:#85957f}
.sr-lesson-search-label input{width:100%;border:0;outline:0;background:transparent;color:#405442;font-size:13px}
.sr-module{border:1px solid #e9eee6;border-radius:12px;overflow:hidden;margin-bottom:10px}
.sr-module>summary{cursor:pointer;padding:15px;background:#f7f9f4;display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:12px;font-weight:800;color:#526b54;list-style:none}
.sr-module>summary::-webkit-details-marker{display:none}
.sr-module>summary small{color:#93a18f;font-size:11px}
.sr-module-list{padding:6px}
.sr-lesson-button{border:0;border-radius:8px;background:transparent;display:flex;align-items:center;gap:11px;text-align:left;padding:10px 7px;width:100%;font-size:12px;line-height:1.4;color:#647564;cursor:pointer}
.sr-lesson-button:hover{background:#f4f9ee}
.sr-lesson-button[aria-current="step"]{background:#eff5e3;color:#35563d;font-weight:800}
.sr-lesson-number{width:28px;height:28px;border:1px solid #e1e9d9;border-radius:8px;display:grid;place-items:center;flex:none;font-size:11px;font-weight:800}
.sr-lesson-button.is-done .sr-lesson-number{background:#dcefbd;color:#3d6539}
.sr-lesson-name{flex:1}
.sr-resources-section{padding:29px;margin-top:30px}
.sr-resources-section h2{margin:8px 0 8px;font-size:23px}
.sr-resources-section p{margin:0 0 22px;color:#859180;font-size:13px;line-height:1.5}
.sr-resource-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.sr-resource{padding:15px;display:flex;gap:12px;align-items:center;text-align:left;border:1px solid #e8eee1;background:#fbfcf8;border-radius:12px;cursor:pointer;color:#314a37}
.sr-resource-icon{background:#eaf2d9;width:37px;height:37px;border-radius:10px;display:grid;place-items:center;flex:none}
.sr-resource strong{font-size:12px;display:block}
.sr-resource small{font-size:11px;color:#859582;display:block;margin-top:3px}
.sr-resource-dialog{width:min(1000px,95vw);max-height:94vh;border:0;border-radius:18px;padding:0;box-shadow:0 30px 80px #0e241955;background:#fff}
.sr-resource-dialog::backdrop{background:#0a170bb8}
.sr-resource-modal-head{display:flex;justify-content:space-between;align-items:center;padding:17px 23px;border-bottom:1px solid #e7ebdf;gap:15px}
.sr-resource-modal-head h2{font-size:17px;margin:0}
.sr-resource-modal-head button{font-size:25px;background:transparent;border:0;cursor:pointer}
.sr-resource-dialog video{width:100%;display:block;aspect-ratio:16/9;background:#101c18;object-fit:contain}
.sr-resource-dialog iframe{display:block;width:100%;height:70vh;border:0}
.sr-resource-dialog img{display:block;max-width:100%;max-height:75vh;margin:auto}
.sr-resource-missing{padding:35px;color:#6d786b;text-align:center}
@media(max-width:1100px){.sr-study-layout{grid-template-columns:minmax(0,1fr) 295px;gap:15px}.sr-study-wrap{width:min(100% - 35px,1480px)}.sr-study-sidebar{padding:14px}}
@media(max-width:900px){.sr-study-layout{grid-template-columns:1fr}.sr-study-sidebar{position:static;max-height:none;order:-1}.sr-study-heading{align-items:start}.sr-study-progress{width:190px}.sr-module-list{max-height:360px;overflow:auto}}
@media(max-width:650px){.sr-study-wrap{width:calc(100% - 28px)}.sr-study-heading{padding:28px 0 22px;display:block}.sr-study-heading h1{font-size:34px}.sr-study-progress{width:100%;margin-top:22px}.sr-study-chip{display:none}.sr-player-meta{padding:12px;font-size:9px}.sr-player-actions{padding:10px;flex-wrap:wrap}.sr-view-tabs{width:100%}.sr-view-tabs button{flex:1;padding:10px 5px;font-size:11px}.sr-speed-control{margin-left:auto}.sr-lesson-details,.sr-resources-section{padding:19px}.sr-task-block{padding:17px}.sr-resource-grid{grid-template-columns:1fr}.sr-lesson-completion{align-items:stretch;flex-direction:column}.sr-inline-pdf{padding:13px}.sr-inline-pdf iframe{height:65vh}.sr-pdf-header{align-items:start;flex-direction:column}.sr-prevnext button{font-size:12px}.sr-study-sidebar{order:0}}
'''
with (root / "style.css").open("a",encoding="utf-8") as css:
    css.write("\n"+style+"\n")
js = r'''(() => {
  'use strict';
  const catalog=window.SHALINI_COURSES||{};
  const params=new URLSearchParams(location.search);
  const slug=Object.prototype.hasOwnProperty.call(catalog,params.get('course'))?params.get('course'):'speakathon';
  const course=catalog[slug];
  if(!course)return;
  const $=id=>document.getElementById(id);
  const flat=course.modules.flatMap((module,group)=>module.lessons.map((lesson)=>({...lesson,moduleTitle:module.title,group})));
  const storageKey='shalini-course-progress-v2:'+slug;
  let saved={};
  try{saved=JSON.parse(localStorage.getItem(storageKey)||'{}')||{};}catch(_){}
  const completed=new Set((Array.isArray(saved.completed)?saved.completed:[]).filter(n=>Number.isInteger(n)&&n>=0&&n<flat.length));
  const requested=Number(params.get('lesson'));
  let index=Number.isInteger(requested)&&requested>=1&&requested<=flat.length?requested-1:(Number.isInteger(saved.active)&&saved.active>=0&&saved.active<flat.length?saved.active:0);
  let mode='video',mediaKind='lesson';
  const video=$('sr-lesson-video'),shell=$('sr-video-shell'),warning=$('sr-media-warning');
  const frame=$('sr-pdf-frame'),pdfPanel=$('sr-inline-pdf');
  $('sr-course-title').textContent=course.title;
  document.title=course.title+' | Shalini Rathod Academy';
  $('sr-study-overview').href='lms-course.html?course='+encodeURIComponent(slug);
  $('sr-lessons-total').textContent=flat.length+' lessons';
  const notice=msg=>{warning.querySelector('p').textContent=msg;warning.hidden=false;video.hidden=true;};
  const showVideo=(path)=>{
    video.pause(); video.removeAttribute('src');video.load();mediaKind='lesson';
    warning.hidden=true;video.hidden=false;
    if(!path){notice('This recording has not been uploaded to the website yet.');return;}
    video.src=path;video.playbackRate=Number($('sr-playback-rate').value)||1;
    video.load();
  };
  video.addEventListener('error',()=>{
    if(mode==='video')notice('The video file is not on this website yet. Add the matching MP4 to assets/lms/videos/ and refresh this page.');
  });
  const save=()=>{try{localStorage.setItem(storageKey,JSON.stringify({completed:[...completed],active:index}));}catch(_){}};
  let groups=[];
  course.modules.forEach((mod,group)=>{
    const d=document.createElement('details');d.className='sr-module';d.open=group===0;
    const summary=document.createElement('summary');const name=document.createElement('span');name.textContent=mod.title;
    const count=document.createElement('small');count.textContent=mod.lessons.length+' lessons';
    summary.append(name,count);d.append(summary);
    const list=document.createElement('div');list.className='sr-module-list';
    flat.forEach((lesson,i)=>{
      if(lesson.group!==group)return;
      const button=document.createElement('button');button.type='button';button.className='sr-lesson-button';button.dataset.index=i;
      const num=document.createElement('span');num.className='sr-lesson-number';num.textContent=String(i+1).padStart(2,'0');
      const label=document.createElement('span');label.className='sr-lesson-name';label.textContent=lesson.title;
      button.append(num,label);button.addEventListener('click',()=>selectLesson(i));
      list.append(button);
    });d.append(list);$('sr-module-list').append(d);groups.push(d);
  });
  $('sr-search-lessons').addEventListener('input',e=>{
    const q=e.target.value.trim().toLowerCase();
    groups.forEach(d=>{let found=0;d.querySelectorAll('.sr-lesson-button').forEach(b=>{const match=!q||b.textContent.toLowerCase().includes(q);b.hidden=!match;if(match)found++;});d.hidden=!found; if(q)d.open=true;});
  });
  const openPdf=()=>{
    const pdf=flat[index]?.pdfUrl;
    if(!pdf){$('sr-pdf-fallback').hidden=false;frame.hidden=true;return;}
    frame.hidden=false;$('sr-pdf-fallback').hidden=true;
    if(frame.getAttribute('src')!==pdf+'#toolbar=1')frame.src=pdf+'#toolbar=1';
    $('sr-pdf-download').href=pdf;
    $('sr-pdf-download').download='Speakathon-Day-'+String(index+1).padStart(2,'0')+'.pdf';
  };
  const setMode=next=>{
    mode=next;
    $('sr-tab-video').setAttribute('aria-selected',String(next==='video'));
    $('sr-tab-pdf').setAttribute('aria-selected',String(next==='pdf'));
    pdfPanel.hidden=next!=='pdf';
    shell.hidden=next!=='video';
    $('sr-playback-rate').disabled=next!=='video';
    if(next==='pdf'){video.pause();openPdf();}
    else if(video.error||!video.src||mediaKind!=='lesson'){showVideo(flat[index]?.videoUrl);}
  };
  $('sr-tab-video').addEventListener('click',()=>setMode('video'));
  $('sr-tab-pdf').addEventListener('click',()=>setMode('pdf'));
  $('sr-playback-rate').addEventListener('change',e=>{video.playbackRate=Number(e.target.value)||1;});
  const openResource=(resource)=>{
    const dialog=$('sr-resource-dialog'),viewer=$('sr-resource-viewer');
    viewer.replaceChildren();$('sr-resource-title').textContent=resource.title;
    const path=resource.url;
    if(!path){const text=document.createElement('p');text.className='sr-resource-missing';text.textContent='This resource is being prepared for upload to the website.';viewer.append(text);}
    else if(resource.type==='video'){const media=document.createElement('video');media.controls=true;media.playsInline=true;media.src=path;media.onerror=()=>{media.replaceWith(Object.assign(document.createElement('p'),{className:'sr-resource-missing',textContent:'The video has not been uploaded to the website yet.'}));};viewer.append(media);}
    else if(resource.type==='pdf'){const pdf=document.createElement('iframe');pdf.title=resource.title;pdf.src=path+'#toolbar=1';viewer.append(pdf);}
    else if(resource.type==='image'){const img=document.createElement('img');img.alt=resource.title;img.src=path;viewer.append(img);}
    dialog.showModal();
  };
  $('sr-resource-close').addEventListener('click',()=>$('sr-resource-dialog').close());
  $('sr-resource-dialog').addEventListener('close',()=>{const v=$('sr-resource-viewer').querySelector('video');if(v)v.pause();$('sr-resource-viewer').replaceChildren();});
  $('sr-resource-dialog').addEventListener('click',e=>{if(e.target===$('sr-resource-dialog'))$('sr-resource-dialog').close();});
  (course.resources||[]).forEach(resource=>{
    if(!resource.url)return;
    const b=document.createElement('button');b.type='button';b.className='sr-resource';
    const i=document.createElement('span');i.className='sr-resource-icon';i.textContent=resource.type==='video'?'▶':resource.type==='pdf'?'▤':'▧';
    const t=document.createElement('span');const strong=document.createElement('strong');strong.textContent=resource.title;
    const small=document.createElement('small');small.textContent=resource.note||'View resource';
    t.append(strong,small);b.append(i,t);b.addEventListener('click',()=>openResource(resource));$('sr-extra-resources').append(b);
  });
  const selectLesson=(newIndex)=>{
    if(newIndex<0||newIndex>=flat.length)return;
    index=newIndex;mediaKind='lesson';
    const lesson=flat[index];
    $('sr-current-tag').textContent='DAY '+String(index+1).padStart(2,'0')+' · LEARN & PRACTISE';
    $('sr-current-title').textContent=lesson.title.replace(/^Day \d+\s*[·-]\s*/i,'');
    $('sr-current-summary').textContent=lesson.summary||'Explore this lesson at your pace.';
    $('sr-current-practice').textContent=lesson.practice||'Watch the lesson and reflect on one key takeaway.';
    $('sr-active-week').textContent=lesson.moduleTitle.toUpperCase();
    $('sr-lesson-count').textContent='LESSON '+String(index+1).padStart(2,'0')+' OF '+flat.length;
    $('sr-prev').disabled=index===0;$('sr-next').disabled=index===flat.length-1;
    $('sr-extra-videos').replaceChildren();
    if(lesson.solutionUrl){const b=document.createElement('button');b.textContent='▶ Watch solution / example';b.type='button';
      b.addEventListener('click',()=>{setMode('video');showVideo(lesson.solutionUrl);mediaKind='solution';});
      $('sr-extra-videos').append(b);}
    if(frame){frame.removeAttribute('src');}
    showVideo(lesson.videoUrl);
    if(mode==='pdf')openPdf();
    const title='Day '+(index+1);
    document.querySelectorAll('.sr-lesson-button').forEach(b=>{
      const n=Number(b.dataset.index),done=completed.has(n);b.classList.toggle('is-done',done);b.setAttribute('aria-current',String(n===index?'step':'false'));b.querySelector('.sr-lesson-number').textContent=done?'✓':String(n+1).padStart(2,'0');
    });
    groups[lesson.group].open=true;
    const percent=Math.round(completed.size/Math.max(1,flat.length)*100);
    $('sr-progress-label').textContent=completed.size+' / '+flat.length;
    $('sr-progress-fill').style.width=percent+'%';
    $('sr-progress-meter').setAttribute('aria-valuenow',String(percent));
    $('sr-complete').textContent=completed.has(index)?'✓ Completed · Undo':'Mark lesson complete ✓';
    $('sr-complete').setAttribute('aria-pressed',String(completed.has(index)));
    const url=new URL(location.href);url.searchParams.set('course',slug);url.searchParams.set('lesson',String(index+1));
    history.replaceState(null,'',url.pathname+url.search+url.hash);
    save();
  };
  $('sr-complete').addEventListener('click',()=>{if(completed.has(index))completed.delete(index);else completed.add(index);selectLesson(index);});
  $('sr-prev').addEventListener('click',()=>selectLesson(index-1));
  $('sr-next').addEventListener('click',()=>selectLesson(index+1));
  selectLesson(index);
})();
'''
(root / "lms-player.js").write_text(js,encoding="utf-8")
(root / "assets/lms/videos").mkdir(parents=True,exist_ok=True)
(root / "assets/lms/pdfs").mkdir(parents=True,exist_ok=True)
(root / "assets/lms/resources").mkdir(parents=True,exist_ok=True)
(root / "SELF_HOSTED_MEDIA_README.md").write_text(
"""# Speakathon course - on-site media

Open lms-learn.html?course=speakathon&lesson=1 in a browser served by a local web server.
All 21 worksheet PDFs are at assets/lms/pdfs/day-01.pdf through day-21.pdf.

The 21 source MP4 videos are ~6 GB total. This ZIP includes only the videos
specifically named in MEDIA_STATUS.json. Other recordings must be uploaded to
assets/lms/videos/day-XX.mp4 on the website's media hosting/server.
Do NOT point them at Drive; the LMS will show a transparent missing-media
state until a recording exists. For 6GB of videos, use object storage/CDN
on your own domain rather than committing them to a GitHub Pages repository.

Because this is static HTML, course progress is stored only in localStorage.
It is not an authentication or purchase gate. Use authenticated hosting
before publishing paid course content publicly. No original website
navigation or other pages were removed.
""",encoding="utf-8")
assert "drive.google.com" not in (root / "courses-data.js").read_text()
assert "drive.google.com" not in (root / "lms-learn.html").read_text()
print("Updated 21 lesson entries; built local video player, onsite PDF reader, responsive LMS.")
