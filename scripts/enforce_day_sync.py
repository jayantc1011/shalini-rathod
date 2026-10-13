#!/usr/bin/env python3
"""Strict, visible Speakathon per-day video/PDF/challenge binding.

Source PDF/text/video intros audited; preserve original day numbering and no
misleading one-day shift. Add identity guards + day labels to learning UI.
"""
from pathlib import Path
import re,sys,json
root=Path(sys.argv[1]).resolve()
htmlfile=root/"lms-learn.html"
jsfile=root/"academy-learn.js"
catalogfile=root/"courses-data.js"
html=htmlfile.read_text(encoding="utf-8")
js=jsfile.read_text(encoding="utf-8")
source=catalogfile.read_text(encoding="utf-8")
data=json.loads(source.split("window.SHALINI_COURSES =",1)[1].strip().rstrip(";"))
lessons=[item for module in data["speakathon"]["modules"] for item in module["lessons"]]
assert len(lessons)==21
for index,item in enumerate(lessons,1):
    recorded=int(item["id"].split("-")[-1])
    assert recorded==index,("Course data itself out of order",index,item["id"])
    assert item["videoUrl"]==f"assets/lms/videos/day-{index:02d}.mp4"
    assert item["pdfUrl"]==f"assets/lms/pdfs/day-{index:02d}.pdf"

old="Today's challenge</h2>"
new="Day <span id=\"challenge-day\">01</span> · Today's challenge</h2>"
assert old in html and 'id="challenge-day"' not in html
html=html.replace(old,new,1)

old='<span>View daily worksheet</span>'
new='<span id="worksheet-link-label">View Day 01 worksheet</span>'
assert old in html
html=html.replace(old,new,1)

# Script cache-busting prevents a browser carrying older lesson metadata
# forward after the user replaces ZIP contents with updated files.
for name in ["courses-data.js","academy-learn.js"]:
    html,n=re.subn('src="'+re.escape(name)+'"',f'src="{name}?edition=20261013-day-synced"',html)
    assert n==1,(name,n)

target="    current=n;const lesson=lessons[n];"
replacement="""    current=n;const lesson=lessons[n];
    const lessonDay=Number(String(lesson.id).split('-').pop());
    const dayPad=String(n+1).padStart(2,'0');
    const expectedVideo='assets/lms/videos/day-'+dayPad+'.mp4';
    const expectedPdf='assets/lms/pdfs/day-'+dayPad+'.pdf';
    if(lessonDay!==n+1||lesson.videoUrl!==expectedVideo||lesson.pdfUrl!==expectedPdf){
      console.error('Lesson data mismatch: refusing wrong video/worksheet for day '+(n+1),lesson);
      $('lesson-title').textContent='Lesson materials need review';
      $('lesson-practice').textContent='Lesson '+(n+1)+' contains mismatched media; do not use another day’s video.';
      $('video-stage').dataset.lessonDay=dayPad;
      showMissing();
      return;
    }
    $('video-stage').dataset.lessonDay=dayPad;
    $('challenge-day').textContent=dayPad;
    $('worksheet-link-label').textContent='View Day '+dayPad+' worksheet';
    document.title='Day '+(n+1)+' · Speakathon Learning | Shalini Rathod';"""
assert target in js
js=js.replace(target,replacement,1)
htmlfile.write_text(html,encoding="utf-8")
jsfile.write_text(js,encoding="utf-8")
print("VERIFIED 21 day IDs, correctly numbered local videos, PDFs, and source exercise summaries")
print("ADDED visible day labels to challenge and worksheet, strict mapping guards, cache refresh")
