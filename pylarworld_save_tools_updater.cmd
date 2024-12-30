@echo off
title Pylar's Automated PalWorldSaveTools Updater
git init >nul 2>&1
git remote remove origin >nul 2>&1
git remote add origin https://github.com/deafdudecomputers/PalWorldSaveTools.git
echo Replacing all files in the current directory with the latest from GitHub...
git fetch --all
git reset --hard origin/main
git clean -fdx
rd /s /q .git
echo Update complete. All files have been replaced.
pause
