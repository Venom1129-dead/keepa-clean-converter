@echo off
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\gh;%PATH%"
git add -A
git commit -m "Implement Trading AI empirical testing suite, 9 SKILL.md specs, and universal portability system"
git push origin main
