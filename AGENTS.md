# AGENTS.md — Master Multi-Agent Collaboration Protocol

## 1. The Autonomous Perpetual Loop Invariant
- **Directive:** WORK NEVER STOPS. Always execute in a continuous loop until the milestone is complete.
- **Self-Sufficiency Principle:** Antigravity actively drives, codes, verifies, and tests all pipelines. We never stall or wait for external manual steps unless a true user-only action (private payment setup, 2FA, API credential approval) is strictly required.
- **User Interrupt Boundary:** Only pause to ask the user when human judgment, real-world capital, or private authentication is required. All technical, mathematical, coding, and verification work proceeds autonomously.

---

## 2. Verified Agent Roster & Executables
| Agent | Core Specialty | Verified Executable Path | Autonomous Integration |
| :--- | :--- | :--- | :--- |
| **Antigravity** | Chief Coordinator & Relentless Worker | Built-in | Direct continuous execution loop across all files, tests, and deploys. |
| **ZCode** (Zed Engine) | High-Speed Kernel & Math Edits | `%LOCALAPPDATA%\Programs\ZCode\ZCode.exe` | Available via `tools\launch_zcode.bat` for low-latency kernel inspection. |
| **Cline** | Application Worker | `%LOCALAPPDATA%\Cline\cline-app.exe` | Available via `tools\launch_cline.bat` with live workspace synchronization. |
| **Claude** | Chief Risk Auditor & Kill-Switch | `%LOCALAPPDATA%\AnthropicClaude\claude.exe` | Available via `tools\launch_claude.bat` with clipboard briefing injection. |
| **OpenCode** | Web Intelligence & Scraper | `%LOCALAPPDATA%\Programs\ai.opencode.desktop\OpenCode.exe` | Available via `tools\launch_opencode.bat`. |

---

## 3. Universal Portability Invariant
- **Rule:** ZERO hardcoded personal paths (`C:\Users\username\...`) in any script, test, or config.
- **Implementation:** Always use relative paths (`os.path.dirname(__file__)` in Python, `%~dp0` in Batch, `$PSScriptRoot` in PowerShell).
- **Verification:** `python tools/storage_audit.py` must report 0 hardcoded paths and Exit Code 0 at all times.

---

## 4. Strict Verification-First Rule (NO PHANTOM PROGRESS)
1. **Never claim work is complete without active proof:**
   - Every asset must have clean files on disk.
   - Every asset must have an automated test script (`verifier/`) returning **Exit Code 0**.
   - Every web app must return **HTTP 200** on production hosting.
2. **Deterministic State Definitions:**
   - `IDLE`: Pipeline task completed, waiting for next queue trigger.
   - `ACTIVE_EXECUTING`: Actively writing, verifying, or deploying code.
   - `VERIFIED_COMPLETE`: Code is written and verified by deterministic test scripts (Exit Code 0).
   - `FAILED / BLOCKED`: Actionable failure requiring retry or user input.
