# J.A.R.V.I.S. - Personal AI Assistant

A futuristic Windows desktop assistant built in Python with:
- Python + PyQt6 dashboard UI
- local AI-first approach
- speech-to-text and text-to-speech
- PC automation and command execution
- YouTube automation pipeline
- image, video, and 3D generation readiness

## Current build status

This project is currently in the working assistant phase:
- dashboard UI shell is live
- assistant controller is wired up
- command executor handles core PC actions
- system monitor checks local environment readiness
- local AI validation is built in

## Tech stack

- Python 3.11+
- PyQt6
- Ollama for local AI
- SpeechRecognition + pyttsx3
- PyAutoGUI + subprocess-based Windows automation
- Blender-ready 3D generation workflow

## Install

1. Create a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Start Ollama locally if you want local AI features
   ```bash
   ollama run mistral
   ```

## Run

```bash
python main.py
```

## Features in development

- Voice recognition and speech output
- AI command processing
- Windows automation commands
- YouTube workflow automation
- image generation pipeline
- video generation pipeline
- Blender-based 3D model generation
- self-improving assistant loops

## Notes

This is being built in phases. The current milestone is a working assistant shell with dashboard UI and command control.
