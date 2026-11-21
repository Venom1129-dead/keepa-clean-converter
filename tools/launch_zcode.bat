@echo off
title Launch ZCode (Zed Editor / Agent)
cls
cd /d "%~dp0\.."

echo [*] Opening project workspace in ZCode...
if exist "%LOCALAPPDATA%\Programs\ZCode\ZCode.exe" (
  start "" "%LOCALAPPDATA%\Programs\ZCode\ZCode.exe" "%CD%"
) else if exist "%ProgramFiles%\ZCode\ZCode.exe" (
  start "" "%ProgramFiles%\ZCode\ZCode.exe" "%CD%"
) else (
  start "" zcode "%CD%"
)
echo [+] ZCode launched with workspace: %CD%
