#!/usr/bin/env python3
"""Desktop-focused learning workspace: no page/footer scrolling, independently scrollable roadmap,
and temporary QA-only Skip Video button. Apply to the already-built latest site ZIP.
"""
from pathlib import Path
import re,sys
root=Path(sys.argv[1]).resolve()
html_path=root/"lms-learn.html"
css_path=root/"academy-learn.css"
js_path=root/"academy-learn.js"
assert all(p.is_file() for p in (html_path,css_path,js_path))

html=html_path.read_text(encoding="utf-8")
html,n=re.subn(r"<footer\b[^>]*>.*?</footer>\s*","",html,flags=re.I|re.S)
assert n==1,f"Expected one learner-only footer, got {n}"
assert "academy-learn.css" in html
html=html.replace('<link rel="stylesheet" href="academy-learn.css">','<link rel="stylesheet" href="academy-learn.css">\n  <link rel="stylesheet" href="academy-workspace.css">',1)

old_outline='''<div class="learn-outline-header"><div><span class="learn-eyebrow">YOUR LEARNING PATH</span><h2>21 days to confidence.</h2></div><button id="outline-toggle" class="learn-outline-toggle" type="button" aria-expanded="false" aria-controls="outline-list">Lessons <span aria-hidden="true">⌄</span></button></div>'''
new_outline='''<div class="learn-outline-header">
          <div><span class="learn-eyebrow">21-DAY CHALLENGE</span><h2>Course lessons</h2></div>
          <button id="outline-toggle" class="learn-outline-toggle" type="button" aria-expanded="false" aria-controls="outline-list">View days <span aria-hidden="true">⌄</span></button>
        </div>
        <div class="learn-roadmap-progress"><span>YOUR PROGRESS</span><strong id="roadmap-done">0 / 21</strong><div class="learn-roadmap-track"><span id="roadmap-fill"></span></div></div>'''
assert old_outline in html
html=html.replace(old_outline,new_outline,1)

needle='''<button id="complete-and-next" class="learn-complete-btn" type="button" disabled><span id="complete-label">Finish video to continue</span><span aria-hidden="true">→</span></button>'''
assert needle in html
html=html.replace(needle,needle+'''
          <button id="qa-skip-video" type="button" class="learn-qa-skip" title="Temporary pre-launch testing only; remove before publishing"><span class="learn-qa-badge">TEST ONLY</span><span>Skip video &amp; next day</span><span aria-hidden="true">↗</span></button>''',1)
html_path.write_text(html,encoding="utf-8")

