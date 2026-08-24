import os
import sys

from dotenv import load_dotenv

from src.hotkey import setup_hotkey, register_start_callback, register_stop_callback
from src.audio import start_recording, stop_recording
from src.typer import type_text
from src.overlay import Overlay

# Load environment variables from .env
load_dotenv()

# Try to initialize OpenAI Client (optional for Phase 1)
client = None
try:
    from openai import OpenAI
    client = OpenAI()  # Reads OPENAI_API_KEY from environment
    print("[+] OpenAI API connected. AI transcription enabled.")
except Exception:
    print("[!] No OpenAI API key found. Running in DEMO MODE (no AI transcription).")
    print("[!] To enable AI, create a .env file with: OPENAI_API_KEY=your_key_here")

HOTKEY = 'ctrl+shift+space'
overlay_instance = None

CLEANUP_PROMPT = (
    "You are an expert transcriptionist and editor. "
    "Clean up the following raw transcription: remove filler words (like 'um', 'uh', 'like'), "
    "fix false starts or stutters, and format the output as natural, written text. "
    "Output ONLY the final cleaned text and nothing else. No markdown formatting."
)

def process_audio(filename):
    """Sends the audio to OpenAI Whisper for STT, then to an LLM for cleanup."""
    if not client:
        print("[*] Demo mode: skipping AI transcription.")
        return "Hello from GlintVoice! (demo mode - no API key)"

    print("[*] Transcribing audio with Whisper...")
    try:
        # Step 1: Speech-to-Text via Whisper
        with open(filename, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        raw_text = transcript.text
        print(f"[*] Raw transcript: {raw_text}")

        # Step 2: Cleanup via LLM
        print("[*] Cleaning up with LLM...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CLEANUP_PROMPT},
                {"role": "user", "content": raw_text}
            ]
        )
        cleaned_text = response.choices[0].message.content.strip()
        print(f"\n[+] Final Text: {cleaned_text}\n")
        return cleaned_text

    except Exception as e:
        print(f"[!] Error during processing: {e}")
        return None

def start_recording_action():
    if overlay_instance:
        overlay_instance.trigger_start_ripple()
    start_recording()

def stop_recording_action():
    if overlay_instance:
        overlay_instance.trigger_stop_ripple()

    print("[*] Processing... please wait.")

    temp_file = stop_recording()

    if not temp_file:
        print("[!] No audio recorded.")
        return

    text = process_audio(temp_file)

    if text:
        type_text(text)
        try:
            os.remove(temp_file)
        except:
            pass

def main():
    global overlay_instance
    print("=========================================")
    print("          GlintVoice")
    print("=========================================")

    # Initialize the transparent overlay
    overlay_instance = Overlay()

    # Register callbacks for the hotkey events
    register_start_callback(start_recording_action)
    register_stop_callback(stop_recording_action)

    # Setup the global hotkey
    setup_hotkey(HOTKEY)

    print(f"[*] Hotkey listener active. Try pressing: {HOTKEY}")
    print("[*] Overlay active. Close the terminal window to exit.")

    # Block the main thread with Tkinter's event loop
    try:
        overlay_instance.run()
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
