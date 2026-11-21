# Operator Guide: Dedicated Web AI Browser & Local Hands Execution Bridge
> **Autonomous AI Income Factory — Tool Infrastructure #19**  
> **Task ID:** `aii-mwqh5uqm-15a517`  
> **Classification:** Isolated Autonomous Browser Profile & Sandboxed Execution Bridge

---

## 1. System Architecture & Isolation Guarantees

Many developers and researchers use web-based frontier AI models (Gemini, ChatGPT, Claude, DeepSeek, Zhipu/Z.ai, Qwen, MiniMax) for deep technical inquiries and code generation. However, using your primary browser creates friction:
- Logins, cookies, and history mix with personal browsing.
- Extensions or ad-blockers can interfere with AI web applications.
- Web AIs produce code that you must manually copy, paste, save to a file, open a terminal, and run.

The **Dedicated Web AI Browser & Hands Bridge** solves this through a dual-layer isolation architecture:

```
[ USER WORKSTATION ]
       |
       +---> [ Layer 1: Dedicated Browser Profile ]
       |     - Directory: %LOCALAPPDATA%\AIIncome_Dedicated_Browser
       |     - Remote Debugging: Port 9222 (--remote-debugging-port=9222)
       |     - 100% Isolated from personal Chrome/Edge bookmarks & cookies
       |     - Preloaded with 7 Web AI tabs
       |
       +---> [ Layer 2: Local AI Hands Bridge ]
             - File: tools/web_ai_hands_bridge.py
             - Sandboxed Workspace: projects/hands-executions/
             - Security Guardrails: Destructive command blocklist
             - Execution Telemetry: Output capture & execution_history.jsonl
```

---

## 2. The 7 Preloaded Frontier Web AI Endpoints

The dedicated launcher automatically opens all 7 frontier web interfaces simultaneously:
1. **Google Gemini:** `https://gemini.google.com/app`
2. **ChatGPT (OpenAI):** `https://chatgpt.com/`
3. **Claude (Anthropic):** `https://claude.ai/new`
4. **DeepSeek:** `https://chat.deepseek.com/`
5. **Zhipu AI (GLM / Z.ai):** `https://chat.z.ai/`
6. **Qwen (Alibaba Cloud):** `https://chat.qwen.ai/`
7. **MiniMax:** `https://agent.minimax.io/`

---

## 3. Quick Start & Operation

### Step 1: Launch the Dedicated AI Browser
Double-click or run from terminal:
```cmd
tools\launch_dedicated_ai_browser.bat
```
*Effect:* Opens a dedicated, fresh browser window preloaded with all 7 tabs. It creates an isolated profile in `%LOCALAPPDATA%\AIIncome_Dedicated_Browser` and enables CDP debugging on port `9222`. Sign into your free accounts once; they will remain cached in this isolated profile without affecting your personal browser.

### Step 2: Verify the Hands Execution Bridge
Test the local execution engine:
```cmd
tools\run_hands_bridge.bat --test-run
```
*Expected Output:*
```markdown
### Local AI Hands Execution Report — ✅ SUCCESS
- Exit Code: 0
- Execution Time: 0.035s
- Standard Output: Hands Bridge Active
```

### Step 3: Run Code from Any Web AI
When any Web AI generates Python, PowerShell, or Batch scripts:
1. Pass the snippet to `tools/web_ai_hands_bridge.py`.
2. The script runs inside `projects/hands-executions/` with zero risk of contaminating other projects.
3. Standard output, errors, execution time, and generated files are captured and logged to `execution_history.jsonl`.
4. Copy the formatted Markdown report back to the Web AI for instant interactive debugging.

---

## 4. Safety Guardrails & Security Policies
- **Destructive Command Blocking:** The bridge actively filters patterns like disk formatting, recursive root directory deletions, and system shutdowns.
- **Sandboxed Working Directory:** All execution subprocesses run with `cwd` set strictly to `projects/hands-executions/`.
- **Zero External Telemetry:** The bridge operates entirely locally via Python standard libraries (`subprocess`, `urllib.request`, `json`, `os`). Zero data leaves your machine.
- **Universal Portability:** Uses relative paths (`%~dp0` in batch, `os.path.dirname(__file__)` in Python).
