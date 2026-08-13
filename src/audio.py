import os
import queue
import tempfile
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
CHANNELS = 1

_is_recording = False
_audio_queue = queue.Queue()
_recording_thread = None

def _record_loop():
    """Continuously reads audio from the microphone into the queue."""
    global _is_recording
    
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32') as stream:
            while _is_recording:
                # Read a small chunk of audio
                data, overflowed = stream.read(1024)
                if overflowed:
                    print("[!] Audio buffer overflow")
                _audio_queue.put(data)
    except Exception as e:
        print(f"[!] Error accessing microphone: {e}")

def start_recording():
    """Starts the audio recording in a background thread."""
    global _is_recording, _recording_thread, _audio_queue
    
    if _is_recording:
        return
        
    _is_recording = True
    _audio_queue = queue.Queue() # Reset queue
    _recording_thread = threading.Thread(target=_record_loop, daemon=True)
    _recording_thread.start()

def stop_recording() -> str:
    """
    Stops the recording, saves the buffered audio to a temporary WAV file, 
    and returns the path to the WAV file.
    Returns None if no audio was recorded.
    """
    global _is_recording, _recording_thread, _audio_queue
    
    if not _is_recording:
        return None
        
    _is_recording = False
    if _recording_thread:
        _recording_thread.join(timeout=1.0)
        
    audio_data = []
    while not _audio_queue.empty():
        audio_data.append(_audio_queue.get())
        
    if not audio_data:
        return None
        
    # Flatten the list of arrays into one continuous array
    audio_data = np.concatenate(audio_data, axis=0)
    
    # Generate temporary file path
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, 'wispr_dictation.wav')
    
    # Save to WAV
    sf.write(temp_file, audio_data, SAMPLE_RATE)
    
    return temp_file
