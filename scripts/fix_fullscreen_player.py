#!/usr/bin/env python3
"""Improve Shalini Speakathon player: true video overlay controls that remain visible in fullscreen,
better matched 9:16 video height, preserve current learning workspace and QA skip.
Only intended for the focused LMS page.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
htmlfile=root/"lms-learn.html"; cssfile=root/"academy-workspace.css"; jsfile=root/"academy-learn.js"
assert all(p.is_file() for p in (htmlfile,cssfile,jsfile))
html=htmlfile.read_text(encoding="utf-8")
bar_start=html.index('        <div class="learn-video-bar">')
bar_end=html.index('\n      </section>',bar_start)
bar=html[bar_start:bar_end]
assert 'id="toggle-play"' in bar and 'id="full-screen"' in bar and bar.rstrip().endswith("</div>")
start=html[:bar_start]
idx=start.rfind('        </div>\n')
assert idx>html.index('id="video-stage"'),"Unable to find player closing DIV"
end=html[bar_end:]
bar=bar.replace('          <button id="full-screen"', '''          <button id="volume-toggle" class="learn-icon-button" type="button" aria-label="Mute video" title="Mute or unmute"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5ZM15.5 8a5 5 0 0 1 0 8"/></svg></button>
          <button id="full-screen"''')
assert 'id="volume-toggle"' in bar
bar=bar.replace('<div class="learn-video-bar">','<div class="learn-video-bar" role="group" aria-label="Video controls">',1)
html=start[:idx]+bar+'\n'+start[idx:]+end
assert html.index('id="volume-toggle"')<html.index('</section>',html.index('id="video-stage"'))
assert html.index('id="full-screen"')<html.index('</section>',html.index('id="video-stage"'))
assert html.count('class="learn-video-bar"')==1
htmlfile.write_text(html,encoding="utf-8")

css=r'''
/* 9:16 portrait player now spans the same vertical space as the course outline,
   while preserving the actual video aspect ratio and avoiding letterboxed side bars.
   Controls are an overlay INSIDE #video-stage, including during fullscreen. */
.fresh-learn .learn-video {
  position:relative;
  isolation:isolate;
}
.fresh-learn .learn-video-bar {
  position:absolute;
  left:0;
  right:0;
  bottom:0;
  z-index:10;
  width:100%;
  max-width:none;
  margin:0;
  padding:22px 12px 10px;
  display:flex;
  align-items:center;
  gap:8px;
  background:linear-gradient(to bottom,transparent 0%,rgba(0,0,0,.45) 30%,rgba(0,0,0,.85) 100%);
  color:#fff;
  border-radius:0 0 12px 12px;
  pointer-events:auto;
}
.fresh-learn .learn-video-bar .learn-icon-button {
  display:grid;
  flex:0 0 27px;
  width:27px;
  height:27px;
  padding:4px;
  border:0;
  border-radius:5px;
  color:#fff;
  background:transparent;
}
.fresh-learn .learn-video-bar .learn-icon-button:hover {
  background:rgba(255,255,255,.19);
}
.fresh-learn .learn-video-bar .learn-icon-button:focus-visible {
  outline:2px solid #bbf36a;
  outline-offset:2px;
}
.fresh-learn .learn-video-bar .learn-duration {
  color:#f9fbf5;
  font-size:10px;
  flex:0 0 auto;
  gap:4px;
}
.fresh-learn .learn-video-bar .learn-duration-divider {color:#d0d5d0}
.fresh-learn .learn-video-bar .learn-playback-progress {
  flex:1 1 0;
  width:auto;
  height:4px;
  min-width:20px;
  border-radius:8px;
  background:rgba(255,255,255,.4);
}
.fresh-learn .learn-video-bar .learn-playback-progress>span {
  background:#bdf35b;
}
.fresh-learn .learn-video video {
  object-fit:contain;
  object-position:center center;
  width:100%;
  height:100%;
}
.fresh-learn #video-stage:fullscreen,
.fresh-learn #video-stage:-webkit-full-screen {
  width:100vw!important;
  height:100vh!important;
  height:100dvh!important;
  max-width:none!important;
  max-height:none!important;
  aspect-ratio:auto!important;
  border-radius:0!important;
  background:#000;
}
.fresh-learn #video-stage:fullscreen video,
.fresh-learn #video-stage:-webkit-full-screen video {
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:contain;
  background:#000;
}
.fresh-learn #video-stage:fullscreen .learn-video-bar,
.fresh-learn #video-stage:-webkit-full-screen .learn-video-bar {
  position:absolute;
  z-index:20;
  left:50%;
  right:auto;
  bottom:0;
  transform:translateX(-50%);
  width:min(100%,750px);
  max-width:100%;
  padding:28px 20px max(20px,env(safe-area-inset-bottom));
  border-radius:0;
}
.fresh-learn #video-stage:fullscreen .learn-icon-button,
.fresh-learn #video-stage:-webkit-full-screen .learn-icon-button {
  width:34px;
  height:34px;
  flex-basis:34px;
}
.fresh-learn #video-stage:fullscreen .learn-duration,
.fresh-learn #video-stage:-webkit-full-screen .learn-duration {
  font-size:13px;
}
@media(min-width:1001px){
  .fresh-learn .learn-layout {
    grid-template-columns:clamp(330px,29vw,410px) minmax(290px,1fr) minmax(270px,350px);
    gap:clamp(15px,1.8vw,28px);
  }
  .fresh-learn .learn-video-column {
    min-height:0;
    justify-content:flex-start;
  }
  .fresh-learn .learn-video {
    width:min(100%,calc((100dvh - 191px)*9/16));
    max-width:100%;
    height:auto;
    max-height:100%;
    flex:0 0 auto;
    aspect-ratio:9/16;
    border-radius:13px;
  }
  .fresh-learn .learn-video-bar {
    padding:18px 11px 10px;
  }
}
@media(min-width:1001px) and (max-height:740px){
  .fresh-learn .learn-video {
    width:min(100%,calc((100dvh - 162px)*9/16));
    height:auto;
    max-height:100%;
  }
}
@media(max-width:1000px){
  .fresh-learn .learn-video {
    width:min(100%,340px);
    aspect-ratio:9/16;
  }
  .fresh-learn .learn-video-bar {
    padding:18px 9px 9px;
    gap:5px;
  }
}
@media(max-width:390px) {
  .fresh-learn .learn-video-bar .learn-icon-button {
    flex-basis:24px;
    width:24px;
  }
  .fresh-learn .learn-video-bar .learn-duration {
    font-size:9px;
  }
}
'''
with cssfile.open("a",encoding="utf-8") as f:f.write("\n"+css+"\n")
js=jsfile.read_text(encoding="utf-8")
target="""  $('full-screen').addEventListener('click',()=>{
    if(document.fullscreenElement)document.exitFullscreen?.();
    else stage.requestFullscreen?.();
  });"""
assert target in js
replacement="""  const fullscreenBtn=$('full-screen'),volumeBtn=$('volume-toggle');
  const syncFullscreen=()=>{
    const active=document.fullscreenElement===stage || document.webkitFullscreenElement===stage;
    fullscreenBtn.setAttribute('aria-label',active?'Exit full screen':'Full screen');
    fullscreenBtn.setAttribute('title',active?'Exit full screen':'Full screen');
    fullscreenBtn.innerHTML=active
      ? '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 9h6V3M21 9h-6V3M3 15h6v6M21 15h-6v6"/></svg>'
      : '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 3H3v5M16 3h5v5M21 16v5h-5M3 16v5h5"/></svg>';
  };
  fullscreenBtn.addEventListener('click',async()=>{
    try{
      if(document.fullscreenElement)await document.exitFullscreen();
      else if(stage.requestFullscreen)await stage.requestFullscreen();
      else if(stage.webkitRequestFullscreen)stage.webkitRequestFullscreen();
      else if(video.webkitEnterFullscreen){
        // Safari iOS cannot fullscreen generic containers. Native controls remain usable there.
        video.controls=true;
        video.webkitEnterFullscreen();
      }
    }catch(e){console.warn('Full-screen operation unavailable',e);}
    syncFullscreen();
  });
  document.addEventListener('fullscreenchange',syncFullscreen);
  document.addEventListener('webkitfullscreenchange',syncFullscreen);
  video.addEventListener('webkitendfullscreen',()=>{video.controls=false;syncFullscreen();});
  const syncMute=()=>{
    const mute=video.muted||video.volume===0;
    volumeBtn.setAttribute('aria-label',mute?'Unmute video':'Mute video');
    volumeBtn.setAttribute('title',mute?'Unmute video':'Mute video');
    volumeBtn.innerHTML=mute
      ? '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4V5ZM16 9l5 6m0-6-5 6"/></svg>'
      : '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4V5ZM15.5 8a5 5 0 0 1 0 8"/></svg>';
  };
  volumeBtn.addEventListener('click',()=>{video.muted=!video.muted;syncMute();});
  video.addEventListener('volumechange',syncMute);
  syncMute();"""
js=js.replace(target,replacement,1)
assert "video.webkitEnterFullscreen" in js
jsfile.write_text(js,encoding="utf-8")
print("Video controls moved inside portrait video: play/pause, time, progress, mute, fullscreen and exit.")
