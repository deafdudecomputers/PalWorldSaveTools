@echo off
title Pylar's Auto Clean Tool
setlocal enabledelayedexpansion

:: Clean up all .log files
del /q *.log >nul 2>&1
echo All logs have been deleted.

:: Delete the Pal Logger folder and its contents
if exist "Pal Logger" rmdir /s /q "Pal Logger" >nul 2>&1
echo Pal Logger folder and all contents within have been deleted.

:: Delete the Players folder and its contents
if exist "Players" rmdir /s /q "Players" >nul 2>&1
echo Players folder and all contents within have been deleted.

:: Delete everything in external_libs except for palworld_save_tools
if exist "external_libs" (
    pushd "external_libs"
    for /d %%D in (*) do (
        if /i not "%%~nxD"=="palworld_save_tools" (
            rmdir /s /q "%%D" >nul 2>&1
        )
    )
    for %%F in (*) do (
        if /i not "%%~nxF"=="palworld_save_tools" (
            del /q "%%F" >nul 2>&1
        )
    )
    popd
    echo All contents except palworld_save_tools have been deleted from external_libs.
)

:: Delete everything in internal_libs except .py files
if exist "internal_libs" (
    pushd "internal_libs"
    for %%F in (*) do (
        if /i not "%%~xF"==".py" (
            del /q "%%F" >nul 2>&1
        )
    )
    popd
    echo All non-.py files have been deleted from internal_libs.
)

:: Delete the LocalWorldSave folder and its contents
if exist "LocalWorldSave" rmdir /s /q "LocalWorldSave" >nul 2>&1
echo LocalWorldSave folder and all contents within have been deleted.

:: Recreate the LocalWorldSave folder
mkdir "LocalWorldSave"
echo New LocalWorldSave folder has been created.

:: Create a new Players folder
mkdir "Players"
echo New Players folder has been created.

:: Delete all .sav files
del /q *.sav >nul 2>&1
echo All .sav files have been deleted.

:: Delete all .json files
del /q *.json >nul 2>&1
echo All .json files have been deleted.

:: Delete all .csv files
del /q *.csv >nul 2>&1
echo All .csv files have been deleted.

:: Delete all .png files
del /q *.png >nul 2>&1
echo All .png files have been deleted.

:: Detect and delete all __pycache__ folders recursively
for /r %%D in (__pycache__) do (
    if exist "%%D" rmdir /s /q "%%D" >nul 2>&1
)
echo All __pycache__ folders has been deleted.

echo Everything's all cleaned.
pause
