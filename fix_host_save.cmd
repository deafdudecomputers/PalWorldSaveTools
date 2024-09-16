@echo off
title Pylar's Save Tool
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

:: Switch to script directory
cd /D "%~dp0"

set "SCRIPT_PATH=fix_host_save.py"
:: Check if fix_host_save.py exists
if not exist "%SCRIPT_PATH%" (
    exit /B 1
)

:: Execute the Python script using the found Python path
echo Executing fix_host_save.py using !PYTHON_PATH!...
echo Save Path: %SAVE_PATH%
echo Running: "%PYTHON_PATH%" "%SCRIPT_PATH%" 
set /p NEW_GUID="Enter the new GUID (e.g., 4E6DACB6000000000000000000000000): "
set /p OLD_GUID="Enter the old GUID (e.g., 00000000000000000000000000000001): "
"%PYTHON_PATH%" "%SCRIPT_PATH%" "LocalWorldSave" %NEW_GUID% %OLD_GUID% True
pause
