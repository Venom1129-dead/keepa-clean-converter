@echo off
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\gh;%PATH%"
cd /d "%~dp0\..\03_Active_MVP_11\frontend"

git init -b main
git config user.email "venom1129@gmail.com"
git config user.name "Venom1129-dead"
git add -A
git commit -m "Deploy RetroMemory Hex & CWCheat Address Calculator MVP_11"
gh repo create Venom1129-dead/retro-memory-calc --public --source=. --remote=origin --push
gh api --method POST "repos/Venom1129-dead/retro-memory-calc/pages" -f "source[branch]=main" -f "source[path]=/"
