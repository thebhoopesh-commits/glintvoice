import os
import sys

from dotenv import load_dotenv
from google import genai

from src.hotkey import setup_hotkey, wait_for_exit, register_start_callback, register_stop_callback
from src.audio import start_recording, stop_recording
from src.typer import type_text

# Load environment variables from .env
load_dotenv()

# Initialize Gemini Client
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please make sure you have a valid GEMINI_API_KEY set in your .env file.")
    sys.exit(1)

HOTKEY = 'ctrl+shift+space'

def process_audio(filename):
    """Sends the audio to Gemini for transcription and processing."""
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
    start_recording()

def stop_recording_action():
    print("[*] Processing... please wait.")
    
    # audio.py handles thread joining and returning the WAV file path
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
    print("=========================================")
    print("          GlintVoice")
    print("=========================================")
    
    # Register callbacks for the hotkey events
    register_start_callback(start_recording_action)
    register_stop_callback(stop_recording_action)
    
    # Setup the global hotkey
    setup_hotkey(HOTKEY)
    
    # Block and wait for exit
    wait_for_exit()

if __name__ == "__main__":
    main()
