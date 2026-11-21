@echo off
title Autonomous Perpetual Income Daemon
color 0A
cls
cd /d "%~dp0\.."

echo ========================================================
echo     AUTONOMOUS PERPETUAL WORKER DAEMON LAUNCHER
echo ========================================================
echo [*] Starting continuous background worker loop...
echo [*] Logs will be written to: 00_Brain\memory\findings\autonomous_loop.log
echo.
python tools\autonomous_worker_loop.py
pause
