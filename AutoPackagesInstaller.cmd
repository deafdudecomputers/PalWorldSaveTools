@echo off
title Pylar's Automated Packages Updater
setlocal
set "packages=msgpack palworld_coord psutil palworld_save_tools matplotlib pandas cityhash"
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python and try again.
    exit /b 1
)
for %%P in (%packages%) do (
    echo Installing %%P...
    python -m pip install %%P --no-cache-dir
    if errorlevel 1 (
        echo Failed to install %%P. Aborting.
        exit /b 1
    )
)
echo All packages installed successfully!
endlocal
pause
