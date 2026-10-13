#!/usr/bin/env python3
"""Final website-only, local-media mapping and content-integrity audit.

Validate that the source lesson day in courses-data.js corresponds to the
same-numbered local MP4 and PDF, with no substitutions for missing recordings.
"""
from pathlib import Path
import sys,re,json,hashlib,subprocess
site=Path(sys.argv[1]).resolve()
assert (site/'lms-learn.html').is_file()
assert (site/'courses-data.js').is_file()
assert (site/'assets/lms/videos/day-09.mp4').is_file()
assert (site/'assets/lms/videos/day-11.mp4').is_file()
lessons=(site/'courses-data.js').read_text(encoding='utf-8')
required=list(range(1,12))+[15]
missing=[12,13,14,16,17,18,19,20,21]
mp4s=[]
for day in range(1,22):
    token=f'assets/lms/videos/day-{day:02d}.mp4'
    assert token in lessons, f'Missing day {day} entry in course data'
    worksheets=f'assets/lms/pdfs/day-{day:02d}.pdf'
    assert worksheets in lessons, f'Missing day {day} PDF mapping'
    path=site/token
    if day in required:
        assert path.is_file() and path.stat().st_size>200000,token
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        mp4s.append((day,path.stat().st_size,digest))
    else:
        assert not path.exists(),f'Day {day} unexpected content: {path}'
assert len(set(d for _,_,d in mp4s))==len(mp4s),'Duplicate MP4 bytes across different days!'
assert len(list((site/'assets/lms/pdfs').glob('day-*.pdf')))==21
assert '<footer' not in (site/'lms-learn.html').read_text().lower()
assert 'id="qa-skip-video"' in (site/'lms-learn.html').read_text()
assert len(list(site.glob('*.html')))==9

report=[
    '# Speakathon — local media integrity check',
    'All lesson video URLs map to their matching numbered MP4 filenames.',
    'Different numbered MP4 files have different SHA256 hashes.',
    'The source videos were assigned by their Google Drive Challenge folder names.',
    'The content spoken inside each video has not been independently transcribed or verified.',
    'Day 12 and the other untransferred days deliberately show "Video not uploaded".',
    '',
    'INCLUDED:',
]
for day,size,digest in mp4s:
    report.append(f'Day {day:02d} -> assets/lms/videos/day-{day:02d}.mp4 | {size} bytes | SHA256 {digest}')
report+=['','NOT INCLUDED: '+', '.join(map(str,missing)), '',
    'Before public launch: remove TEST ONLY skip button. Production paid-course protections require a server.',
    'The original videos for missing days were too big for the connected per-file download service.',
]
(site/'VIDEO_MAPPING_CHECK.txt').write_text('\n'.join(report)+'\n',encoding='utf-8')
print('VERIFIED days',required)
print('UNAVAILABLE days',missing)
print('DISTINCT MP4 SHA256 count',len(set(d for _,_,d in mp4s)))
print('DAY 09 SHA256',dict((d,h) for d,_,h in mp4s)[9])
print('DAY 11 SHA256',dict((d,h) for d,_,h in mp4s)[11])
print('PDFs',len(list((site/'assets/lms/pdfs').glob('day-*.pdf'))))
