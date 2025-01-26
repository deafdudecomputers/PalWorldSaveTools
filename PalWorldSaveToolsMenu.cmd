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
echo Checking and installing required modules...
python -m pip install -r requirements.txt

:: Define tools
set "tools[1]=Convert Level.sav file to Level.json"
set "tools[2]=Convert Level.json file back to Level.sav"
set "tools[3]=Convert Player files to json format"
set "tools[4]=Convert Player files back to sav format"
set "tools[5]=Convert Game Pass Save to Steam Save"
set "tools[6]=Convert Steam Save to Game Pass Save"
set "tools[7]=Convert SteamID"
set "tools[8]=Convert Coordinates"
set "tools[9]=Slot Injector"
set "tools[10]=Modify Save"
set "tools[11]=Scan Save"
set "tools[12]=Generate Map"
set "tools[13]=Transfer Character"
set "tools[14]=Delete Inactive Players Saves"
set "tools[15]=Delete Players Saves by Pals amount"
set "tools[16]=Generate palguard killnearestbase commands"
set "tools[17]=Reset/Update PalWorldSaveTools"
set "tools[18]=About PalWorldSaveTools"
set "tools[19]=PalWorldSaveTools Usage"
set "tools[20]=PalWorldSaveTools Readme"
set "tools[21]=Exit"

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
type logo.txt
echo.
echo v!tools_version! - Working as of v!game_version! Patch
echo.
echo WARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!
echo.
echo ==================================================================================

:: Dynamically group tools based on their range
echo ==================================================================================
echo.                         Converting Tools
echo ==================================================================================
for /L %%i in (1,1,8) do echo %%i. !tools[%%i]!
echo ==================================================================================
echo.                         Management Tools
echo ==================================================================================
for /L %%i in (9,1,13) do echo %%i. !tools[%%i]!
echo ==================================================================================
echo.                         Cleaning Tools
echo ==================================================================================
for /L %%i in (14,1,16) do echo %%i. !tools[%%i]!
echo ==================================================================================
echo.                         PalWorldSaveTools
echo ==================================================================================
for /L %%i in (17,1,21) do echo %%i. !tools[%%i]!
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

set /p "choice=Select what you want to do (1-%max_choice%): "
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
    title Loading Pylar's Convert Player Files Tool
    cls
    python convert_players_location_finder.py json
    pause
) else if "%selected_tool%" == "!tools[4]!" (
    title Loading Pylar's Convert Player Files Tool
    cls
    python convert_players_location_finder.py sav
    pause
) else if "%selected_tool%" == "!tools[5]!" (
    title Loading Pylar's Game Pass Save Convert Tool
    cls
    python game_pass_save_fix.py
    pause
) else if "%selected_tool%" == "!tools[6]!" (
    title Loading Fr33dan's Game Pass Save Converter...
    cls
    python gamepass_save_converter.py
    pause
) else if "%selected_tool%" == "!tools[7]!" (
    title Loading Pylar's Convert SteamID Tool...
    cls
    python convertids.py
    pause
) else if "%selected_tool%" == "!tools[8]!" (
    title Loading Pylar's Convert Coordinates Tool...
    cls
    python coords.py
    pause
) else if "%selected_tool%" == "!tools[9]!" (
    title Loading Pylar's Slot Injector Tool...
    cls
    python slot_injector.py
    pause
) else if "%selected_tool%" == "!tools[10]!" (
    title Loading oMaN-Rod's Save Editor...
    cls
    python palworld_save_pal.py
    pause
) else if "%selected_tool%" == "!tools[11]!" (
    title Loading Pylar's Scan Save...
    cls
    if exist "scan_save.log" del "scan_save.log"
    if exist "players.log" del "players.log"
    if exist "sort_players.log" del "sort_players.log"
    if exist "Pal Logger" rmdir /s /q "Pal Logger"
    if exist "import_lock.txt" del "import_lock.txt"
    if exist "PalWorldSave/Level.sav" (
        python scan_save.py PalWorldSave/Level.sav
    ) else (
        echo Error: PalWorldSave/Level.sav not found!
    )
    pause
) else if "%selected_tool%" == "!tools[12]!" (
    title Loading Pylar's Generate Map Tool...
    cls
    python -m internal_libs.bases
    if exist "updated_worldmap.png" (
        echo Opening updated_worldmap.png...
        start updated_worldmap.png
    ) else (
        echo updated_worldmap.png not found.
    )
    pause
) else if "%selected_tool%" == "!tools[13]!" (
    title Loading Pylar's Transfer Character Tool...
    cls
    python character_transfer.py
    pause
) else if "%selected_tool%" == "!tools[14]!" (
    title Loading Pylar's Delete Inactive Players Saves Tool...
    cls
    python delete_inactive_players.py players.log
    pause
) else if "%selected_tool%" == "!tools[15]!" (
    title Loading Pylar's Delete Players Saves by Pals amount Tool...
    cls
    python delete_pals_save.py players.log
    pause
) else if "%selected_tool%" == "!tools[16]!" (
    title Loading Pylar's Generate Palguard Commands Tool...
    cls
    python palguard_bases.py
    pause
) else if "%selected_tool%" == "!tools[17]!" (
    title Resetting/Updating PalWorldSaveTools...
    cls
    python -m ensurepip --upgrade >nul 2>&1
    git init >nul 2>&1
    git remote remove origin >nul 2>&1
    git remote add origin https://github.com/deafdudecomputers/PalWorldSaveTools.git
    echo Replacing all files in the current directory with the latest from GitHub...
    git fetch --all
    git reset --hard origin/main
    git clean -fdx
    rmdir /s /q .git
    echo Update complete. All files have been replaced.    
    start "" "%~f0"
    exit
) else if "%selected_tool%" == "!tools[18]!" (
    title About PalWorldSaveTools...
    cls
    echo ==================================================================================
    echo.
    type logo.txt
    echo.
    echo v!tools_version! - Working as of v!game_version! Patch
    echo.
    echo WARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!
    echo.
    echo ==================================================================================
    echo PalWorldSaveTools, all in one tools that helps fix/transfer/edit/etc for PalWorld saves.
    echo Author: MagicBear and cheahjs
    echo License: MIT License
    echo Updated by: Pylar and Techdude
    echo Map Pictures Provided by: Kozejin
    echo Testers/Helpers: Lethe and xKillerMaverick
    echo The UI was made by xKillerMaverick
    echo Contact me on Discord: Pylar1991
    pause
) else if "%selected_tool%" == "!tools[19]!" (
    title PalWorldSaveTools Usage:
    cls
    echo ==================================================================================
    echo.
    type logo.txt
    echo.
    echo v!tools_version! - Working as of v!game_version! Patch
    echo.
    echo WARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!
    echo.
    echo ==================================================================================
    echo Some options may require you to use PalWorldSave folder, so place your saves in that folder.
    echo If you encounter some errors, make sure to run Scan Save first.
    echo Then repeat the previous option to see if it fixes the previous error.
    echo If everything else fails, you may contact me on Discord: Pylar1991
    echo Or raise an issue on my github: https://github.com/deafdudecomputers/PalWorldSaveTools
    pause
) else if "%selected_tool%" == "!tools[20]!" (
    start README.md
) else if "%selected_tool%" == "!tools[21]!" (
    exit
)
goto :eof