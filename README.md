# GlintVoice

An open-source, AI-powered natural dictation tool. This application allows you to dictate text globally across any application, using AI to clean up rambling speech, fix formatting, and write out text as if it were typed naturally.

## Features (Proposed)
- **Global Hotkey:** Press `Ctrl+Shift+Space` to start and stop dictation from anywhere.
- **AI Text Processing:** Uses large language models to remove filler words and format sentences.
- **Universal Typing:** Automatically types the processed text into your active window.

## Setup Instructions
1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt` (dependencies include sounddevice, keyboard, pyautogui, google-genai, etc.)
5. Create a `.env` file and add your API keys (e.g., `GEMINI_API_KEY=your_key_here`).
6. Run the application: `python main.py`
