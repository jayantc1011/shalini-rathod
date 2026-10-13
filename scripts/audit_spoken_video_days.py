from pathlib import Path
import json,re,subprocess,sys,os,wave
import numpy as np
from faster_whisper import WhisperModel
from pypdf import PdfReader

root=Path(sys.argv[1])
s=(root/"courses-data.js").read_text(encoding="utf-8")
data=json.loads(s.split("window.SHALINI_COURSES =",1)[1].strip().rstrip(";"))
lessons=[l for m in data["speakathon"]["modules"] for l in m["lessons"]]
assert len(lessons)==21
print("SOURCE CURRICULUM AND PDF")
for i,l in enumerate(lessons,1):
 pdf=root/f"assets/lms/pdfs/day-{i:02d}.pdf"
 try:
  reader=PdfReader(str(pdf))
  preview=" ".join((reader.pages[0].extract_text() or "").split())[:360]
 except Exception as exc:preview="PDF TEXT ERROR "+str(exc)
 print(json.dumps({"day":i,"title":l.get("title"),"summary":l.get("summary"),"practice":l.get("practice"),"local_pdf":str(pdf.relative_to(root)),"pdf_first_page":preview},ensure_ascii=False))
print("VIDEO INTRO TRANSCRIPTS")
model=WhisperModel("tiny.en",device="cpu",compute_type="int8",cpu_threads=4)
folder=root/"assets/lms/videos"
for day in [1,2,3,8,9,10,11,15]:
 mp4=folder/f"day-{day:02d}.mp4"
 if not mp4.exists():continue
 audio=Path("/tmp/intro-audio.wav")
 subprocess.run(["ffmpeg","-y","-nostdin","-v","error","-ss","0","-t","115","-i",str(mp4),"-ar","16000","-ac","1",str(audio)],check=True)
 with wave.open(str(audio),"rb") as wav:
  assert wav.getframerate()==16000 and wav.getnchannels()==1 and wav.getsampwidth()==2
  pcm=np.frombuffer(wav.readframes(wav.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
 chunks,info=model.transcribe(pcm,language="en",beam_size=2,vad_filter=True,condition_on_previous_text=False)
 utterances=[{"start":round(seg.start,1),"text":seg.text.strip()} for seg in chunks]
 print(json.dumps({"day":day,"mp4":mp4.name,"intro_115s":utterances},ensure_ascii=False))
 print("DONE DAY",day,flush=True)
