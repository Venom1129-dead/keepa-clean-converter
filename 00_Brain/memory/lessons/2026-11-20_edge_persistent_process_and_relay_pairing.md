# Lesson: Resolving Edge Extension Disconnection & Browser Lifecycle
- **Date:** 2026-11-20
- **Severity:** Critical (Core Browser Automation Infrastructure)

## 1. What Happened
The browse extension in Edge showed `disconnected` and attempts to pair generated pairing codes that didn't appear in tabs. When Edge was spawned by CLI scripts, it died immediately with exit code 1006 after 2 seconds.

## 2. Root Cause Analysis
1. **Subprocess Lifecycle Collision:** When a script or CLI tool launches Edge as a child process without anchoring to the desktop shell, Windows terminates child processes when the parent script exits. This killed Edge 2.4s after startup (`extension.close code=1006`).
2. **Missing Local File Policy:** The browse relay blocked `file:///` URLs by default with security error `browse blocked Page.navigate to a file: URL`.
3. **Ghost Pairing Claims:** An agent reported "In the Edge tab that just opened... enter pairing code" without any command actually opening that tab.

## 3. The Permanent Solution
1. **Desktop Shell Launching:** Starting Edge via `explorer.exe "microsoft-edge:about:blank"` delegates process creation to `explorer.exe` (the interactive desktop shell, Session ID 4). Edge stays permanently open and visible.
2. **Permanent Relay File Permission:** Added `OPENCODE_BROWSER_ALLOW_FILE_URLS=1` to the Windows User environment variables.
3. **Automated Watchdog:** Created `tools/ensure_edge_browser.py` which:
   - Verifies Edge process is active.
   - Verifies relay HTTP 200 on `http://127.0.0.1:19988`.
   - Confirms `Extension: connected (0.1.5)`.
   - Executes live DOM test and captures proof screenshot.
   - Exits 0 only when all 4 conditions are verified.
