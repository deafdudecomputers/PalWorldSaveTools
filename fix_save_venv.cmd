@echo off
title Pylar's Save Tool *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Run the fix_save.py with Level.sav
python fix_save.py Level.sav

pause
