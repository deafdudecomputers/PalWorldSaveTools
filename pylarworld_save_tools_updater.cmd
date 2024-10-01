@echo off
title Pylar's Automated PalWorldSaveTools Updater
if exist "PalWorldSaveTools" (
    echo Updating PalWorldSaveTools...
    cd PalWorldSaveTools
    git pull
    cd ..
) else (
    echo Cloning PalWorldSaveTools...
    git clone https://github.com/deafdudecomputers/PalWorldSaveTools.git
)
pause