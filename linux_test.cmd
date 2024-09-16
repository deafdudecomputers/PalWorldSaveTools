@echo off
setlocal

:: Automatically set the script path
set "WINDOWS_SCRIPT_PATH=%~dp0fix_save.sh"
set "WSL_SCRIPT_PATH=/mnt/c%WINDOWS_SCRIPT_PATH:~2%"
set "WSL_SCRIPT_PATH=%WSL_SCRIPT_PATH:\=/%

:: Change to the directory where the script is located
cd /d "%~dp0"

:: Display paths for debugging
echo WINDOWS_SCRIPT_PATH=%WINDOWS_SCRIPT_PATH%
echo WSL_SCRIPT_PATH=%WSL_SCRIPT_PATH%

:: Run sed to convert line endings
wsl sed -i 's/\r$//' "%WSL_SCRIPT_PATH%"

:: Make the script executable
wsl chmod +x "%WSL_SCRIPT_PATH%"

echo Script %WSL_SCRIPT_PATH% has been made executable.

:: Execute the shell script using WSL
wsl bash "%WSL_SCRIPT_PATH%"

pause