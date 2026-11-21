@echo off
setlocal

REM =========================================================================
REM RUN WEB AI HANDS BRIDGE
REM Autonomous AI Income Factory — Task ID: aii-mwqh5uqm-15a517
REM =========================================================================

echo [*] Starting Web AI Hands Execution Bridge...
python "%~dp0web_ai_hands_bridge.py" %*

exit /b %ERRORLEVEL%
