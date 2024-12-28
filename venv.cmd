@echo off
title Pylar's Save Tool *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Update pip to the latest version
python -m pip install --upgrade pip

:: Install the required packages
python -m pip install -r requirements.txt

:: Run the fix_save.cmd
.\fix_save.cmd
