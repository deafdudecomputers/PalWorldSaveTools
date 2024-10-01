@echo off
title Pylar's Auto Pip Installer
setlocal enabledelayedexpansion

:: Download get-pip.py
curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py

:: Install pip
python get-pip.py

:: Remove the downloaded file
del get-pip.py

:: Check pip version
python -m pip --version

pip list

pause