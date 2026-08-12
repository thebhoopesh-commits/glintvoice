import os
import queue
import sys
import tempfile
import threading
import time

import numpy as np
import pyautogui
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from google import genai

from src.hotkey import setup_hotkey, wait_for_exit, register_start_callback, register_stop_callback

# Load environment variables from .env
load_dotenv()

# Initialize Gemini Client
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please make sure you have a valid GEMINI_API_KEY set in your .env file.")
    sys.exit(1)

# Configuration
HOTKEY = 'ctrl+shift+space'
SAMPLE_RATE = 16000
CHANNELS = 1

# Global state for audio
is_recording = False
audio_queue = queue.Queue()
recording_thread = None

def record_audio():
    """Records audio continuously until stopped."""
    global is_recording
    
    print(f"[*] Recording started... Speak now!")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32') as stream:
        while is_recording:
            # Read a small chunk of audio
            data, overflowed = stream.read(1024)
            audio_queue.put(data)

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
    global is_recording, recording_thread, audio_queue
    is_recording = True
    audio_queue = queue.Queue()
    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()

def stop_recording_action():
    global is_recording, recording_thread, audio_queue
    is_recording = False
    
    print("[*] Processing... please wait.")
    if recording_thread:
        recording_thread.join()
        
    audio_data = []
    while not audio_queue.empty():
        audio_data.append(audio_queue.get())
    
    if not audio_data:
        print("[!] No audio recorded.")
        return
        
    audio_data = np.concatenate(audio_data, axis=0)
    
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, 'wispr_dictation.wav')
    
    sf.write(temp_file, audio_data, SAMPLE_RATE)
    
    text = process_audio(temp_file)
    
    if text:
        print("[*] Typing...")
        time.sleep(0.1)
        pyautogui.write(text)
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
