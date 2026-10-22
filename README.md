# OpenAI & Artificial Intelligence: From Zero to the Future

A code-generated 4:55 educational video project. The portable pipeline creates animated procedural visuals, local English narration, synthesized electronic ambience and timed effects, SRT subtitles, and an H.264/AAC MP4. It does **not** perform live research; the AI-agent chapter is explicitly simulated.

## Important implementation note
HTML itself does not expose Blender's `bpy` API. This project therefore uses Python for rendering/audio/assembly and includes `blender_renderer.py` as an optional Blender procedural 3D scene builder. The default renderer is a portable procedural 2D/2.5D renderer with moving particles, network links, scene-specific diagrams, and cinematic vignette. This keeps the full pipeline runnable without Blender. It is not a claim of feature-film-quality true 3D.

## Requirements
- Python 3.10+
- FFmpeg and FFprobe installed and available on `PATH`
- For local TTS: `pyttsx3` plus an installed system voice engine (eSpeak NG on Linux; Windows SAPI on Windows)
- Optional: Piper TTS executable and a compatible voice model; set `PIPER_MODEL` to the model file path.
- Optional Blender 3.6+ for `blender_renderer.py`

## Install
### Windows PowerShell
```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
ffmpeg -version
ffprobe -version
python main.py --quality preview
```
### macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
brew install ffmpeg
python main.py --quality preview
```
### Ubuntu / Debian
```bash
sudo apt update
sudo apt install ffmpeg espeak-ng python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --quality preview
```

## Render commands
```bash
python main.py --quality preview
python main.py --quality final
python main.py --quality final --force
```
Preview renders at 960x540; final renders at 1920x1080, 30 FPS. Cached frames are reused on rerun within each quality setting, so completed frames are not rendered again. `--force` clears cached assets. The output is `output/openai_ai_future.mp4`; narration/music/effects and `output/subtitles.srt` are also saved.

After rendering, open `index.html` in a browser for the video player with a volume slider and maximize/fullscreen control.

## Quality and runtime
The project uses FFprobe to validate the final file's duration and audio/video streams. Full-HD generation creates 8,850 frames and can require substantial disk space and render time. The current source was generated as a project bundle here; the MP4 itself has **not** been rendered or validated in this environment. Run the preview first, then final. If local TTS is unavailable, configure Piper or install a system voice engine.

## Audio
The background music is `assets/openai_futuristic_background_music.wav`, converted to 44.1 kHz stereo and faded to fit the 4:55 video. Narration and synthesized effects are mixed with the music using FFmpeg sidechain compression and a limiter. If the music asset is unavailable, the pipeline generates a procedural ambient fallback.
