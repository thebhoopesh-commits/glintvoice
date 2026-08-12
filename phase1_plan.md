# Phase 1: Walking Skeleton — Implementation Plan

## Goal
Prove that all core OS-level mechanics work independently before introducing any AI. By the end of Phase 1, pressing a hotkey should record your voice, and pressing it again should type a hardcoded string into your active window — with a visual ripple animation confirming each action.

No AI, no transcription, no cleanup. Just the plumbing.

---

## Prerequisites
- Python 3.10+ installed
- A working microphone
- Windows 10/11

---

## Step-by-Step Breakdown

### Step 1.1 — Project Scaffolding
**Goal:** Set up the project structure, virtual environment, and install all dependencies.

```
glintvoice/
├── src/
│   ├── __init__.py
│   ├── hotkey.py          # Global hotkey listener
│   ├── audio.py           # Microphone recording
│   ├── typer.py           # Keystroke simulation
│   └── overlay.py         # Transparent overlay (ripple animation)
├── main.py                # Entry point — wires everything together
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

**Tasks:**
- [ ] Create `src/` directory and empty module files
- [ ] Create virtual environment and install dependencies
- [ ] Verify all imports work with a simple test script

**Commit:** `chore: scaffolded project structure and installed dependencies`

---

### Step 1.2 — Global Hotkey Listener (`src/hotkey.py`)
**Goal:** Listen for `Ctrl+Shift+Space` globally. When pressed, print "Recording started" to the console. When pressed again, print "Recording stopped."

**Tasks:**
- [ ] Implement a toggle function using the `keyboard` library
- [ ] Register the hotkey with `keyboard.add_hotkey()`
- [ ] Maintain a boolean `is_recording` state that flips on each press
- [ ] Print state changes to the console for verification

**How to test:** Run the script. Open Notepad. Press `Ctrl+Shift+Space`. Check the terminal — it should print "Recording started." Press again — "Recording stopped."

**Commit:** `feat: global hotkey toggle listener (Ctrl+Shift+Space)`

---

### Step 1.3 — Microphone Audio Capture (`src/audio.py`)
**Goal:** When recording starts, capture audio from the default microphone into a numpy buffer. When recording stops, save it to a temporary `.wav` file.

**Tasks:**
- [ ] Use `sounddevice.InputStream` to capture audio at 16kHz, mono
- [ ] Store incoming audio chunks in a `queue.Queue` on a background thread
- [ ] On stop, concatenate all chunks and write to a `.wav` file using `soundfile`
- [ ] Print the file path and duration to the console

**How to test:** Run the script. Press the hotkey, speak for 3 seconds, press the hotkey again. Check the printed file path. Open the `.wav` in any media player and verify your voice was captured clearly.

**Commit:** `feat: microphone audio capture to WAV file`

---

### Step 1.4 — Keystroke Simulation (`src/typer.py`)
**Goal:** After recording stops, simulate typing a hardcoded string ("Hello from GlintVoice!") into whatever window is currently focused.

**Tasks:**
- [ ] Use `pyautogui.write()` or `pyautogui.typewrite()` to simulate keystrokes
- [ ] Add a configurable `typing_speed` interval (default: 0.02s per character)
- [ ] Handle edge cases: what if no text field is focused? (Graceful failure with a console warning)
- [ ] Add a small delay (~200ms) after recording stops before typing begins, to give the user time to click into the target window if needed

**How to test:** Run the script. Open Notepad. Press the hotkey, say anything (audio is captured but ignored for now), press the hotkey again. "Hello from GlintVoice!" should appear typed out in Notepad.

**Commit:** `feat: auto-typing into active window via keystroke simulation`

---

### Step 1.5 — Transparent Overlay: Ripple Animation (`src/overlay.py`)
**Goal:** When the hotkey is pressed, a subtle ripple animation appears at the current cursor position on a transparent, click-through overlay window.

**Tasks:**
- [ ] Create a fullscreen, transparent, always-on-top, click-through window using `tkinter` (simplest for Phase 1; will migrate to Tauri later)
- [ ] On hotkey press (recording start): draw an expanding circle at the mouse cursor position that fades out over ~300ms
- [ ] On hotkey press (recording stop): draw a second ripple in a different color (e.g., amber)
- [ ] Ensure the overlay does NOT steal focus from the active application
- [ ] Ensure all mouse clicks pass through the overlay to the app beneath

**How to test:** Open Notepad and position your cursor. Press the hotkey — a ripple should appear at the cursor and fade. Notepad should remain focused the entire time.

**Commit:** `feat: transparent overlay with ripple animation on hotkey`

---

### Step 1.6 — Wire Everything Together (`main.py`)
**Goal:** Connect all four modules into a single entry point. The full flow should be:

```
Hotkey pressed → Ripple animation → Audio recording starts
Hotkey pressed again → Ripple animation → Audio recording stops → WAV saved → Hardcoded text typed out
```

**Tasks:**
- [ ] Import and initialize all modules in `main.py`
- [ ] Wire the hotkey callback to trigger audio + overlay simultaneously
- [ ] Add a startup banner in the terminal showing the hotkey, version, and status
- [ ] Add graceful shutdown on `Ctrl+C`

**How to test:** Full end-to-end test:
1. Run `python main.py`
2. Open Notepad
3. Press `Ctrl+Shift+Space` → see ripple, terminal says "Recording started"
4. Speak for a few seconds
5. Press `Ctrl+Shift+Space` → see ripple, terminal says "Recording stopped"
6. "Hello from GlintVoice!" appears typed in Notepad
7. Check that the `.wav` file was saved correctly

**Commit:** `feat: wired walking skeleton — hotkey, audio, typing, and overlay connected`

---

## Phase 1 Milestone

After all 6 steps are committed, you tag this as:

```bash
git tag -a v0.1.0-skeleton -m "Phase 1 complete: Walking skeleton with hotkey, audio capture, auto-typing, and ripple overlay"
git push origin v0.1.0-skeleton
```

**What you have:** A working proof that all OS-level plumbing functions correctly.
**What you don't have yet:** Any AI. That comes in Phase 2.

---

## Commit History After Phase 1

```
f4cd2ac  Initial commit: Added project documentation, PRD, and baseline script
75f596b  docs: redesigned UI with Zero UI philosophy
xxxxxxx  chore: scaffolded project structure and installed dependencies
xxxxxxx  feat: global hotkey toggle listener (Ctrl+Shift+Space)
xxxxxxx  feat: microphone audio capture to WAV file
xxxxxxx  feat: auto-typing into active window via keystroke simulation
xxxxxxx  feat: transparent overlay with ripple animation on hotkey
xxxxxxx  feat: wired walking skeleton — hotkey, audio, typing, and overlay connected
         → TAG: v0.1.0-skeleton
```
