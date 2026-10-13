from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
import re,json
root=Path('output/shalini-rathod-website')
print("===== ALL HTML PAGES =====")
for p in sorted(root.rglob('*.html')):
 if 'node_modules' in p.parts:continue
 print(f"{p.relative_to(root)} SIZE={p.stat().st_size:,}")
print("===== TOP-LEVEL ASSETS =====")
for p in sorted(root.iterdir()):
 if p.is_dir():print("DIR",p.name)
 elif p.suffix.lower() in ('.css','.js','.md','.json'):print("FILE",p.name)
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('a','script','link','iframe','img','video','source'):
   key={'a':'href','script':'src','link':'href','iframe':'src','img':'src','video':'src','source':'src'}[tag]
   if key in a:self.urls.append((tag,a[key]))
print("===== HTML PAGE NAV TARGETS =====")
for p in sorted(root.glob('*.html')):
 parser=Links()
 parser.feed(p.read_text(errors='ignore'))
 targets=defaultdict(set)
 missing=set()
 for tag,url in parser.urls:
  local=url.split('#')[0].split('?')[0]
  if not local or re.match(r'^(?:https?:|mailto:|tel:|data:|//|javascript:)',local):continue
  targets[tag].add(local)
  if not (root/local.lstrip('/')).exists() and local not in ('/','#') and not local.startswith('#'):
   missing.add(local)
 print(f"\nPAGE {p.name}")
 print(" LINK HTML",sorted(x for x in targets.get('a',set()) if x.endswith('.html')))
 print(" SCRIPTS",sorted(targets.get('script',[])))
 print(" STYLES",sorted(targets.get('link',[])))
 print(" MISSING PATHS",sorted(missing)[:30])
print("===== HTML ALL REFERENCES CROSS-FILES =====")
for name in ['course.html','courses.html','lms-course.html','lms.html','lms-learn.html','services.html','index.html']:
 matches=[]
 for f in root.rglob('*'):
  if f.is_file() and f.suffix.lower() in ('.js','.html','.css','.json') and f.stat().st_size<1500000:
   s=f.read_text(errors='ignore')
   k=len(re.findall(r'\b'+re.escape(name)+r'\b',s,re.I))
   if k:matches.append((str(f.relative_to(root)),k))
 print(name,matches[:30])
print("===== DIRECT MEDIA =====")
v=root/'assets/lms/videos'
for p in sorted(v.glob('*')):
 print(p.name,p.stat().st_size)

print("===== PAGE TITLE AND FIRST H1 =====")
for p in sorted(root.glob("*.html")):
 txt=p.read_text(errors="ignore")
 title=re.search(r'<title[^>]*>(.*?)</title>',txt,re.S|re.I)
 h1=re.search(r'<h1[^>]*>(.*?)</h1>',txt,re.S|re.I)
 clean=lambda x: re.sub(r'<[^>]*>','',x or '').strip()[:180]
 print(p.name,"TITLE:",clean(title.group(1) if title else ''),"H1:",clean(h1.group(1) if h1 else ''))
print("===== SOURCE LINK CONTEXT FOR LEGACY PAGES =====")
for legacy in ['course.html','courses.html','dashboard.html','enrollment.html','login.html','package.html','programs.html','communication-course.html']:
 for source in sorted(root.iterdir()):
  if not source.is_file() or source.suffix.lower() not in ('.js','.html'): continue
  txt=source.read_text(errors="ignore")
  for match in list(re.finditer(r'(?<![-\w])'+re.escape(legacy),txt))[:3]:
   loc=match.start();frag=txt[max(0,loc-110):loc+140].replace('\n',' ')
   print(legacy, source.name, '...' + frag + '...')
