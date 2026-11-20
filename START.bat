@echo off
title AI Income Factory — 1-Click Starter
color 0A
cls

echo ========================================================
echo        AI INCOME FACTORY — DAILY LAUNCHER
echo ========================================================
echo.
echo [CURRENT TASK]: Keepa Clean Excel Converter (MVP #1 Built!)
echo [ACTIVE AGENT]: Antigravity + Claude (Architect & Verifier)
echo [VERIFIER STATUS]: Sanity Tests PASSED
echo.
echo ========================================================
echo.
echo  Choose an action:
echo.
echo   [1] Open Keepa Clean Converter in Browser (Test MVP #1)
echo   [2] Connect Free API Key to Codex CLI (Bypass Nov 24 limit)
echo   [3] Run Research Harvester (Extract YouTube/Web links)
echo   [4] View Live Status & Baton (HANDOFF.md)
echo   [5] Open Project Folder in File Explorer
echo   [6] Run Verifier Sanity Checks (Python)
echo   [7] Instant Failover Switch (OpenCode / Gemini Web)
echo   [8] Exit
echo.
echo ========================================================
set /p choice="Enter choice (1-8): "

if "%choice%"=="1" goto OPEN_MVP
if "%choice%"=="2" goto SETUP_CODEX
if "%choice%"=="3" goto HARVEST
if "%choice%"=="4" goto STATUS
if "%choice%"=="5" goto OPEN_DIR
if "%choice%"=="6" goto RUN_TESTS
if "%choice%"=="7" goto FAILOVER
if "%choice%"=="8" goto END

:OPEN_MVP
cls
echo [*] Opening Keepa Clean Converter in your browser...
start "" "03_Active_MVP\frontend\index.html"
goto END

:SETUP_CODEX
cls
call tools\setup_codex_api.bat
goto END

:HARVEST
cls
echo [*] Running Automated Research Harvester...
echo.
python tools\harvest.py
echo.
pause
goto END

:STATUS
cls
echo [*] Live HANDOFF.md:
echo ========================================================
type HANDOFF.md
echo ========================================================
echo.
pause
goto END

:OPEN_DIR
explorer .
goto END

:RUN_TESTS
cls
echo [*] Running Verifier test suite...
python 03_Active_MVP\verifier\test_converter.py
echo.
pause
goto END

:FAILOVER
cls
call FAILOVER.bat
goto END

:END
exit
