@echo off
:: Save current installed packages to requirements.txt
pip freeze > requirements.txt

:: Uninstall all packages listed in requirements.txt
pip uninstall -r requirements.txt -y

:: Optional: Delete requirements.txt after uninstalling
del requirements.txt

echo Uninstallation complete.

pip list

pause