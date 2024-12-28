@echo off
title Pylar's Auto Delete Players Saves Tool
echo Setting up your environment!

:: Enable delayed variable expansion
setlocal enabledelayedexpansion

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Prompt for days and level
set /p days=Enter the number of days: 
set /p level=Enter the level: 

:: Execute sort_players.py using the Python from the virtual environment
python sort_players.py players.log !days! !level!

pause
