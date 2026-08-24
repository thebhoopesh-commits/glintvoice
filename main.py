import os
import sys

from dotenv import load_dotenv

from src.hotkey import setup_hotkey, register_start_callback, register_stop_callback
from src.audio import start_recording, stop_recording
from src.typer import type_text
from src.overlay import Overlay

# Load environment variables from .env
load_dotenv()

# Try to initialize Gemini Client (optional for Phase 1)
client = None
try:
    from google import genai
    client = genai.Client()
    print("[+] Gemini API connected. AI transcription enabled.")
except Exception:
    print("[!] No Gemini API key found. Running in DEMO MODE (no AI transcription).")
    print("[!] To enable AI, create a .env file with: GEMINI_API_KEY=your_key_here")

HOTKEY = 'ctrl+shift+space'
overlay_instance = None

def process_audio(filename):
    """Sends the audio to Gemini for transcription and processing."""
    if not client:
        # Demo mode: no API key, just return a placeholder
        print("[*] Demo mode: skipping AI transcription.")
        return "Hello from GlintVoice! (demo mode - no API key)"
    
    print(f"[*] Processing audio with Gemini...")
    try:
        audio_file = client.files.upload(file=filename, config={'display_name': 'Dictation'})
        prompt = (
            "You are an expert transcriptionist and editor. "
            "Listen to the following audio and transcribe it perfectly. "
            "Clean up the transcription: remove filler words (like 'um', 'uh', 'like'), "
            "fix false starts or stutters, and format the output as natural, written text. "
            "Output ONLY the final cleaned text and nothing else. No markdown formatting."
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[audio_file, prompt]
        )
        
        cleaned_text = response.text.strip()
        print(f"\n[+] Final Text: {cleaned_text}\n")
        
        client.files.delete(name=audio_file.name)
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
