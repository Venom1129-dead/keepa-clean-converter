# Feature Specification: Wake Word & Hands-Free Mic Control
- **Target:** Antigravity Voice Talker / OpenCode Voice Bridge
- **Status:** SPEC_LOCKED

## Wake Words & Voice Triggers
1. **Wake Trigger ("Listen Antigravity"):**
   - Automatically unpauses/unmutes the voice microphone stream.
   - Sets visual indicator to `ACTIVE_LISTENING`.
   - Starts capturing speech input until silence threshold is reached.

2. **Sleep / Mute Trigger ("Close Antigravity mic"):**
   - Pauses/mutes the microphone stream (`track.enabled = false`).
   - Cuts off background noise and room chatter from being streamed.
   - Sets visual indicator to `PAUSED_MUTED`.

## Client-Side Audio Pipeline Architecture
- **Offline Wake-Word Engine:** Porcupine / Web Speech Recognition API / Local VAD (Voice Activity Detection).
- **Zero Cloud Leakage:** Listens strictly for keyword tokens locally in buffer; does not stream audio to LLM until "Listen Antigravity" is detected.
- **Immediate Pause:** On detecting "Close Antigravity mic", buffer clears immediately without firing a model prompt.
