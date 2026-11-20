@echo off
title Setup Free API in Codex CLI
cls
echo ========================================================
echo       CONNECT FREE GPT API KEY TO CODEX CLI
echo ========================================================
echo.
echo Your ChatGPT Web subscription reached its limit until Nov 24.
echo You can use Codex CLI right now with free API keys from:
echo.
echo  1. GitHub Models (Free GPT-4o / GPT-4o-mini with GitHub token)
echo     Base URL: https://models.inference.ai.azure.com
echo.
echo  2. OpenRouter (Free DeepSeek, Qwen 2.5 Coder, GPT free tiers)
echo     Base URL: https://openrouter.ai/api/v1
echo.
echo  3. Google AI Studio (Free Gemini Flash with OpenAI compatibility)
echo     Base URL: https://generativelanguage.googleapis.com/v1beta/openai/
echo.
echo  4. Direct OpenAI API Key (if you have one)
echo.
echo ========================================================
echo.
set /p API_KEY="Enter your API Key: "
set /p BASE_URL="Enter Base URL (Press Enter for default OpenAI): "

if "%BASE_URL%"=="" (
    set OPENAI_BASE_URL=https://api.openai.com/v1
) else (
    set OPENAI_BASE_URL=%BASE_URL%
)

set OPENAI_API_KEY=%API_KEY%

echo.
echo [*] Logging Codex CLI in with your API Key...
echo %API_KEY% | "C:\Program Files\WindowsApps\OpenAI.Codex_26.1117.3838.0_x64__2p2nqsd0c76g0\app\resources\codex.exe" login --with-api-key

echo.
echo [+] Done! You can now run Codex CLI without waiting for Nov 24.
echo.
pause
