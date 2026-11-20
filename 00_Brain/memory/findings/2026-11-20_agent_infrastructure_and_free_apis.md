# Finding: Multi-Agent Environment & Free Model Endpoints Map
- **Date:** 2026-11-20
- **Status:** VERIFIED
- **Category:** Infrastructure / Free Model Routing

---

## 1. Discovered Agent Installations on System
1. **OpenCode:**
   - Config: `D:\AI RE\opencode-config\opencode.jsonc` & `C:\Users\myven\.config\opencode\opencode.json`
   - Memory Vault: `D:\AI RE\opencode\memory`
   - Free Models: `opencode/mimo-v2.6-flash-free`, `opencode/nemotron-3-ultra-free`, `opencode/longcat-2.5-preview-free`, `opencode/ling-3.0-tiny-free`, `opencode/north-mini-code-free`
2. **Cline Desktop:**
   - Location: `C:\Users\myven\.cline` & `C:\Users\myven\Desktop\Cline.lnk`
   - Settings: `C:\Users\myven\.cline\data\settings\providers.json`
   - Shared Queue: Connected to `C:/AIIncome/orchestrator/mcp-server.mjs` (`ai-income-queue`)
3. **OpenAI Codex:**
   - Location: `C:\Program Files\WindowsApps\OpenAI.Codex_...`
   - Config: `C:\Users\myven\.codex\config.toml` (Default model: `gpt-6-luna`)
   - Auth Switch: `codex login --with-api-key` switches from ChatGPT web quota to direct API keys

---

## 2. GPT Luna / Sol / Astra Free API Routing Map
- **GPT-6 Luna / GPT-5 Sol:** Accessible through OpenAI Codex app or routed via LiteLLM / OpenRouter using OpenAI-compatible base URLs.
- **GitHub Models (Azure OpenAI):** Free access to GPT-4o / GPT-4o-mini with GitHub Personal Access Token at `https://models.inference.ai.azure.com`.
- **Google AI Studio (OpenAI Compatible):** Free Gemini 2.5 Flash at `https://generativelanguage.googleapis.com/v1beta/openai/` (15 RPM free, zero cost).
- **OpenRouter Free Tier:** `https://openrouter.ai/api/v1` for community-hosted free models.
