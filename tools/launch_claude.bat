@echo off
title Launch Claude Desktop (Auditor & Verifier)
cls
cd /d "%~dp0\.."

echo [*] Copying active task briefing from HANDOFF.md to clipboard...
(
  echo You are the Chief Risk Auditor and Verifier for the Autonomous Income and Trading Factory.
  echo Review the current task state in HANDOFF.md and test suites.
  echo.
  type HANDOFF.md
) | clip

echo [+] Briefing copied to clipboard!
echo [*] Launching Claude Desktop...

if exist "%LOCALAPPDATA%\AnthropicClaude\claude.exe" (
  start "" "%LOCALAPPDATA%\AnthropicClaude\claude.exe"
) else (
  start "" claude
)
echo [+] Claude Desktop launched! Simply press Ctrl+V to paste the active audit briefing.
