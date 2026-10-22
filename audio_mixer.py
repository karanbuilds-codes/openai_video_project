import subprocess, shutil
from pathlib import Path
from config import OUT, DURATION
def mix_audio(narration,music,sfx):
    ff=shutil.which("ffmpeg")
    if not ff: raise RuntimeError("FFmpeg not found.")
    out=OUT/"final_audio.wav"
    # narration centered; music ducked under speech; sfx mixed at low level.
    cmd=[ff,"-y","-i",str(music),"-i",str(narration),"-i",str(sfx),
         "-filter_complex",
         f"[0:a]volume=0.8,afade=t=in:st=0:d=2,afade=t=out:st={DURATION-5}:d=5[m];"
         "[1:a]adelay=0|0,loudnorm=I=-18:TP=-2:LRA=7,apad,asplit=2[nside][nvoice];"
         "[2:a]volume=0.65[e];"
         "[m][nside]sidechaincompress=threshold=0.025:ratio=5:attack=20:release=500[duck];"
         "[duck][nvoice][e]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.93,apad,atrim=0:295[a]",
         "-map","[a]","-ar","44100","-ac","2",str(out)]
    subprocess.run(cmd,check=True)
    return out
