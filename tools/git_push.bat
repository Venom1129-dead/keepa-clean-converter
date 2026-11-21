@echo off
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\gh;%PATH%"
git add -A
git commit -m "Stage MVP 14 activity pack, MVP 15 health vault, and multi-platform publishing guide"
git push origin main
