import argparse, shutil, subprocess, sys
from config import OUT, CACHE
from scenes import render_video
from narration import make_narration
from audio_generator import make_music_and_sfx
from audio_mixer import mix_audio
from subtitles import make_srt
from video_assembler import assemble, validate

def have(cmd): return shutil.which(cmd) is not None
def main():
    p=argparse.ArgumentParser(description="Generate a 4:55 OpenAI and AI agents explainer")
    p.add_argument("--quality",choices=["preview","final"],default="preview")
    p.add_argument("--force",action="store_true",help="Regenerate cached assets")
    a=p.parse_args()
    OUT.mkdir(exist_ok=True); CACHE.mkdir(exist_ok=True)
    if not have("ffmpeg") or not have("ffprobe"):
        sys.exit("ERROR: ffmpeg and ffprobe must be installed and available on PATH.")
    if a.force:
        shutil.rmtree(CACHE,ignore_errors=True); CACHE.mkdir(exist_ok=True)
    try:
        narration=make_narration()
        music,sfx=make_music_and_sfx()
        mix_audio(narration,music,sfx)
        make_srt()
        render_video(a.quality)
        assemble(a.quality)
        validate()
        print("\\nSUCCESS: output/openai_ai_future.mp4")
    except Exception as e:
        print(f"ERROR: {e}",file=sys.stderr); raise
if __name__=="__main__": main()
