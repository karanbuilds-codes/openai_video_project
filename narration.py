import subprocess, shutil, wave
from pathlib import Path
import numpy as np
from config import OUT, CACHE, NARRATION, SCENES, DURATION
def make_narration():
    CACHE.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
    final=OUT/"narration.wav"
    if final.exists(): return final
    piper=shutil.which("piper")
    model=__import__("os").environ.get("PIPER_MODEL")
    pieces=[]
    if piper and model:
        for i,text in enumerate(NARRATION):
            f=CACHE/f"voice_{i:02d}.wav"
            subprocess.run([piper,"--model",model,"--output_file",str(f)],input=text.encode(),check=True)
            pieces.append(f)
    else:
        try: import pyttsx3
        except ImportError as e: raise RuntimeError("Install requirements or configure Piper TTS.") from e
        engine=pyttsx3.init()
        engine.setProperty("rate", 165); engine.setProperty("volume", 1.0)
        for i,text in enumerate(NARRATION):
            f=CACHE/f"voice_{i:02d}.wav"
            engine.save_to_file(text,str(f))
            pieces.append(f)
        engine.runAndWait()
        for f in pieces:
            if not f.exists() or f.stat().st_size < 1000:
                raise RuntimeError("Local TTS did not create audio. Install eSpeak NG or configure Piper.")
    # Place each scene's narration at its storyboard start; time-compress only when needed.
    ff=shutil.which("ffmpeg")
    aligned=[]
    for i,(f,scene) in enumerate(zip(pieces,SCENES)):
        start,end=scene[0],scene[1]
        with wave.open(str(f),"rb") as w: dur=w.getnframes()/w.getframerate()
        target=max(2.0,end-start-0.8)
        use=f
        if dur>target:
            rate=min(2.0,dur/target)
            use=CACHE/f"voice_fit_{i:02d}.wav"
            subprocess.run([ff,"-y","-i",str(f),"-filter:a",f"atempo={rate:.5f}","-ac","1",str(use)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        aligned.append((start,use))
    sr=44100; total=int(DURATION*sr); mix=np.zeros(total,dtype=np.float32)
    for start,f in aligned:
        with wave.open(str(f),"rb") as w:
            rate=w.getframerate(); raw=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
        if rate!=sr:
            old=np.arange(len(raw))/rate; new=np.arange(int(len(raw)*sr/rate))/sr
            raw=np.interp(new,old,raw).astype(np.float32)
        pos=int(start*sr); n=min(len(raw),total-pos)
        if n>0: mix[pos:pos+n]+=raw[:n]
    mix=np.clip(mix*0.88,-1,1)
    with wave.open(str(final),"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix*32767).astype(np.int16).tobytes())
    return final
