# Design & User Experience (UX)

## 1. Design Philosophy
The primary goal of this application is to be **invisible**. It should feel like a native OS feature rather than a bloated application. The user should rarely need to interact with a GUI.

## 2. User Interface (UI)

### The System Tray
The application runs as a background process with a simple icon in the system tray (Windows) or menu bar (macOS).
- **Left Click:** Opens the quick status overlay.
- **Right Click:** Opens the context menu (Settings, Pause App, Quit).

### Visual Feedback Overlay
Because the app runs in the background, immediate visual feedback is critical so the user knows if they are being recorded.
- **Recording State:** A small, unobtrusive floating indicator (e.g., a glowing microphone icon or a minimal pill-shaped widget) appears at the edge of the screen or near the text cursor while the hotkey is active.
- **Processing State:** The indicator turns into a subtle spinner while Whisper and Ollama are processing, indicating that the user should wait a second before typing manually.

## 3. Settings & Configuration Panel

The settings panel should be clean, modern, and accessible via the system tray menu. It handles the following configurations:

### A. General Tab
- **Hotkey Configuration:** Input field to record a custom global hotkey.
- **Launch on Startup:** Toggle to start the app when the OS boots.

### B. AI Models Tab
- **STT Model Selection:** Dropdown to select the Whisper model size (`tiny`, `base`, `small`). Includes indicators for speed vs. accuracy.
- **LLM Model Selection:** Dropdown to select the local Ollama model to use for cleanup (`phi3`, `llama3`).

### C. Context Mapping Tab (The Unique Feature)
A table interface where users can define rules based on the active application.
- **Column 1 (App Name):** e.g., `code.exe`, `Discord.exe`
- **Column 2 (System Prompt):** The instructions sent to the LLM. 
  - *Example for Code:* "You are a senior developer. Format the following dictation as a concise inline code comment. Remove all conversational filler."

### D. Voice Macros Tab
A table interface for defining trigger phrases.
- **Trigger Phrase:** e.g., `Action Item`
- **Action Type:** Dropdown (Webhook, Type Snippet, Run Script)
- **Action Value:** The URL or script path.
