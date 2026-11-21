@echo off
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%PATH%"
cd /d "%~dp0\..\03_Active_MVP_09\frontend"
git add -A
git commit -m "Add in-game live Dev Mode inspector"
git push origin main
