import time
import pyautogui

def type_text(text: str):
    """
    Simulates keystrokes to type the given text into the active window.
    """
    if not text:
        return
        
    print(f"[*] Typing text: {text}")
    
    # We add a tiny delay to ensure the OS has fully focused 
    # the target window after the user releases the hotkey
    time.sleep(0.1)
    
    # Use pyautogui to simulate typing
    pyautogui.write(text)
