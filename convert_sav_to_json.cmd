@echo off
title Pylar's Auto Convert Tool *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Run the convertids.py script
python convert.py "Level.sav."

pause