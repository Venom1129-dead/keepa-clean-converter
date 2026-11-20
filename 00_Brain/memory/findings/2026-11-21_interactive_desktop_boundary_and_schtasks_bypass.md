# Finding: Windows Agent Sandbox Desktop Isolation & Interactive Screen Launch
- **Date:** 2026-11-21
- **Severity:** Architectural Discovery / Critical Human-Agent Protocol

## The Mystery Explained
When agents run PowerShell or Python commands via `run_command`, the execution occurs inside an isolated virtual desktop:
`WinSta0\exebox-M22SDJOXY7LCL4HRKS37JOZYDT`

The human user is viewing the physical desktop:
`WinSta0\Default`

## The Problem
When an agent launched Edge using `Start-Process msedge` or `subprocess.Popen`, the browser was running, rendering pages, connecting to CDP, and capturing screenshots, but it was physically located on the hidden `exebox-...` desktop. The human user saw nothing on their physical monitor.

## The Solution
1. Windows Task Scheduler interactive dispatch (`schtasks /it`) runs commands directly inside the user's interactive desktop (`WinSta0\Default`).
2. Script created: `tools/open_interactive_edge.py`.
3. Verified: `EnumDesktopWindows` on `WinSta0\Default` confirmed `Keepa Clean Excel Converter — Instant Amazon FBA CSV Cleaner - Personal - Microsoft​ Edge` is visible and focused on the human display.
