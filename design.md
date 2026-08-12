# Design & User Experience (UX)

## 1. Design Philosophy: "Zero UI"

GlintVoice follows a radical design principle: **it has no permanent visual presence on screen.** When idle, it is completely invisible — zero pixels used, zero distraction. When active, it manifests *exactly where the user's eyes already are* — at the text cursor.

This is fundamentally different from every existing voice tool (Siri's orb, Copilot's sidebar, Dynamic Island's pill). Those all demand the user look *away* from their work. GlintVoice never does.

The goal: GlintVoice should feel less like a separate application and more like **your keyboard learned to listen.**

---

## 2. Visual Feedback System (Dictation Mode)

All visual feedback is rendered on an invisible, click-through, always-on-top transparent overlay window. The user never interacts with this window directly — it simply draws animations at the cursor position.

### State 1: Idle
- **Visual:** Nothing. Absolutely nothing on screen. GlintVoice is a background process with a system tray icon only.

### State 2: Activated (Hotkey Pressed — Recording Starts)
- **Visual:** A single, subtle **ripple animation** expands outward from the text cursor position and fades within ~300ms. Like dropping a stone in still water. This is the user's confirmation that recording has begun.
- **Audio Cue (Optional):** A very soft, short chime (< 100ms).

### State 3: Listening (User is Speaking)
- **Visual:** A thin (2-3px), animated **waveform underline** appears directly beneath the text cursor. It pulses and moves in sync with the user's voice amplitude. It follows the cursor if the user moves it.
- **Why:** The user never has to look at a corner or a widget. The feedback is exactly where the text will eventually appear.

### State 4: Processing (AI is Transcribing & Cleaning)
- **Visual:** The waveform underline dissolves. In its place, **ghost text** begins appearing at the cursor — semi-transparent, grey placeholder characters that shimmer subtly. This gives the user a sense that "something is being written" without committing final text yet.

### State 5: Done (Text is Typed Out)
- **Visual:** The ghost text rapidly solidifies from grey to full color, like **ink bleeding into paper**. The final, cleaned text is now typed into the active application. All visual elements vanish. GlintVoice returns to the Idle state.

### State Summary Table

| State | Visual | Duration |
|---|---|---|
| Idle | Nothing | Persistent |
| Activated | Ripple from cursor | ~300ms |
| Listening | Waveform underline at cursor | While speaking |
| Processing | Ghost text shimmer at cursor | ~1-2 seconds |
| Done | Text solidifies, everything vanishes | ~200ms fade |

---

## 3. Visual Feedback System (Teach Mode)

Teach Mode is the exception to "Zero UI." When GlintVoice needs to visually guide the user through a workflow, it requires a visible presence. It uses a cinematic, focused approach.

### The Spotlight
When Teach Mode activates:
1. The entire screen **dims by ~70%** (like a projector in a dark room), except for the specific UI element the AI wants the user to interact with.
2. A glowing **highlight ring** appears around the target element (e.g., a button, a menu item).
3. When the user completes the step, the highlight smoothly **glides** to the next element.

### The Whisper Bar
A thin, frosted-glass instruction bar slides up from the bottom of the screen (similar to a macOS Dock, but narrower — ~40px tall). It displays:
- The AI's instruction text (e.g., "Click the 'File' menu to open your project").
- A step counter (e.g., "Step 2 of 5").
- A small "X" button to exit Teach Mode.

### The Laser Line
A subtle, animated line connects the Whisper Bar to the highlighted element on screen, visually linking the instruction to the action. This acts as the AI's "laser pointer."

---

## 4. Fullscreen App Handling

When a fullscreen application is detected (e.g., a game, a presentation, or a maximized browser video):
- The ripple and waveform underline may not be visible or practical.
- **Fallback:** A thin (3-4px) **ambient glow** appears along the top edge of the screen. It pulses blue while listening, amber while processing, and briefly flashes green on completion. Uses near-zero screen space.

---

## 5. System Tray (The Only Persistent Element)

The system tray icon is the only permanent trace of GlintVoice on screen. It serves as the entry point for settings and status.
- **Left Click:** Opens the quick status overlay (shows current model, last dictation, and whether GlintVoice is active).
- **Right Click:** Opens the context menu (Settings, Pause App, Quit).

---

## 6. Settings & Configuration Panel

The settings panel is accessed via the system tray. It should be a clean, dark-themed window with the following tabs:

### A. General Tab
- **Hotkey Configuration:** Input field to record a custom global hotkey.
- **Launch on Startup:** Toggle to start the app when the OS boots.
- **Visual Feedback Style:** Dropdown to choose between "Cursor Ripple" (default), "Edge Glow", or "Floating Pill" (for users who prefer a visible widget).

### B. AI Models Tab
- **STT Model Selection:** Dropdown to select the Whisper model size (`tiny`, `base`, `small`). Includes indicators for speed vs. accuracy trade-off.
- **LLM Model Selection:** Dropdown to select the local Ollama model to use for cleanup (`phi3`, `llama3`, `gemma2`).

### C. Context Mapping Tab
A table interface where users can define rules based on the active application.
- **Column 1 (App Name):** e.g., `code.exe`, `Discord.exe`, `chrome.exe`
- **Column 2 (System Prompt):** The instructions sent to the LLM.
  - *Example for VS Code:* "You are a senior developer. Format the following dictation as a concise inline code comment. Remove all conversational filler."
  - *Example for Discord:* "Keep it casual and conversational. Use lowercase. Add relevant emojis sparingly."

### D. Voice Macros Tab
A table interface for defining trigger phrases and their corresponding actions.
- **Trigger Phrase:** e.g., `Action Item`
- **Action Type:** Dropdown (Webhook, Type Snippet, Run Script)
- **Action Value:** The URL, snippet text, or script path.

---

## 7. Technical Implementation

The overlay system (ripple, waveform, ghost text, spotlight) will be built using a **transparent, click-through, always-on-top window**. Recommended stack:

| Option | Use Case |
|---|---|
| **Tauri + HTML/CSS/JS** | Final product — lightweight (~5MB), beautiful CSS animations, transparent window support |
| **Electron** | Rapid prototyping — heavier but faster to develop |
| **Win32 API via Python ctypes** | Minimal overhead — direct OS calls for the overlay, no framework needed |

The overlay window covers the entire screen but is fully transparent and passes all mouse/keyboard events through to the application beneath it. GlintVoice only draws the small animation elements (ripple, waveform, text) on this canvas at the tracked cursor coordinates.
