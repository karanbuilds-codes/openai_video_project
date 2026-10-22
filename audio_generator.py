import wave, numpy as np
import shutil, subprocess
from config import OUT, CACHE, DURATION, MUSIC_SOURCE
SR=44100
def save_wav(path, data, sr=SR):
    data=np.asarray(data,dtype=np.float32)
    peak=max(float(np.max(np.abs(data))),1e-8); data=np.clip(data/ max(1.0,peak/0.92),-1,1)
    pcm=(data*32767).astype(np.int16)
    with wave.open(str(path),"wb") as w:
        w.setnchannels(2 if pcm.ndim==2 else 1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
def make_music_and_sfx():
    OUT.mkdir(exist_ok=True); CACHE.mkdir(exist_ok=True)
    music=OUT/"music.wav"; sfx=OUT/"sfx.wav"
    has_music_source=MUSIC_SOURCE.is_file()
    if has_music_source:
        ff=shutil.which("ffmpeg")
        if not ff: raise RuntimeError("FFmpeg not found.")
        fade_out=max(0,DURATION-5)
        subprocess.run(
            [ff,"-y","-i",str(MUSIC_SOURCE),"-af",
             f"aresample={SR},aformat=sample_fmts=s16:channel_layouts=stereo,"
             f"afade=t=in:st=0:d=2,afade=t=out:st={fade_out}:d=5,apad,atrim=0:{DURATION}",
             "-ar",str(SR),"-ac","2",str(music)],
            check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if sfx.exists(): return music,sfx
    elif music.exists() and sfx.exists(): return music,sfx
    n=int(SR*DURATION); t=np.arange(n,dtype=np.float32)/SR
    if not has_music_source:
        # Procedural ambient fallback for projects without a configured music source.
        left=np.zeros(n,np.float32); right=np.zeros(n,np.float32)
        for i,f in enumerate([55.0,82.41,110.0,164.81,220.0]):
            env=0.18+0.10*np.sin(2*np.pi*t/(37+i*4)+i)
            tone=np.sin(2*np.pi*f*t + 0.18*np.sin(2*np.pi*0.07*t+i))
            left += (0.018/(i+1))*tone*env
            right += (0.018/(i+1))*np.sin(2*np.pi*f*1.003*t+0.7)*env
        pulse=(np.maximum(0,np.sin(2*np.pi*0.5*t))**6)*0.012
        left+=pulse*np.sin(2*np.pi*110*t); right+=pulse*np.sin(2*np.pi*113*t)
        # Chapter lifts and a soft final resolution.
        lift=np.interp(t,[0,40,120,205,245,285,295],[0.4,0.65,0.8,1.0,0.7,0.9,0.0])
        left*=lift; right*=lift
        fade=np.minimum(1,t/2)*np.minimum(1,(DURATION-t)/5).clip(0,1)
        save_wav(music,np.column_stack([left*fade,right*fade])*8.0)
    # Effects are deliberately tied to scene starts and agent workflow events.
    fx=np.zeros((n,2),np.float32)
    rng=np.random.default_rng(22)
    events=[(0,"impact"),(15,"click"),(40,"pulse"),(70,"sweep"),(95,"confirm"),
            (120,"pulse"),(132,"click"),(140,"click"),(150,"notify"),(160,"sweep"),
            (171,"confirm"),(180,"sweep"),(205,"rise"),(245,"tension"),(255,"confirm"),(290,"ping")]
    for sec,kind in events:
        start=int(sec*SR); dur=2.0 if kind in ("impact","rise","tension") else 0.45
        m=min(int(dur*SR),n-start)
        if m<=0: continue
        x=np.arange(m)/SR; env=np.exp(-x*(2.4 if kind in ("rise","sweep") else 7))
        if kind=="impact": sig=np.sin(2*np.pi*(48+70*np.exp(-x*5))*x)*env*0.23
        elif kind=="click": sig=(rng.normal(0,1,m)*np.exp(-x*35))*0.10
        elif kind=="notify" or kind=="confirm" or kind=="ping": sig=(np.sin(2*np.pi*880*x)+.5*np.sin(2*np.pi*1320*x))*env*.06
        elif kind=="sweep" or kind=="rise": sig=np.sin(2*np.pi*(180+400*x)*x)*env*.06
        elif kind=="tension": sig=np.sin(2*np.pi*73*x)*env*.08
        else: sig=np.sin(2*np.pi*150*x)*env*.05
        pan=np.linspace(-0.7,0.7,m)
        fx[start:start+m,0]+=sig*(1-pan)*0.5
        fx[start:start+m,1]+=sig*(1+pan)*0.5
    save_wav(sfx,fx)
    return music,sfx
