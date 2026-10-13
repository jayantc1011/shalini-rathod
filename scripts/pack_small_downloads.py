#!/usr/bin/env python3
"""Create lightweight, individually downloadable ZIPs from the verified Shalini build.
Every ZIP preserves paths relative to website root and can be extracted into the same folder.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
import json
root=Path('output/shalini-rathod-website').resolve()
assert (root/'index.html').is_file() and (root/'lms-learn.html').is_file()
dest=Path('output/parts').resolve()
dest.mkdir(parents=True,exist_ok=True)
all_files=sorted((p for p in root.rglob('*') if p.is_file()),key=lambda p:str(p.relative_to(root)))
videos=[p for p in all_files if p.relative_to(root).parts[:3]==('assets','lms','videos')]
pdfs=[p for p in all_files if p.relative_to(root).parts[:3]==('assets','lms','pdfs')]
website=[p for p in all_files if p not in set(videos+pdfs)]
assert len(list(root.glob('*.html')))==9
assert len(pdfs)==21 and len(videos)==16, (len(pdfs),len(videos))
print('SITE CORE RAW BYTES',sum(p.stat().st_size for p in website))
print('PDF TOTAL RAW BYTES',sum(p.stat().st_size for p in pdfs))
print('VIDEO TOTAL RAW BYTES',sum(p.stat().st_size for p in videos))

# Every artifact must remain small enough for ChatGPT downloads. Keep batches below 60MiB.
MAX=58*1024*1024
def group(files,limit=MAX):
 result=[];current=[];bytes_used=0
 for path in files:
  size=path.stat().st_size
  if current and bytes_used+size>limit:
   result.append(current);current=[];bytes_used=0
  current.append(path);bytes_used+=size
 if current:result.append(current)
 return result
def make_zip(name,files):
 path=dest/name
 with ZipFile(path,'w') as z:
  for p in files:
   # Deflate site JS/CSS/HTML. MP4/PDF are already compressed; store original bytes.
   ty=ZIP_DEFLATED if p.suffix.lower() not in ('.mp4','.pdf','.png','.jpg','.jpeg','.webp','.woff','.woff2') else ZIP_STORED
   z.write(p,str(p.relative_to(root)),compress_type=ty,compresslevel=7 if ty==ZIP_DEFLATED else None)
 assert path.stat().st_size<71*1024*1024,(name,path.stat().st_size)
 with ZipFile(path) as z:
  bad=z.testzip()
  assert bad is None, (name,bad)
 return path
parts=[]
for category,paths in [('Core',website),('PDFs',pdfs),('Videos',videos)]:
 for i,batch in enumerate(group(paths),1):
  name=f'Shalini-{category}-Part-{i:02d}.zip'
  pack=make_zip(name,batch)
  parts.append({'name':name,'category':category,'bytes':pack.stat().st_size,'files':[str(p.relative_to(root)) for p in batch]})
  print('CREATED',name,round(pack.stat().st_size/1024/1024,1),'MiB',
        'FILES',len(batch),'FIRST',str(batch[0].relative_to(root)),'LAST',str(batch[-1].relative_to(root)))
print('PART COUNT',len(parts))
assert len(parts)<=14,'Too many parts; adjust archive size rules'
manifest={'instructions':'Extract all ZIPs into one website directory, merging folders/overwriting where prompted.',
          'part_count':len(parts),'parts':parts,'all_original_files':len(all_files)}
(dest/'PARTS-MANIFEST.json').write_text(json.dumps(manifest,indent=2))
assert sorted(file for item in parts for file in item['files'])==sorted(str(p.relative_to(root)) for p in all_files)
print('ALL ORIGINAL WEBSITE FILES ACCOUNTED FOR',len(all_files))
