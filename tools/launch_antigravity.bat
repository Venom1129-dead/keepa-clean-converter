@echo off
title Launch Antigravity IDE
cls
cd /d "%~dp0\.."

echo [*] Launching Antigravity IDE...
if exist "%LOCALAPPDATA%\Programs\Antigravity IDE\Antigravity IDE.exe" (
  start "" "%LOCALAPPDATA%\Programs\Antigravity IDE\Antigravity IDE.exe" "%CD%"
) else if exist "%LOCALAPPDATA%\Programs\antigravity\Antigravity.exe" (
  start "" "%LOCALAPPDATA%\Programs\antigravity\Antigravity.exe" "%CD%"
) else (
  start "" antigravity "%CD%"
)
echo [+] Antigravity IDE launched with workspace: %CD%
