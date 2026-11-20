# Playbook: Microsoft Edge Automated Navigation & Visual Verification Protocol
- **Created:** 2026-11-20
- **Applies to:** Antigravity, Cline, Claude, OpenCode, Codex, Gemini CLI

## 1. Operating Rules
1. **Exclusive Browser:** Always use Microsoft Edge (`msedge.exe`).
2. **Never Claim Without Visual Proof:** Never tell the user a page is open, loaded, or waiting for input without deterministic proof (exit code 0 from `tools/ensure_edge_browser.py`, or verified screenshot file > 10KB on disk).
3. **No Terminal Child Termination:** Never launch Edge directly as a sub-process of a transient CLI tool (Windows will terminate Edge when the CLI exits). Launch via `explorer.exe "microsoft-edge:<url>"` to anchor it in the user's interactive desktop shell.

## 2. Architecture & Components
- **Browse Relay Daemon:** `C:\Users\myven\.local\bin\browse.exe serve` listening on `http://127.0.0.1:19988`.
- **Environment:** `OPENCODE_BROWSER_ALLOW_FILE_URLS=1` set permanently in User environment.
- **Edge Extension:** OpenCode Browse (`mfnicocicmmlkpjnaffgihfjhdgjkdjg`) paired to relay profile `edge-desktop-tkvbmig-2`.
- **Automated Watchdog & Test Script:** `python tools/ensure_edge_browser.py`

## 3. How Agents Execute Browser Actions
### Method A: Via Browse MCP Server (Preferred in Antigravity / Cline)
Call lazy tool `execute` on server `browse`:
```json
{
  "code": "await page.goto('https://example.com'); return await page.title();"
}
```

### Method B: Via CLI
```powershell
& "C:\Users\myven\.local\bin\browse.exe" execute --json "await page.goto('https://example.com'); return await page.title();"
```

## 4. Deterministic Verification Checklist
Before reporting browser state to the user:
- [ ] Edge process verified via `Get-Process msedge`.
- [ ] Browse relay HTTP 200 on `http://127.0.0.1:19988`.
- [ ] `browse status` reports `Extension: connected (0.1.5)`.
- [ ] Real screenshot saved to `00_Brain/proofs/` and verified > 10,000 bytes.
