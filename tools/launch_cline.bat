@echo off
title Launch Cline App
cls
cd /d "%~dp0\.."

echo [*] Opening project workspace in Cline...
if exist "%LOCALAPPDATA%\Cline\cline-app.exe" (
  start "" "%LOCALAPPDATA%\Cline\cline-app.exe" "%CD%"
) else (
  start "" cline "%CD%"
)
echo [+] Cline launched with workspace: %CD%
