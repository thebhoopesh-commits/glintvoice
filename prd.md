# Product Requirements Document (PRD)

## 1. Product Overview
The project is a next-generation AI dictation tool designed to rival existing solutions like GlintVoice. Unlike standard dictation apps that rely on cloud APIs, this product focuses on absolute privacy (100% local processing), deep OS integration, and workflow automation.

## 2. Target Audience
- **Privacy-Conscious Professionals:** Doctors, lawyers, and enterprise workers bound by NDAs or HIPAA who cannot send audio to cloud services.
- **Software Developers:** Power users who want context-aware formatting in their IDEs.
- **Workflow Automators:** Users who want to trigger APIs and webhooks using their voice.

## 3. Core Features (MVP)
- **Global Hotkey Toggle:** A system-wide shortcut (e.g., `Ctrl+Space`) to start and stop dictation seamlessly, regardless of the active application.
- **Local Transcription (STT):** High-accuracy voice-to-text conversion running entirely on the local CPU/GPU using Whisper models.
- **Local AI Cleanup:** Real-time processing of the raw transcript using a local LLM to remove filler words, fix grammar, and format text properly.
- **Auto-Typing:** Simulated keyboard output to instantly type the cleaned text into the user's active window.

## 4. Unique Differentiators (V2 Features)
- **Active-Window Context Awareness:** Automatically detects the executable of the focused window (e.g., `code.exe`, `slack.exe`) and applies a specific, user-defined AI prompt (e.g., "Format as code comment", "Format as casual chat").
- **Voice Macros:** Ability to define trigger phrases (e.g., "Action Item") that bypass typing and instead execute a predefined script or webhook (e.g., sending data to Notion).

## 5. Non-Functional Requirements
- **Privacy:** Zero internet connection required for core functionality. No audio or text leaves the local machine.
- **Latency:** The time from stopping the recording to the first typed character should ideally be under 1.5 seconds on modern hardware.
- **Resource Efficiency:** Must allow users to select smaller models (e.g., Whisper Tiny, Phi-3) to accommodate laptops without dedicated GPUs.
