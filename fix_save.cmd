@echo off
title Pylar's Save Tool *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Delete old files from previous runs
if exist "fix_save.log" del "fix_save.log"
if exist "players.log" del "players.log"
if exist "sort_players.log" del "sort_players.log"
if exist "Pal Logger" rmdir /s /q "Pal Logger"
if exist "import_lock.txt" del "import_lock.txt"

:: Run the fix_save.py with Level.sav
python fix_save.py Level.sav

pause