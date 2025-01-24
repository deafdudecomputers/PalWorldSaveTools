@echo off
setlocal EnableExtensions EnableDelayedExpansion
title PalWorldSaveTools
echo Setting up your environment...

:: Create necessary directories if they don't exist
if not exist "PalWorldSave\Players" (
    mkdir "PalWorldSave\Players"
    echo PalWorldSave and Players directories created.
)

:: Set up virtual environment and install dependencies
python -m venv venv
call venv\Scripts\activate
echo Installing required modules...
python -m pip install -r requirements.txt

:: Define tools
set "tools[1]=Convert Level.sav file to Level.json"
set "tools[2]=Convert Level.json file back to Level.sav"
set "tools[3]=Convert Player files to json format"
set "tools[4]=Convert Player files back to sav format"
set "tools[5]=Convert Game Pass Save to Steam Save"
set "tools[6]=Convert Steam Save to Game Pass Save"
set "tools[7]=Slot Injector"
set "tools[8]=Modify Save"
set "tools[9]=Scan Save"
set "tools[10]=Generate Map"
set "tools[11]=Fix Host Save"
set "tools[12]=Transfer Character"
set "tools[13]=Convert Steam ID"
set "tools[14]=Convert Coordinates"
set "tools[15]=Delete Inactive Players Saves"
set "tools[16]=Delete Players Saves by Pals amount"
set "tools[17]=Generate palguard killnearestbase commands"
set "tools[18]=Update PalWorldSaveTools"
set "tools[19]=About PalWorldSaveTools"
set "tools[20]=Exit"

:: Main menu
:mainMenu
cls
set "version_file=version.txt"
set "tools_version="
set "game_version="
for /f "tokens=2 delims==" %%a in ('findstr "ToolsVersion" %version_file%') do set "tools_version=%%a"
for /f "tokens=2 delims==" %%a in ('findstr "GameVersion" %version_file%') do set "game_version=%%a"

:: Set the title with version information
title PalWorldSaveTools v!tools_version! (Working as of v!game_version! Patch)

echo ==================================================================================
echo.
echo PalWorldSaveTools v!tools_version! (Working as of v!game_version! Patch)
echo.
echo WARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!
echo.
echo ==================================================================================
echo.

:: Dynamically group tools based on their range
echo ==================================================================================
echo.                         Save Converting Tools
echo ==================================================================================
for /L %%i in (1,1,6) do echo %%i. !tools[%%i]!
echo ==================================================================================
echo.                         Save Management Tools
echo ==================================================================================
for /L %%i in (7,1,14) do echo %%i. !tools[%%i]!
echo ==================================================================================
echo.                         Save Cleaning Tools
echo ==================================================================================
for /L %%i in (15,1,17) do echo %%i. !tools[%%i]!
echo ==================================================================================
echo.                         Program Management
echo ==================================================================================
for /L %%i in (18,1,20) do echo %%i. !tools[%%i]!
echo ==================================================================================

:: Automatically list max choices
set /a max_choice=0
set "index=1"
:countTools
if defined tools[%index%] (
    set /a max_choice+=1
    set /a index+=1
    goto countTools
)

echo Select what you want to do (1-%max_choice%):
set /p "choice=Enter your choice: "
if not defined choice goto mainMenu

:: Process user choice
call :processChoice %choice%
goto mainMenu

:processChoice
set "selected_tool=!tools[%1]!"

