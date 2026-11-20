# Lesson: Interactive Browser Tab Lifecycle & Automated UI Automation Cleanup
- **Date:** 2026-11-21
- **Severity:** High (User Workflow Hygiene & System Resource Management)

## 1. Problem
When the agent launched URLs on the user's interactive monitor (`WinSta0\Default`) via `start msedge.exe <URL>`, each invocation spawned a new tab in the running Microsoft Edge window (e.g., GitHub Device Activation, duplicate Keepa/Shopify converter previews, old audit pages). 
Because these tabs were launched outside the `browse` MCP relay, the standard `browse tabs cleanup` command did not track them, leaving 8 tabs lingering in the user's browser and consuming excess RAM.

## 2. Root Cause
- `browse tabs cleanup` only closes tabs managed by its internal CDP session.
- System shell launches (`msedge.exe <url>`) run in the user's main browser profile and remain open until explicitly closed.

## 3. Solution & Safeguards
1. **Interactive UI Automation Cleanup Script (`tools/close_tabs.ps1`):**
   - Dispatches directly to `WinSta0\Default` via `schtasks /it`.
   - Uses .NET `UIAutomationClient` to find all `TabItem` elements and clicks their `Close tab` buttons.
   - Enforces strict safety rules:
     - **NEVER close user documents** (e.g., `AI income - Google Docs`).
     - Closes stale authentication/activation tabs (`Device Activation`).
     - Closes stale converter and duplicate audit tabs.
2. **Permanent Automation in `tools/energy_saver.py`:**
   - Both `browse tabs cleanup` and the interactive UI Automation dispatch run automatically in our maintenance loop.
3. **Verification:**
   - Enumerate tabs via `inspect_tabs.ps1` before and after to verify only intended tabs remain open.
