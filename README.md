# Video Communication Insights App

A Python + Streamlit app that extracts communication metrics from any public video URL.

## Features
- Accepts YouTube, Loom, Vimeo, MP4 links
- Extracts audio using FFmpeg
- Transcribes using OpenAI Whisper
- Analyzes clarity + communication focus via LLM

## Setup
pip install -r requirements.txt

Set your API key:
export OPENAI_API_KEY="your_key"

Run:
streamlit run app.py
