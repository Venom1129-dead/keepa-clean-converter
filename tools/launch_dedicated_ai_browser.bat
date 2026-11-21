@echo off
setlocal enabledelayedexpansion

REM =========================================================================
REM DEDICATED AI BROWSER LAUNCHER
REM Autonomous AI Income Factory — Task ID: aii-mwqh5uqm-15a517
REM
REM Isolation Invariant (Safety Constraint R5 & R7):
REM - Uses dedicated user data directory: %LOCALAPPDATA%\AIIncome_Dedicated_Browser
REM - Does NOT touch or disrupt your primary personal browsing session/cookies
REM - Binds CDP strictly to localhost (127.0.0.1) on port 9222
REM =========================================================================

set "DATA_DIR=%LOCALAPPDATA%\AIIncome_Dedicated_Browser"
set "DEBUG_PORT=9222"
set "DEBUG_ADDR=127.0.0.1"

if not exist "%DATA_DIR%" (
    mkdir "%DATA_DIR%"
)

echo [*] Dedicated AI Profile: %DATA_DIR%
echo [*] Remote Debugging Address: %DEBUG_ADDR%:%DEBUG_PORT% (Localhost Only)

REM Detect Chrome or Edge executable
set "BROWSER_EXE="

if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
) else if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER_EXE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
)

if "%BROWSER_EXE%"=="" (
    echo [!] ERROR: Could not locate Google Chrome or Microsoft Edge.
    exit /b 1
)

echo [*] Launching Browser: %BROWSER_EXE%

REM Payment & Payout Setup Tabs
set "URL_PAY_1=https://gumroad.com/settings/payouts"
set "URL_PAY_2=https://gumroad.com/products/new"
set "URL_PAY_3=https://www.paypal.com/signin"
set "URL_PAY_4=https://kdp.amazon.com/"
set "URL_PAY_5=https://printify.com/app/dashboard"

REM 7 Target Web AI Tabs
set "URL_AI_1=https://gemini.google.com/app"
set "URL_AI_2=https://chatgpt.com/"
set "URL_AI_3=https://claude.ai/new"
set "URL_AI_4=https://chat.deepseek.com/"
set "URL_AI_5=https://chat.z.ai/"
set "URL_AI_6=https://chat.qwen.ai/"
set "URL_AI_7=https://agent.minimax.io/"

start "" "%BROWSER_EXE%" ^
    --user-data-dir="%DATA_DIR%" ^
    --remote-debugging-port=%DEBUG_PORT% ^
    --remote-debugging-address=%DEBUG_ADDR% ^
    --no-first-run ^
    --no-default-browser-check ^
    --window-size=1380,950 ^
    "%URL_PAY_1%" "%URL_PAY_2%" "%URL_PAY_3%" "%URL_PAY_4%" "%URL_PAY_5%" ^
    "%URL_AI_1%" "%URL_AI_2%" "%URL_AI_3%" "%URL_AI_4%" "%URL_AI_5%" "%URL_AI_6%" "%URL_AI_7%"

echo [+] Dedicated AI Browser successfully launched on %DEBUG_ADDR%:%DEBUG_PORT%.
echo [+] Preloaded tabs: Gumroad Payouts, Products, PayPal, Amazon KDP, Printify + 7 Web AIs.
exit /b 0