css=r'''/* ===========================================================================
   SPEAKATHON IMMERSIVE CLASSROOM · 2026-10
   Full viewport desktop app; only the course lesson list scrolls.
   The desktop page/footer never scrolls. This stylesheet is page-scoped.
   =========================================================================== */
@media (min-width: 1001px) {
  html:has(body.fresh-learn){
    height:100%;
    overflow:hidden;
  }
  body.fresh-learn {
    height:100vh;
    height:100dvh;
    min-height:0;
    overflow:hidden;
    display:flex;
    flex-direction:column;
  }
  body.fresh-learn > .sr-header {
    flex:0 0 auto;
    z-index:60;
  }
  .fresh-learn .learn {
    flex:1 1 0;
    min-height:0;
    width:100%;
    padding:0;
    overflow:hidden;
    display:flex;
    flex-direction:column;
  }
  .fresh-learn .learn-container{
    flex:1 1 0;
    min-height:0;
    display:flex;
    flex-direction:column;
    overflow:hidden;
  }
  .fresh-learn .learn-top{
    flex:0 0 61px;
    min-height:61px;
  }
  .fresh-learn .learn-layout{
    flex:1 1 0;
    min-height:0;
    overflow:hidden;
    padding:18px 0 18px;
    display:grid;
    grid-template-columns:minmax(220px,310px) minmax(290px,1fr) minmax(274px,350px);
    gap:clamp(17px,2vw,30px);
    align-items:stretch;
  }
  .fresh-learn .learn-video-column{
    height:100%;
    min-height:0;
    overflow:hidden;
  }
  .fresh-learn .learn-video{
    width:min(100%,310px,calc((100dvh - 224px)*9/16));
    height:auto;
    aspect-ratio:9/16;
    min-height:0;
    max-height:calc(100% - 44px);
    flex:0 0 auto;
  }
  .fresh-learn .learn-video-bar{
    width:min(100%,310px,calc((100dvh - 224px)*9/16));
    flex:0 0 auto;
    padding-top:10px;
  }
  .fresh-learn .learn-lesson{
    display:flex;
    flex-direction:column;
    min-height:0;
    min-width:0;
    overflow:hidden;
    padding:12px 0 0;
  }
  .fresh-learn .learn-lesson h1{
    font-size:clamp(26px,2.5vw,41px);
    line-height:1.12;
    margin:10px 0 11px;
    letter-spacing:-.044em;
  }
  .fresh-learn .learn-summary{
    font-size:13px;
    line-height:1.5;
    margin-bottom:18px;
  }
  .fresh-learn .learn-practice{
    padding-top:15px;
  }
  .fresh-learn .learn-practice p {
    line-height:1.6;
    font-size:13px;
    margin:0 0 12px;
  }
  .fresh-learn .learn-complete{
    padding-top:12px;
  }
  .fresh-learn .learn-pdf-link{
    margin:6px 0;
    padding:11px 13px;
  }
  .fresh-learn .learn-completion-note{
    margin-bottom:8px;
  }
  .fresh-learn .learn-complete-btn{
    padding:13px 15px;
  }
  .fresh-learn .learn-next-link{
    padding:9px 0;
  }
}
.fresh-learn .learn-outline{
  min-height:0;
  height:100%;
  display:flex;
  flex-direction:column;
  align-items:stretch;
  overflow:hidden;
  padding:0;
  border:1px solid #e1e8dd;
  border-radius:18px;
  background:#fff;
  box-shadow:0 10px 35px rgba(27,52,32,.05);
}
.fresh-learn .learn-outline-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  padding:22px 21px 18px;
  border-bottom:1px solid #edf0e9;
  flex:0 0 auto;
  background:#fff;
}
.fresh-learn .learn-outline-header h2{
  font-size:21px;
  line-height:1.12;
  letter-spacing:-.045em;
  font-weight:800;
  color:#233c2e;
  margin:7px 0 0;
}
.fresh-learn .learn-outline .learn-eyebrow{
  color:#8ba18a;
  font-size:10px;
  letter-spacing:.17em;
}
.fresh-learn .learn-roadmap-progress{
  flex:0 0 auto;
  display:grid;
  grid-template-columns:1fr auto;
  align-items:center;
  gap:10px;
  padding:12px 21px 14px;
  background:#fbfcfa;
  color:#809082;
  font-size:9px;
  font-weight:800;
  letter-spacing:.1em;
}
.fresh-learn .learn-roadmap-progress strong{
  font-size:12px;
  color:#3d6244;
  letter-spacing:0;
}
.fresh-learn .learn-roadmap-track{
  grid-column:1/-1;
  height:4px;
  background:#e6eddf;
  border-radius:50px;
  overflow:hidden;
}
.fresh-learn .learn-roadmap-track>span{
  display:block;
  height:100%;
  width:0%;
  background:#83b45e;
  transition:width .25s;
}
.fresh-learn .learn-outline-list{
  flex:1 1 0;
  min-height:0;
  max-height:none;
  padding:8px 9px 14px 13px;
  overflow-y:auto;
  overflow-x:hidden;
  overscroll-behavior:contain;
  scrollbar-width:thin;
  scrollbar-color:#b7c8af transparent;
  scroll-behavior:smooth;
}
.fresh-learn .learn-outline-list::-webkit-scrollbar{
  width:6px;
}
.fresh-learn .learn-outline-list::-webkit-scrollbar-thumb{
  border-radius:9px;
  background:#b7c8af;
}
.fresh-learn .learn-outline-list::-webkit-scrollbar-track{
  background:transparent;
}
.fresh-learn .learn-week-block{margin:0 0 10px}
.fresh-learn .learn-week-name{
  position:sticky;
  z-index:4;
  top:-9px;
  border:0;
  padding:14px 7px 9px;
  background:#fff;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  color:#648362;
  font-size:10px;
  font-weight:800;
  letter-spacing:.035em;
}
.fresh-learn .learn-week-block + .learn-week-block{
  border-top:1px solid #e9eee7;
}
.fresh-learn .learn-week-name span:last-child{
  color:#9cae98;
  background:#f0f5ed;
  border-radius:5px;
  font-size:9px;
  padding:4px 6px;
  white-space:nowrap;
}
.fresh-learn .learn-day-btn{
  display:flex;
  align-items:center;
  width:100%;
  min-height:53px;
  gap:11px;
  padding:9px 9px;
  margin:2px 0;
  border:1px solid transparent;
  border-radius:10px;
  background:transparent;
  color:#526a59;
  font-size:12px;
  line-height:1.4;
  font-weight:600;
  cursor:pointer;
  opacity:1;
}
.fresh-learn .learn-day-btn:disabled{
  opacity:1;
  color:#647568;
  cursor:default;
  background:transparent;
}
.fresh-learn .learn-day-btn[aria-current="step"]{
  border-color:#d9eac9;
  background:#e8f2df;
  box-shadow:inset 3px 0 0 #75a85e;
  color:#255137;
  font-weight:800;
}
.fresh-learn .learn-day-btn:hover:enabled:not([aria-current="step"]){
  background:#f4f8f1;
  border-color:#e9efe3;
}
.fresh-learn .learn-day-bullet{
  border:1px solid #e1e8dc;
  background:#f7f9f5;
  width:31px;
  height:31px;
  border-radius:9px;
  flex:0 0 31px;
  font-size:11px;
  color:#6b816f;
}
.fresh-learn .learn-day-btn[aria-current="step"] .learn-day-bullet{
  background:#cce8af;
  border-color:#cce8af;
  color:#315c32;
}
.fresh-learn .learn-day-btn.is-completed .learn-day-bullet{
  color:#fff;
  background:#5e9563;
  border-color:#5e9563;
}
.fresh-learn .learn-day-title{
  flex:1;
  min-width:0;
}
.fresh-learn .learn-day-lock{
  color:#b2bfb2;
  opacity:1;
  font-size:12px;
}
.fresh-learn .learn-qa-skip{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  width:100%;
  margin-top:9px;
  border:1px dashed #c8bb95;
  background:#fffbef;
  border-radius:9px;
  padding:10px 12px;
  color:#806b3d;
  font-weight:750;
  font-size:11px;
  cursor:pointer;
}
.fresh-learn .learn-qa-skip:hover{background:#fbf0d5}
.fresh-learn .learn-qa-badge{
  white-space:nowrap;
  background:#f2e4ba;
  color:#725821;
  border-radius:4px;
  padding:4px 5px;
  font-size:9px;
  letter-spacing:.04em;
  font-weight:900;
}
.fresh-learn .learn-qa-skip span:last-child{margin-left:auto;font-size:15px}
@media(min-width:1001px) and (max-height:740px){
  .fresh-learn .learn-top{min-height:50px;flex-basis:50px}
  .fresh-learn .learn-layout{padding:11px 0 11px}
  .fresh-learn .learn-lesson{padding-top:3px}
  .fresh-learn .learn-lesson h1{font-size:clamp(23px,2.25vw,33px);margin:7px 0}
  .fresh-learn .learn-summary{margin-bottom:10px}
  .fresh-learn .learn-practice{padding-top:9px}
  .fresh-learn .learn-practice p{line-height:1.43;margin-bottom:7px}
  .fresh-learn .learn-pdf-link{padding:7px 12px;margin:4px 0}
  .fresh-learn .learn-complete{padding-top:5px}
  .fresh-learn .learn-complete-btn{padding:10px 14px}
  .fresh-learn .learn-qa-skip{padding:7px 9px;margin-top:6px}
  .fresh-learn .learn-next-link{padding:5px 0}
  .fresh-learn .learn-video{width:min(100%,290px,calc((100dvh - 200px)*9/16))}
  .fresh-learn .learn-video-bar{width:min(100%,290px,calc((100dvh - 200px)*9/16))}
}
@media(min-width:1001px) and (max-width:1200px){
  .fresh-learn .learn-container{width:calc(100% - 34px)}
  .fresh-learn .learn-layout{
    grid-template-columns:minmax(210px,268px) minmax(300px,1fr) minmax(250px,288px);
    gap:16px;
  }
  .fresh-learn .learn-outline-header{padding:17px 14px 13px}
  .fresh-learn .learn-roadmap-progress{padding:10px 14px 12px}
  .fresh-learn .learn-outline-list{padding:6px 6px 12px 9px}
}
@media(max-width:1000px){
  /* Normal page scrolling is necessary on tablets and phones to preserve usability. */
  .fresh-learn .learn-outline{
    height:auto;
    min-height:0;
    overflow:hidden;
    padding:0;
    border:1px solid #e1e8dd;
    border-radius:16px;
  }
  .fresh-learn .learn-outline-list{
    max-height:360px;
    overflow-y:auto;
    display:block;
    padding:8px 12px 12px;
  }
  .fresh-learn .learn-outline-header{padding:17px}
  .fresh-learn .learn-roadmap-progress{padding:9px 17px 12px}
  .fresh-learn .learn-week-block{margin:0 0 9px}
}
@media(max-width:690px){
  .fresh-learn .learn-outline-list{display:none}
  .fresh-learn .learn-outline.is-open .learn-outline-list{display:block}
  .fresh-learn .learn-qa-skip{padding:9px 11px}
}
'''
(root/"academy-workspace.css").write_text(css,encoding="utf-8")

