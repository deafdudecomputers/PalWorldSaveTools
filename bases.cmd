@echo off
title Pylar's Bases Tool *venv*
echo Setting up your environment!

:: Create a virtual environment
python -m venv venv

:: Activate the environment
call venv\Scripts\activate

:: Install the required packages
python -m pip install -r requirements.txt

:: Run the internal_libs.base.py
python -m internal_libs.bases

:: Open the image file
if exist "updated_worldmap.png" (
    echo Opening updated_worldmap.png...
    start updated_worldmap.png
) else (
    echo updated_worldmap.png not found.
)

pause