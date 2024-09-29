@echo off
title Pylar's Bases Tool
setlocal enabledelayedexpansion

:: Function to check if Python is installed and capture its path
:CheckPython
for %%A in (python python3 py) do (
    for /f "usebackq tokens=*" %%P in (`where %%A 2^>nul`) do (
        set "PYTHON_PATH=%%P"
        echo Found Python at !PYTHON_PATH!
        goto :PythonFound
    )
)

:: If Python is not found, download and install it
echo Python not found. Downloading Python...
echo Downloading Python installer...
curl -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

echo Installing Python...
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=0 DefaultAllUsersTargetDir=C:\Python311

:: Clean up
del python_installer.exe

:: Check again if Python is installed after installation
goto CheckPython

:PythonFound
:: Get the Python version
"%PYTHON_PATH%" --version > "python_version.txt" 2>&1
set /p PYTHON_VERSION_TEXT=< "python_version.txt"
echo Python Version: !PYTHON_VERSION_TEXT!
if exist "python_version.txt" del "python_version.txt"

:: Switch to the parent directory of the script
cd /D "%~dp0"

:: Set the path to the Python script
set "SCRIPT_PATH=internal_libs.bases"

:: Ensures pip is installed after checking python is installed already.
python -m ensurepip --upgrade >nul 2>&1

:: Delete import_lock.txt
if exist "import_lock.txt" del "import_lock.txt"

:: Check if the Python script exists
echo Script Path: %SCRIPT_PATH%

:: Execute the Python script using the found Python path
echo Executing bases.py using !PYTHON_PATH!...
"%PYTHON_PATH%" -m internal_libs.bases

:: Open the image file
if exist "updated_worldmap.png" (
    echo Opening updated_worldmap.png...
    start updated_worldmap.png
) else (
    echo updated_worldmap.png not found.
)

pause