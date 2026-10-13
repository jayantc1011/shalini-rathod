#!/usr/bin/env python3
"""Remove duplicate legacy Shalini HTML pages while preserving the working LMS."""
from pathlib import Path
import re,sys
from html.parser import HTMLParser
root=Path(sys.argv[1]).resolve()
keep={"index.html","services.html","about.html","contact.html","package.html",
      "lms.html","lms-auth.html","lms-course.html","lms-learn.html"}
obsolete={"course.html","courses.html","dashboard.html","enrollment.html",
          "login.html","programs.html","communication-course.html"}
found={p.name for p in root.glob("*.html")}
assert found==keep|obsolete,f"Unexpected HTML pages: {found-(keep|obsolete)}, missing: {(keep|obsolete)-found}"
redirect={
 "communication-course.html":"lms-course.html",
 "course.html":"lms-course.html",
 "courses.html":"lms.html",
 "dashboard.html":"lms-learn.html",
 "enrollment.html":"lms-auth.html",
 "login.html":"lms-auth.html",
 "programs.html":"services.html",
}
modified=[]
for p in [*root.glob("*.html"),*root.glob("*.js")]:
 source=p.read_text(encoding="utf-8")
 text=source
 for old,new in redirect.items():
  text=re.sub(r'(?<![-\w])'+re.escape(old)+r'(?=([?#"\x27\s]|$))',new,text)
 if text!=source:
  modified.append(p.name)
  p.write_text(text,encoding="utf-8")
for name in sorted(obsolete):(root/name).unlink()
assert {p.name for p in root.glob("*.html")}==keep
for p in [*root.glob("*.html"),*root.glob("*.js")]:
 text=p.read_text(encoding="utf-8")
 for name in obsolete:
  assert not re.search(r'(?<![-\w])'+re.escape(name)+r'(?=([?#"\x27\s]|$))',text),(p.name,name)
class LinkParser(HTMLParser):
 def __init__(self):super().__init__();self.paths=[]
 def handle_starttag(self,tag,attrs):
  attr=dict(attrs)
  key={'a':'href','script':'src','link':'href','img':'src','video':'src','source':'src','iframe':'src'}.get(tag)
  if key and attr.get(key):self.paths.append((tag,attr[key]))
broken=[]
for p in root.glob("*.html"):
 parser=LinkParser();parser.feed(p.read_text(encoding="utf-8"))
 for tag,url in parser.paths:
  if url.startswith(("https:","http:","//","mailto:","tel:","data:","#","javascript:")):continue
  target=url.split("?")[0].split("#")[0]
  if target and not (root/target.lstrip("/")).exists():broken.append((p.name,tag,target))
assert not broken,"Broken local paths: "+repr(broken[:30])
videos=root/"assets/lms/videos"
have=[i for i in range(1,22) if (videos/f"day-{i:02d}.mp4").is_file()]
missing=[i for i in range(1,22) if i not in have]
assert have==list(range(1,12))+[15],have
assert (videos/"day-02.mp4").stat().st_size>1000000
assert len(list((root/"assets/lms/pdfs").glob("day-*.pdf")))==21
readme="""# Shalini Rathod — Clean website and Speakathon studio

START: Open index.html to view the website.
COURSES: Open lms.html to view the current catalog.
OVERVIEW: Open lms-course.html?course=speakathon for the challenge overview.
LESSONS: Open lms-learn.html?course=speakathon&lesson=1 to start Day 1.

Retained pages: Home, Services, About, Contact, Coaching Package,
LMS catalog, LMS login preview, challenge overview, and learning studio.
Obsolete course, courses, dashboard, enrollment, login, programs, and
communication-course duplicate HTML pages were removed.
All references in retained HTML/JavaScript were updated.

The Day 2 original recording is INCLUDED (assets/lms/videos/day-02.mp4).
Included videos: Days 1 through 11, and Day 15.
Not yet transferred: Days 12, 13, 14, 16, 17, 18, 19, 20, 21.
To finish those days, place their website-playable MP4s in
assets/lms/videos/day-XX.mp4. All 21 PDF worksheets are included.
The website does not redirect videos or PDFs to Google Drive.

TESTING VERSION: Skip Video is enabled for QA. Remove it before launch.
Browser-only completion checks cannot be tamper-proof without a backend.
"""
(root/"README.md").write_text(readme,encoding="utf-8")
print("RETAINED PAGES",sorted(keep))
print("REMOVED OLD PAGES",sorted(obsolete))
print("LINKS UPDATED",modified)
print("LOCAL LINKS BROKEN",len(broken))
print("VIDEOS INCLUDED",have)
print("VIDEOS MISSING",missing)
