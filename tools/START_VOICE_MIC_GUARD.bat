@echo off
title Antigravity Local Wake-Word & Mic Guard
color 0B
echo Starting Antigravity Local Wake-Word Engine...
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0voice_mic_guard.ps1"
pause
