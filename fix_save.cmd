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

set "SCRIPT_PATH=fix_save.py"
:: Check if fix_save.py exists
if not exist "%SCRIPT_PATH%" (
    exit /B 1
)

:: Clean up old log files
if exist "fix_save.log" del "fix_save.log"
if exist "players.log" del "players.log"
if exist "sort_players.log" del "sort_players.log"

:: Delete import_lock.txt
if exist "import_lock.txt" del "import_lock.txt"

:: Delete the Pal Logger folder and its contents
if exist "Pal Logger" rmdir /s /q "Pal Logger"

:: Ensures pip is installed after checking python is installed already.
python -m ensurepip --upgrade >nul 2>&1

:: Execute the Python script using the found Python path
echo Executing fix_save.py using !PYTHON_PATH!...
"%PYTHON_PATH%" "%SCRIPT_PATH%" "Level.sav"

:: Check if Level.sav was found
if exist "Level.sav" (
    echo Would you like to delete saves of:
    echo 1. Both
    echo 2. Pals
    echo 3. Players
    echo 4. None
    set /p choice="Enter the number of your choice: "
    if "!choice!"=="1" (
        echo Executing delete_pals_save.cmd...
        call delete_pals_save.cmd
        echo Executing sort_players.cmd...
        call sort_players.cmd
    ) else if "!choice!"=="2" (
        echo Executing delete_pals_save.cmd...
        call delete_pals_save.cmd
    ) else if "!choice!"=="3" (
        echo Executing sort_players.cmd...
        call sort_players.cmd
    ) else if "!choice!"=="4" (
        echo Exiting.
        exit /b 0
    ) else (
        echo Invalid choice. Exiting.
        exit /b 1
    )
) else (
    echo Level.sav does not exist. Skipping choices.
)
pause