@echo off
title Automated GitHub Pages Deployment
cls
echo ========================================================
echo        AUTOMATED GITHUB PAGES DEPLOYMENT
echo ========================================================
echo.

cd /d "%~dp0\..\03_Active_MVP\frontend"

echo [*] Initializing Git repository in frontend directory...
git init -b main

echo [*] Staging all files...
git add -A

echo [*] Committing build...
git commit -m "Deploy Keepa Clean Excel Converter MVP"

echo.
echo ========================================================
echo [+] Frontend committed locally!
echo ========================================================
