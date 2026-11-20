# Lesson Learned: Never Assume Browser State Without Visual Verification
- **Date:** 2026-11-20
- **Severity:** High (User Trust / Phantom Progress)
- **What Happened:** 
  The agent ran `Start-Process msedge "https://github.com/login/device"`. The shell returned exit code 0. The agent falsely claimed "Edge is open to the device page and waiting for your code" without verifying whether a visible browser window actually existed or taking a screenshot. In reality, Edge had no active GUI window in the foreground, and the user saw nothing.
- **Root Cause:**
  1. Confusing a successful OS process launch (exit code 0) with actual UI rendering on the user's display.
  2. Blindly trusting third-party CLI stdout messages (e.g. `✓ Opened browse in Microsoft Edge to connect it`) and repeating them to the user without verifying whether the browser tab was actually created or visible.
- **Permanent Fix & Rule:**
  1. Never tell the user a webpage or tab is open based solely on terminal stdout or exit codes.
  2. If a browser task cannot capture a verified screenshot or confirm active tab URL via live inspection, report that the tab state could not be confirmed rather than claiming it opened.
