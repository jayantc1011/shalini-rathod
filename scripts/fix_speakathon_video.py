#!/usr/bin/env python3
"""Restore a portrait-only Speakathon player (9:16) and remove the extra side artwork.
Runs after the unchanged main website builder. Only the lesson player is altered.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
html_path=root/"lms-learn.html"
css_path=root/"style.css"
js_path=root/"lms-player.js"
assert all(x.is_file() for x in (html_path,css_path,js_path))

html=html_path.read_text(encoding="utf-8")
original='class="sr-video-shell" id="sr-video-shell"'
assert original in html, "Expected unchanged 21-day LMS player container"
html=html.replace(original,'class="sr-video-shell sr-video-portrait" id="sr-video-shell"',1)
html_path.write_text(html,encoding="utf-8")

css=css_path.read_text(encoding="utf-8")
# Remove original landscape constraint at its source, rather than appending duplicate 16:9 definitions.
old='.sr-video-shell{position:relative;background:#121c18;width:100%;aspect-ratio:16/9;overflow:hidden;display:grid;place-items:center}'
new='.sr-video-shell{position:relative;background:#000;width:100%;aspect-ratio:9/16;overflow:hidden;display:block}'
assert old in css,"Original wide video shell not found"
css=css.replace(old,new,1)
css += r"""

/* Speakathon portrait media · use exactly 9:16. No decorative side panels.
   Center the complete video without cropping, stretching, blurred padding or side copy. */
.sr-academy-player-page .sr-watch-card {
  width: min(100%, 380px);
  max-width: 380px;
  margin: 0 auto;
}
.sr-academy-player-page .sr-video-shell,
.sr-academy-player-page .sr-video-shell.sr-video-portrait {
  width: 100%;
  height: auto;
  min-height: 0;
  max-height: none;
  aspect-ratio: 9/16;
  display: block;
  overflow: hidden;
  position: relative;
  background: #000;
  margin: 0;
}
.sr-academy-player-page .sr-video-shell video {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  min-width: 0;
  min-height: 0;
  display: block;
  object-fit: contain;
  object-position: center center;
  background: #000;
  aspect-ratio: 9/16;
}
.sr-academy-player-page .sr-video-shell::before,
.sr-academy-player-page .sr-video-shell::after {
  display: none;
  content: none;
}
.sr-academy-player-page .sr-video-shell video:fullscreen,
.sr-academy-player-page .sr-video-shell video:-webkit-full-screen {
  width: 100%;
  height: 100%;
  max-width: 100vw;
  max-height: 100vh;
  object-fit: contain;
  aspect-ratio: auto;
  background: #000;
}
.sr-academy-player-page .sr-player-actions {
  gap: 8px;
  padding: 10px;
}
.sr-academy-player-page .sr-view-tabs {
  flex: 1 1 100%;
  width: 100%;
}
.sr-academy-player-page .sr-view-tabs button {
  flex: 1;
  padding: 10px 5px;
}
.sr-academy-player-page .sr-speed-control {margin-left: auto;}
@media(max-width:650px){
  .sr-academy-player-page .sr-watch-card{
    width: min(100%, 380px);
    max-width: 100%;
  }
}
"""
css_path.write_text(css,encoding="utf-8")
js=js_path.read_text(encoding="utf-8")
assert "const video=$('sr-lesson-video'),shell=$('sr-video-shell'),warning=$('sr-media-warning');" in js
# Portrait is intentional for every Speakathon lesson; never switch to 16:9.
assert "video.src=path;video.playbackRate=Number($('sr-playback-rate').value)||1;" in js
js=js.replace(
  "video.src=path;video.playbackRate=Number($('sr-playback-rate').value)||1;",
  "shell.classList.add('sr-video-portrait');\n    video.src=path;video.playbackRate=Number($('sr-playback-rate').value)||1;",
  1
)
js_path.write_text(js,encoding="utf-8")
assert 'aspect-ratio:9/16' in css
assert 'WATCH\\A' not in css
assert 'sr-video-landscape' not in css
assert 'video.videoHeight>video.videoWidth' not in js
print("Portrait-only 9:16 player ready. No banners, no side backgrounds, no landscape switching.")
