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