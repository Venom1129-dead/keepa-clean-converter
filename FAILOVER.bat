@echo off
title AI Factory — Instant Failover Switch
cls
color 0B

echo ========================================================
echo        AI FACTORY — INSTANT FAILOVER SWITCH
echo ========================================================
echo.
echo Antigravity quota exhausted? No problem.
echo.
echo 1. Copying latest HANDOFF.md state to clipboard...
(
  echo Read AGENTS.md, program.md, and HANDOFF.md.
  echo Antigravity hit its quota cap. Resume immediately from the exact checkpoint in HANDOFF.md.
  echo.
  type HANDOFF.md
) | clip

echo [+] Baton copied to clipboard! (Just press Ctrl+V in the new window)
echo.
echo 2. Launching OpenCode Desktop (Uses OpenCode Zen Free Models)...
start "" "C:\Users\myven\AppData\Local\Programs\ai.opencode.desktop\OpenCode.exe"

echo 3. Opening Gemini Web backup in browser...
start https://gemini.google.com/app

echo.
echo ========================================================
echo [+] OpenCode and Gemini Web launched!
echo [+] In either app, press Ctrl+V and Enter to resume immediately.
echo ========================================================
echo.
pause
