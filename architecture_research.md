# Architecture Validation Research

This document summarizes the research conducted to validate whether the proposed Python-based, 100% local architecture can meet the strict performance requirements of GlintVoice (specifically the < 1.5s total latency requirement for dictation and the "Zero UI" overlay).

## 1. Zero UI Overlay Performance
**Requirement:** A transparent, click-through window that follows the text cursor without lagging the system or interfering with normal clicks.
**Finding:** **Valid.**
- Using Python to call native Windows APIs (`win32gui` or `ctypes`) to set the `WS_EX_LAYERED` and `WS_EX_TRANSPARENT` window styles is extremely performant. 
- The Windows Desktop Window Manager (DWM) handles the rendering directly via GPU hardware acceleration.
- Because Python is only sending position and drawing commands (not handling the actual pixel-by-pixel transparency math), the CPU overhead is negligible. It is significantly faster and lighter than running an Electron app in the background.

## 2. Local STT Latency
**Requirement:** Transcription must complete in under 500ms for short sentences to hit the overall latency budget.
**Finding:** **Valid, but requires hardware-specific routing.**
- `whisper.cpp` (via Python bindings) adds almost zero overhead compared to the raw C++ binary. It is incredibly fast on Apple Silicon (M-series Macs) and decent on pure CPU.
- **Optimization for Windows:** If the target Windows machine has an **NVIDIA GPU**, research indicates that using the **`faster-whisper`** library (which uses the CTranslate2 engine) drastically outperforms `whisper.cpp`. `faster-whisper` leverages CUDA and 8-bit quantization to achieve massive throughput gains.
- **Conclusion:** The architecture should dynamically check for CUDA availability. If an NVIDIA GPU is present, it routes to `faster-whisper`; if not, it falls back to CPU-optimized `whisper.cpp`.

## 3. Local LLM Latency (Ollama)
**Requirement:** The LLM must process the transcript, apply the context prompt, and generate the cleaned text in under 1 second.
**Finding:** **Valid, provided strict memory management is enforced.**
- Small models like **Phi-3 Mini (3.8B parameters)** or **Llama 3 (8B)** are fast enough to generate a short sentence in under 500ms on modern GPUs.
- **The Bottleneck (Cold Starts):** Ollama's default behavior is to unload a model from VRAM after 5 minutes of inactivity. If the user dictates something after 10 minutes of silence, they will hit a "cold start" penalty (taking 2-5 seconds just to load the model from the SSD into RAM).
- **The Solution:** We must programmatically set the environment variable `OLLAMA_KEEP_ALIVE=-1` when initializing the GlintVoice background service. This forces the model to stay resident in VRAM permanently while GlintVoice is running, completely eliminating the Time To First Token (TTFT) delay.

## Final Verdict
The architecture is completely viable and can easily achieve sub-1.5s latency, provided we implement the `OLLAMA_KEEP_ALIVE` fix and utilize `faster-whisper` for users with dedicated GPUs.
