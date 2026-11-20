# AGENTS.md — Master Multi-Agent Collaboration Protocol

## Role Allocations & Boundaries
- **Antigravity (Plan Mode & Orchestration):**
  - **Operating Mode:** PLAN MODE ONLY. Formulates architectures, writes `build_spec.md` blueprints, coordinates memory vaults, and posts execution plans.
  - **Boundary:** Never performs heavy code execution or unreviewed bulk edits.
- **Cline (Execution Worker):**
  - Owns: `03_Active_MVP/` code implementation, builds, and local development.
  - Tasks: Reads approved `build_spec.md`, executes file edits, implements core algorithms, and runs local servers.
- **Claude (CEO, Architect & Brutal Verifier):**
  - Owns: Idea kill-switches, plan reviews, and independent code audits.
  - Verification: Grades Cline's work independently using deterministic test suites (`verifier/`) and `git diff` inspections. Marks PASS or FAIL in `HANDOFF.md`.
- **Gemini (Intelligence & Market Research):**
  - Owns: `01_Research/`, live web search grounding, Proof-of-Wallet discovery, and Gumroad/Reddit launch copy.

## Memory Architecture ("Found Once, Remembered Forever")
All agents share the **Memory Vault** in `00_Brain/memory/` (mirrored from OpenCode):
- `findings/`: Validated technical discoveries, free model endpoints, and configurations.
- `lessons/`: Key learnings from failed tests or bugs.
- `playbooks/`: Reusable, multi-step SOPs.
- `errors/`: Stuck states, error logs, and watchdog notes.

## Strict Verification-First Rule (NO PHANTOM PROGRESS)
1. **Never claim work is "in progress" without active proof:**
   - An open window or idle process (`cline-app.exe`) does NOT mean work has started.
   - A task file in a folder does NOT mean an agent is executing it.
2. **Deterministic State Definitions (Always cite one of these 4):**
   - `IDLE`: No agent is executing code right now.
   - `ACTIVE_EXECUTING`: An agent is currently running a command with a live PID or active stream.
   - `VERIFIED_COMPLETE`: Code is written and has passed a deterministic test script (Exit Code 0).
   - `FAILED / BLOCKED`: A command failed or human action is required.
3. **Evidence Requirement:** Every status report must list the exact files on disk and test outputs, not assumptions.
