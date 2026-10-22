import subprocess, shutil, json
from config import OUT, CACHE, DURATION, FPS, WIDTH, HEIGHT
def assemble(quality):
    ff=shutil.which("ffmpeg")
    frames=CACHE/f"frames_{quality}"
    scale="1920:1080" if quality=="final" else "960:540"
    vf=f"scale={scale}:flags=lanczos,fps={FPS},format=yuv420p"
    cmd=[ff,"-y","-framerate",str(FPS),"-i",str(frames/"frame_%06d.png"),
         "-i",str(OUT/"final_audio.wav"),"-vf",vf,"-t",str(DURATION),
         "-c:v","libx264","-preset","medium" if quality=="final" else "ultrafast",
         "-crf","19" if quality=="final" else "25","-c:a","aac","-b:a","192k",
         "-movflags","+faststart",str(OUT/"openai_ai_future.mp4")]
    subprocess.run(cmd,check=True)
def validate():
    ff=shutil.which("ffmpeg")
    ffprobe=shutil.which("ffprobe")
    video=OUT/"openai_ai_future.mp4"
    p=subprocess.run([ffprobe,"-v","error","-show_entries","format=duration:stream=codec_type,width,height,r_frame_rate,codec_name","-of","json",str(video)],capture_output=True,text=True,check=True)
    info=json.loads(p.stdout); dur=float(info["format"]["duration"])
    if dur>300.05: raise RuntimeError(f"Duration validation failed: {dur:.2f}s")
    streams=info.get("streams",[])
    if not any(s.get("codec_type")=="audio" for s in streams): raise RuntimeError("No audio stream found.")
    if not any(s.get("codec_type")=="video" for s in streams): raise RuntimeError("No video stream found.")
    audio_check=subprocess.run([ff,"-v","error","-i",str(video),"-map","0:a:0","-f","null","-"],capture_output=True,text=True)
    if audio_check.returncode:
        raise RuntimeError(f"Audio stream could not be decoded: {audio_check.stderr.strip()}")
    print("FFprobe validation:",json.dumps({"duration_seconds":round(dur,3),"streams":streams},indent=2))
