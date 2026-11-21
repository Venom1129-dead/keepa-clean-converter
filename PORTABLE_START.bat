@echo off
title Autonomous AI Income & Trading Factory — Portable Launcher
color 0B
cls

cd /d "%~dp0"

echo ====================================================================
echo    AUTONOMOUS AI INCOME ^& TRADING ENGINE — UNIVERSAL LAUNCHER
echo ====================================================================
echo  [PORTABILITY]: 100%% Relative Paths (Run from ANY folder or PC)
echo  [STORAGE]: Automatic Hygiene ^& Git Optimization
echo ====================================================================
echo.
echo  Choose an action:
echo.
echo   --- MULTI-AGENT LAUNCHERS (VISIBILITY FIRST) ---
echo   [1] Launch ZCode (Fast Zed Editor / Indicator Kernel Agent)
echo   [2] Launch Cline App (Execution Worker)
echo   [3] Launch Claude Desktop (Architect ^& Kill-Switch Auditor)
echo   [4] Launch OpenCode Desktop (Intelligence ^& Sentiment Agent)
echo   [5] Launch Antigravity IDE (Chief Orchestrator)
echo.
echo   --- TRADING AI SUITE (EMPIRICAL STRATEGY TESTING) ---
echo   [6] Run Trading AI Backtest Engine (Deterministic Empirical Test)
echo   [7] Run Trading AI Strategy Miner (Scan ^& Parse Web Strategies)
echo   [8] Run Trading AI Data Harvester (Fetch Historical Data)
echo.
echo   --- STORAGE ^& SYSTEM HYGIENE ---
echo   [9] Run Storage Management ^& Portability Audit (storage_audit.py)
echo   [10] View Live Handoff Board (HANDOFF.md)
echo   [11] Exit
echo.
echo ====================================================================
set /p choice="Enter choice (1-11): "

if "%choice%"=="1" goto LAUNCH_ZCODE
if "%choice%"=="2" goto LAUNCH_CLINE
if "%choice%"=="3" goto LAUNCH_CLAUDE
if "%choice%"=="4" goto LAUNCH_OPENCODE
if "%choice%"=="5" goto LAUNCH_ANTIGRAVITY
if "%choice%"=="6" goto RUN_TRADING_TEST
if "%choice%"=="7" goto RUN_TRADING_MINER
if "%choice%"=="8" goto RUN_TRADING_HARVESTER
if "%choice%"=="9" goto RUN_STORAGE_AUDIT
if "%choice%"=="10" goto VIEW_HANDOFF
if "%choice%"=="11" goto END

:LAUNCH_ZCODE
cls
echo [*] Launching ZCode...
call tools\launch_zcode.bat
goto END

:LAUNCH_CLINE
cls
echo [*] Launching Cline...
call tools\launch_cline.bat
goto END

:LAUNCH_CLAUDE
cls
echo [*] Launching Claude Desktop...
call tools\launch_claude.bat
goto END

:LAUNCH_OPENCODE
cls
echo [*] Launching OpenCode...
call tools\launch_opencode.bat
goto END

:LAUNCH_ANTIGRAVITY
cls
echo [*] Launching Antigravity IDE...
call tools\launch_antigravity.bat
goto END

:RUN_TRADING_TEST
cls
echo [*] Executing Trading Backtest Engine...
python 05_Trading_AI\verifier\test_backtest_engine.py
echo.
pause
goto END

:RUN_TRADING_MINER
cls
echo [*] Executing Trading Strategy Miner...
python 05_Trading_AI\scripts\strategy_miner.py
echo.
pause
goto END

:RUN_TRADING_HARVESTER
cls
echo [*] Executing Historical Data Harvester...
python 05_Trading_AI\scripts\data_harvester.py
echo.
pause
goto END

:RUN_STORAGE_AUDIT
cls
echo [*] Running Storage Management & Portability Audit...
python tools\storage_audit.py
echo.
pause
goto END

:VIEW_HANDOFF
cls
type HANDOFF.md
echo.
pause
goto END

:END
exit
