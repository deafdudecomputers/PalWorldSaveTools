@echo off
title Pylar's Auto Delete Pals Saves Tool *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Prompt for maximum number of pals
set /p max_pals=Enter maximum number of pals per player to delete: 

:: Execute delete_pals_save.py using the Python from the virtual environment
python delete_pals_save.py players.log %max_pals%

pause