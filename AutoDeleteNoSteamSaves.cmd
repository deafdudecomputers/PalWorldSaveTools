@echo off
title Pylar's Auto Delete NoSteam Saves *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Run the AutoDeleteNoSteamSaves.py script
python AutoDeleteNoSteamSaves.py

pause