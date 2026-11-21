@echo off
title Launch OpenCode Desktop
cls
cd /d "%~dp0\.."

echo [*] Launching OpenCode...
if exist "%LOCALAPPDATA%\Programs\ai.opencode.desktop\OpenCode.exe" (
  start "" "%LOCALAPPDATA%\Programs\ai.opencode.desktop\OpenCode.exe" "%CD%"
) else (
  start "" opencode "%CD%"
)
echo [+] OpenCode launched with workspace: %CD%
