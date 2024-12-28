@echo off
title Pylar's Automated PalWorldSaveTools Updater
set "current_dir=%cd%"
if exist "PalWorldSaveTools" (
    echo Updating PalWorldSaveTools...
    cd PalWorldSaveTools
    git pull
    cd ..
) else (
    echo Cloning PalWorldSaveTools to a temporary directory...
    git clone https://github.com/deafdudecomputers/PalWorldSaveTools.git Temp_PalWorldSaveTools
)
echo Replacing files in the current directory...
xcopy "Temp_PalWorldSaveTools\*" "%current_dir%\" /E /H /C /Y
:: Clean up the temporary folder if used
if exist "Temp_PalWorldSaveTools" (
    echo Cleaning up temporary files...
    rmdir /S /Q "Temp_PalWorldSaveTools"
)
echo Update complete.
pause