:: Dynamic execution based on selected tool
if "%selected_tool%" == "!tools[1]!" (
    title Loading Pylar's Convert Save Tool
    cls
    python convert_level_location_finder.py json
    pause
) else if "%selected_tool%" == "!tools[2]!" (
    title Loading Pylar's Convert Save Tool
    cls
    python convert_level_location_finder.py sav
    pause
) else if "%selected_tool%" == "!tools[3]!" (
    title Loading Pylar's Convert Save Tool
    cls
    python convert_players_location_finder.py json
    pause
) else if "%selected_tool%" == "!tools[4]!" (
    title Loading Pylar's Convert Save Tool
    cls
    python convert_players_location_finder.py sav
    pause
) else if "%selected_tool%" == "!tools[5]!" (
    title Loading Pylar's Game Pass Save Convert Tool - Based on Z1ni Scripts...
    cls
    python game_pass_save_fix.py
    pause
) else if "%selected_tool%" == "!tools[6]!" (
    title Loading Fr33dan's Game Pass Save Converter...
    cls
    python gamepass_save_converter.py
    pause
) else if "%selected_tool%" == "!tools[7]!" (
    title Loading Pylar's Save Tool...
    cls
    python slot_injector.py
    pause
) else if "%selected_tool%" == "!tools[8]!" (
    title Loading oMaN-Rod's Save Editor...
    cls
    python palworld_save_pal.py
    pause
) else if "%selected_tool%" == "!tools[9]!" (
    title Loading Pylar's Save Tool
    cls
    if exist "fix_save.log" del "fix_save.log"
    if exist "players.log" del "players.log"
    if exist "sort_players.log" del "sort_players.log"
    if exist "Pal Logger" rmdir /s /q "Pal Logger"
    if exist "import_lock.txt" del "import_lock.txt"
    if exist "PalWorldSave/Level.sav" (
        python fix_save.py PalWorldSave/Level.sav
    ) else (
        echo Error: PalWorldSave/Level.sav not found!
    )
    pause
) else if "%selected_tool%" == "!tools[10]!" (
    title Loading Pylar's Map Maker Tool...
    cls
    python -m internal_libs.bases
    if exist "updated_worldmap.png" (
        echo Opening updated_worldmap.png...
        start updated_worldmap.png
    ) else (
        echo updated_worldmap.png not found.
    )
    pause
) else if "%selected_tool%" == "!tools[11]!" (
    title Loading Pylar's Save Tool...
    cls
    python fix_host_save.py PalWorldSave
    pause
) else if "%selected_tool%" == "!tools[12]!" (
    title Loading Pylar's Save Tool...
    cls
    python character_transfer.py
    pause
) else if "%selected_tool%" == "!tools[13]!" (
    title Loading Pylar's Save Tool...
    cls
    python convertids.py
    pause
) else if "%selected_tool%" == "!tools[14]!" (
    title Loading Pylar's Convert Tool
    cls
    python coords.py
    pause
) else if "%selected_tool%" == "!tools[15]!" (
    title Loading Pylar's Save Tool...
    cls
    python sort_players.py players.log
    pause
) else if "%selected_tool%" == "!tools[16]!" (
    title Loading Pylar's Save Tool
    cls
    python delete_pals_save.py players.log
    pause
) else if "%selected_tool%" == "!tools[17]!" (
    title Loading Pylar's Save Tool...
    cls
    python palguard_bases.py
    pause
) else if "%selected_tool%" == "!tools[18]!" (
    title Updating PalWorldSaveTools...
    cls
    python -m ensurepip --upgrade >nul 2>&1
    git init >nul 2>&1
    git remote remove origin >nul 2>&1
    git remote add origin https://github.com/deafdudecomputers/PalWorldSaveTools.git
    echo Replacing all files in the current directory with the latest from GitHub...
    git fetch --all
    git reset --hard origin/main
    git clean -fdx
    echo Update complete. All files have been replaced.    
    start "" "%~f0"
    exit
) else if "%selected_tool%" == "!tools[19]!" (
    title About PalWorldSaveTools...
    cls
    echo PalWorldSaveTools - Save Converting, Management, and Cleaning Tools for PalWorld.
    echo Author: MagicBear and cheahjs
    echo License: MIT License
    echo Updated by: Pylar and Techdude
    echo Map Pictures Provided by: Kozejin
    echo Testers/Helpers: Lethe and xKillerMaverick
    echo The UI was made by xKillerMaverick
    pause
) else if "%selected_tool%" == "!tools[20]!" (
    exit
)
goto :eof