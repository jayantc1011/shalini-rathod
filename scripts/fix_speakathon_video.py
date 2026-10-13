#!/usr/bin/env python3
"""Correct Speakathon lesson-video framing according to the source MP4 metadata.
Run after build_self_hosted_lms.py without changing shared site components.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
html_path=root/'lms-learn.html'
css_path=root/'style.css'
player_path=root/'lms-player.js'
for path in (html_path,css_path,player_path):
    assert path.is_file(),f"Missing {path}"
html=html_path.read_text(encoding='utf8')
assert 'class="sr-video-shell" id="sr-video-shell"' in html, 'Expected original player class not found'
html=html.replace('class="sr-video-shell" id="sr-video-shell"','class="sr-video-shell sr-video-portrait" id="sr-video-shell"')
html_path.write_text(html,encoding='utf8')

css=r"""
/* =============================================================
   Source-aware video frame: Day 1 is 478 x 850 (portrait 9:16).
   Do NOT display a vertical MP4 by filling a 16:9 crop.
   The full video and its original aspect ratio are always visible.
   Works for portrait, landscape and mixed daily recordings.
   ============================================================= */
.sr-academy-player-page .sr-video-shell{
  width:100%;
  height:min(70vh,640px);
  min-height:350px;
  max-height:none;
  aspect-ratio:auto;
  display:flex;
  flex-direction:row;
  align-items:center;
  justify-content:center;
  position:relative;
  overflow:hidden;
  background:radial-gradient(ellipse at 50% 45%,#253c2f 0%,#131f19 68%,#111a15 100%);
}
.sr-academy-player-page .sr-video-shell.sr-video-portrait video{
  display:block;
  position:relative;
  flex:none;
  width:auto;
  height:100%;
  max-width:100%;
  max-height:100%;
  min-width:0;
  min-height:0;
  margin:0 auto;
  object-fit:contain;
  object-position:center center;
  aspect-ratio:auto;
  background:#111b16;
}
.sr-academy-player-page .sr-video-shell.sr-video-landscape{
  width:100%;
  aspect-ratio:16/9;
  height:auto;
  min-height:0;
  max-height:720px;
}
.sr-academy-player-page .sr-video-shell.sr-video-landscape video{
  display:block;
  position:relative;
  width:100%;
  height:100%;
  min-height:0;
  min-width:0;
  max-width:100%;
  max-height:100%;
  object-fit:contain;
  object-position:center center;
  aspect-ratio:auto;
  background:#111b16;
}
.sr-academy-player-page .sr-video-shell.sr-video-portrait::before,
.sr-academy-player-page .sr-video-shell.sr-video-portrait::after{
  position:absolute;
  top:50%;
  transform:translateY(-50%);
  color:rgba(221,239,207,.35);
  font:700 12px/1.6 "Bricolage Grotesque",sans-serif;
  letter-spacing:.22em;
  text-align:center;
  width:min(22%,210px);
  pointer-events:none;
}
.sr-academy-player-page .sr-video-shell.sr-video-portrait::before{
  content:"WATCH\A PRACTISE\A GROW";
  white-space:pre;
  left:3%;
}
.sr-academy-player-page .sr-video-shell.sr-video-portrait::after{
  content:"21 DAYS\A ONE VOICE";
  white-space:pre;
  right:3%;
}
.sr-academy-player-page .sr-video-shell video:fullscreen,
.sr-academy-player-page .sr-video-shell video:-webkit-full-screen{
  width:100%;
  height:100%;
  max-width:100vw;
  max-height:100vh;
  object-fit:contain;
  background:#000;
}
@media (max-width:750px){
 .sr-academy-player-page .sr-video-shell.sr-video-portrait{
    height:min(75vh,650px);
    min-height:0;
 }
 .sr-academy-player-page .sr-video-shell.sr-video-portrait::before,
 .sr-academy-player-page .sr-video-shell.sr-video-portrait::after{
    display:none;
 }
}
@media (max-width:480px){
 .sr-academy-player-page .sr-video-shell.sr-video-portrait{
   height:auto;
   min-height:0;
   aspect-ratio:9/16;
 }
 .sr-academy-player-page .sr-video-shell.sr-video-portrait video{
   width:100%;
   height:100%;
 }
}
"""
with css_path.open('a',encoding='utf8') as f:
    f.write('\n'+css+'\n')
js=player_path.read_text(encoding='utf8')
needle="const video=$('sr-lesson-video'),shell=$('sr-video-shell'),warning=$('sr-media-warning');"
assert needle in js, "Player structure changed; cannot safely patch."
addition=needle+"""
  const updateVideoOrientation=()=>{
    if(!video.videoWidth||!video.videoHeight)return;
    const isPortrait=video.videoHeight>video.videoWidth;
    shell.classList.toggle('sr-video-portrait',isPortrait);
    shell.classList.toggle('sr-video-landscape',!isPortrait);
    shell.dataset.videoSize=video.videoWidth+'x'+video.videoHeight;
    shell.dataset.videoOrientation=isPortrait?'portrait':'landscape';
  };
  video.addEventListener('loadedmetadata',updateVideoOrientation);
"""
js=js.replace(needle,addition)
needle2="video.src=path;video.playbackRate=Number($('sr-playback-rate').value)||1;"
assert needle2 in js
js=js.replace(needle2,
"""shell.classList.add('sr-video-portrait');shell.classList.remove('sr-video-landscape');
    video.src=path;video.playbackRate=Number($('sr-playback-rate').value)||1;""")
player_path.write_text(js,encoding='utf8')
assert 'video.videoHeight>video.videoWidth' in js
assert 'sr-video-portrait' in css
print('Fixed player: Day 1 displays as centered 9:16 portrait, other lessons adapt to MP4 metadata.')
