# 🎧 Real-Time Voice Translator

A **real-time voice translator** built using Python, OpenAI's Whisper model, and Google Text-to-Speech. Speak in one language, see it transcribed and translated, and hear the translated speech — all in a user-friendly desktop app.

## 🛠 Features

- 🎤 Real-time voice input using your microphone
- 🧠 Speech-to-text with [Whisper Large V3](https://huggingface.co/openai/whisper-large-v3)
- 🌍 Translation using Bing via `translators` Python package
- 🔊 Voice playback using `gTTS` and `playsound`
- 🪟 Intuitive Tkinter-based GUI
- 🗣️ Supports 13 languages including English, Hindi, Spanish, French, Japanese, Tamil, and more

## 📦 Requirements

- Python 3.8+
- GPU (optional but recommended for Whisper speed)

### Python Libraries

```bash
pip install -r requirements.txt
```

## 🧩 Model & Pipeline

The app uses Hugging Face's pipeline:
- Model: `openai/whisper-large-v3`
- Device: CUDA if available, fallback to CPU
- Translation: `translators` (using Bing API)
- TTS: `gTTS` (Google Text-to-Speech)

## 🚀 How to Run

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/real-time-voice-translator.git
cd real-time-voice-translator
```

2. **Install Requirements**

```bash
pip install -r requirements.txt
```

3. **Add App Icon**

Place an image named `icon.png` in the project directory (or replace it with your custom icon).

4. **Run the App**

```bash
python main.py
```

## 🌐 Supported Languages

| Language  | Code |
|-----------|------|
| English   | en   |
| Hindi     | hi   |
| Bengali   | bn   |
| Spanish   | es   |
| Russian   | ru   |
| Japanese  | ja   |
| Korean    | ko   |
| German    | de   |
| French    | fr   |
| Tamil     | ta   |
| Telugu    | te   |
| Gujarati  | gu   |
| Punjabi   | pa   |

## 📸 GUI Overview

- 🗣 Input your speech via microphone
- 📜 Recognized text is displayed on the left
- 🌐 Translated text (with audio playback) appears on the right
- ▶ Start, 🛌 Stop, and 🪹 Clear buttons included

## 🧠 Notes

- Internet connection required for `gTTS` and `translators` libraries.
- Use a quiet environment for better speech recognition accuracy.
- Whisper model download may take a while the first time (~2.9 GB).

## ⚠️ Troubleshooting

- **No sound?** Ensure your system audio is working. Try opening `voice.mp3` manually.
- **Slow performance?** Consider using a smaller Whisper model or enable GPU.
- **Translators API fails?** Bing API usage may be limited or blocked in some regions. Try switching translator services (e.g., Google, Deepl if supported).