@echo off
title Pylar's Convert X Y tool
setlocal enabledelayedexpansion

REM Define constants
set "transl_x=123888"
set "transl_y=158000"
set "scale=459"

REM Convert .sav to in-game coordinates
echo --- Convert .sav to In-Game Coordinates ---
set /p "sav_x=Enter .sav X coordinate: "
set /p "sav_y=Enter .sav Y coordinate: "

REM Translate and scale
set /a "temp_x= sav_x + transl_x"
set /a "temp_y= sav_y - transl_y"

REM Use PowerShell for floating-point division and rounding
for /f "tokens=* usebackq" %%a in (`powershell -command "[math]::Round((%temp_y% / %scale%), 0)"`) do set "in_game_x=%%a"
for /f "tokens=* usebackq" %%a in (`powershell -command "[math]::Round((%temp_x% / %scale%), 0)"`) do set "in_game_y=%%a"

echo In-game coordinates: X = %in_game_x%, Y = %in_game_y%
echo.

REM Convert in-game to .sav coordinates
echo --- Convert In-Game to .sav Coordinates ---
set /p "game_x=Enter in-game X coordinate: "
set /p "game_y=Enter in-game Y coordinate: "

REM Scale and translate
set /a "temp_x_sav = game_x * scale"
set /a "temp_y_sav = game_y * scale"

REM Use PowerShell for floating-point division and rounding
for /f "tokens=* usebackq" %%a in (`powershell -command "[math]::Round((%temp_y_sav% - %transl_x%), 0)"`) do set "sav_x_out=%%a"
for /f "tokens=* usebackq" %%a in (`powershell -command "[math]::Round((%temp_x_sav% + %transl_y%), 0)"`) do set "sav_y_out=%%a"

echo .sav coordinates: X = %sav_x_out%, Y = %sav_y_out%
echo.

endlocal
pause
