import keyboard

# Global state
is_recording = False
hotkey_combination = 'ctrl+shift+space'

# Callback lists so other modules can subscribe to hotkey events
_start_callbacks = []
_stop_callbacks = []

def register_start_callback(callback):
    """Registers a function to be called when recording starts."""
    _start_callbacks.append(callback)

def register_stop_callback(callback):
    """Registers a function to be called when recording stops."""
    _stop_callbacks.append(callback)

def _toggle_recording():
    global is_recording
    
    if not is_recording:
        is_recording = True
        print("[*] Recording started")
        for cb in _start_callbacks:
            try:
                cb()
            except Exception as e:
                print(f"[!] Error in start callback: {e}")
    else:
        is_recording = False
        print("[*] Recording stopped")
        for cb in _stop_callbacks:
            try:
                cb()
            except Exception as e:
                print(f"[!] Error in stop callback: {e}")

def setup_hotkey(custom_hotkey=None):
    """Sets up the global hotkey listener."""
    global hotkey_combination
    if custom_hotkey:
        hotkey_combination = custom_hotkey
        
    print(f"[*] Registering global hotkey: {hotkey_combination}")
    keyboard.add_hotkey(hotkey_combination, _toggle_recording)

def wait_for_exit():
    """Blocks the main thread until the user exits (useful for testing)."""
    try:
        print(f"[*] Hotkey listener active. Try pressing: {hotkey_combination}")
        print("[*] Press Ctrl+C in this terminal to exit.")
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n[*] Exiting...")

if __name__ == "__main__":
    # Test script when run directly
    setup_hotkey()
    wait_for_exit()