js=js_path.read_text(encoding="utf-8")
needle="    $('overall-fill').style.width=percent+'%';"
assert needle in js
js=js.replace(needle,needle+"""
    $('roadmap-done').textContent=completed.size+' / '+lessons.length;
    $('roadmap-fill').style.width=percent+'%';""",1)

needle2="    updateCompletion();updateOutline();setProgress();"
assert needle2 in js
js=js.replace(needle2,needle2+"""
    const currentButton=document.querySelector('.learn-day-btn[data-day="'+n+'"]');
    if(currentButton && window.innerWidth>1000) {
      currentButton.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'});
    }""",1)
needle3="  select(current);\n})();"
assert needle3 in js
js=js.replace(needle3,"""  // Pre-launch QA shortcut: deliberately allows navigating all 21 lessons even if
  // some videos are still missing. Remove the button and this handler before publishing.
  $('qa-skip-video').addEventListener('click',()=>{
    watched.add(current);
    completed.add(current);
    save();
    setProgress();
    updateOutline();
    if(current<lessons.length-1)select(current+1);
    else updateCompletion();
  });
  select(current);
})();""",1)
js_path.write_text(js,encoding="utf-8")
assert "<footer" not in html_path.read_text(encoding="utf-8")
assert "qa-skip-video" in js_path.read_text(encoding="utf-8")
print("Immersive desktop learner: fixed viewport, independent roadmap scrollbar, no footer, QA skip and unlock action.")
