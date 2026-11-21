# AGENTS.md — Master Multi-Agent Collaboration Protocol

## 1. Role Allocations & Verified Agent Roster
Every agent has a defined role, a verified local executable, and a deterministic responsibility:

| Agent | Core Specialty | Verified Local Path | Launch Command | Primary Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **Antigravity** | Chief Coordinator & Architect | Built-in / IDE | Self | Master planning, architecture blueprints, memory coordination, skill synthesis. |
| **ZCode** (Zed Engine) | High-Speed Kernel & Indicator Dev | `%LOCALAPPDATA%\Programs\ZCode\ZCode.exe` | `tools\launch_zcode.bat` | Low-latency math, fast backtest indicators (NumPy/Rust/C kernels), rapid code edits. |
| **Cline** | Core Application Worker | `%LOCALAPPDATA%\Cline\cline-app.exe` | `tools\launch_cline.bat` | Strategy adapter implementations, API integrations, data parsers, test suites. |
| **Claude** | CEO, Risk Auditor & Brutal Verifier | `%LOCALAPPDATA%\AnthropicClaude\claude.exe` | `tools\launch_claude.bat` | Statistical validation, p-value audit, data-snooping rejection, kill-switch enforcer. |
| **OpenCode** | Web Intelligence & Sentiment Miner | `%LOCALAPPDATA%\Programs\ai.opencode.desktop\OpenCode.exe` | `tools\launch_opencode.bat` | Scraping crowdsourced strategies, parsing news sentiment, extracting macro catalyst data. |

---

## 2. Universal Portability Invariant
- **Rule:** ZERO hardcoded personal paths (`C:\Users\username\...`) in any script, test, or config.
- **Implementation:** Always use relative paths (`os.path.dirname(__file__)` in Python, `%~dp0` in Batch, `$PSScriptRoot` in PowerShell).
- **Verification:** `python tools/storage_audit.py` must report 0 hardcoded paths and Exit Code 0 on any machine or drive.

---

## 3. Strict Verification-First Rule (NO PHANTOM PROGRESS)
1. **Never claim work is "in progress" or "open" without active proof:**
   - An open window or idle process does NOT mean work has started.
   - A shell launcher returning Exit Code 0 does NOT mean an agent has completed a task.
   - A task file in a folder does NOT mean an agent is executing it.
2. **Deterministic State Definitions (Always cite one of these 4):**
   - `IDLE`: No agent is executing code right now.
   - `ACTIVE_EXECUTING`: An agent is currently running a command with a live PID or active stream.
   - `VERIFIED_COMPLETE`: Code is written and has passed a deterministic test script (Exit Code 0).
   - `FAILED / BLOCKED`: A command failed or human action is required.
3. **Evidence Requirement:** Every status report must list the exact files on disk, test outputs, or execution proofs.
