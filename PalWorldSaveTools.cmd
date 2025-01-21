@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: Set PalWorldSaveTools Directory
set "PalWorldSaveToolsDir=%~dp0PalWorldSaveTools"

:: Navigate to PalWorldSaveTools
cd /d "%PalWorldSaveToolsDir%"

:: Customize Window
title PalWorldSaveTools Setup
echo Setting up your environment!

:: Create the PalWorldSave folder if it doesn't exist
if not exist "PalWorldSave" (
    mkdir "PalWorldSave"
    mkdir "PalWorldSave/Players"
    echo PalWorldSave folder and its subdirectories have been created.
)

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Display Menu
call PalWorldSaveToolsMenu.cmd