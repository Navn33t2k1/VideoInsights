import os
import tempfile
import subprocess
import shutil
from yt_dlp import YoutubeDL
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# DOWNLOAD VIDEO (Universal)

def download_video(url):
    temp_dir = tempfile.mkdtemp()
    out_template = os.path.join(temp_dir, "video.%(ext)s")

    ydl_opts = {
        "format": "best",
        "outtmpl": out_template,
        "quiet": True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        shutil.rmtree(temp_dir)
        raise Exception(f"Video download failed: {e}")

    # Find downloaded video
    for f in os.listdir(temp_dir):
        if f.lower().endswith((".mp4", ".mkv", ".mov", ".webm")):
            return os.path.join(temp_dir, f)

    raise Exception("Downloaded video file not found.")

# EXTRACT AUDIO (FFmpeg)

def extract_audio(video_path):
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "mp3", audio_file]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise Exception("Audio extraction failed:\n" + proc.stderr.decode())

    return audio_file


# TRANSCRIBE AUDIO

def transcribe(audio_path):
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return result.text


#  ANALYZE COMMUNICATION

def analyze_text(transcript):
    prompt = f"""
You are a communication analysis engine.

Provide output in JSON with keys:
- clarity: a score from 0-100 based on fluency, grammar, pace.
- focus: one sentence summarizing the main topic.

Transcript:
{transcript}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    content = response.choices[0].message.content.strip()

    import json, re
    json_text = re.search(r"{.*}", content, flags=re.DOTALL)

    if not json_text:
        return {"clarity": 75, "focus": "Not found"}

    return json.loads(json_text.group(0))

# MASTER PIPELINE

def process_video(url):
    video = download_video(url)
    audio = extract_audio(video)
    transcript = transcribe(audio)
    metrics = analyze_text(transcript)

    return {
        "clarity": metrics["clarity"],
        "focus": metrics["focus"],
        "transcript": transcript
    }
