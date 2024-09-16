#!/bin/bash

# Function to check if Python is installed and capture its path
check_python() {
    for cmd in python python3 py; do
        if command -v "$cmd" &> /dev/null; then
            PYTHON_PATH=$(command -v "$cmd")
            echo "Found Python at $PYTHON_PATH"
            return
        fi
    done

    # If Python is not found, download and install it
    echo "Python not found. Downloading Python..."
    echo "Downloading Python installer..."
    wget -O python_installer.deb "https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.deb"

    echo "Installing Python..."
    sudo dpkg -i python_installer.deb
    sudo apt-get install -f -y

    # Clean up
    rm python_installer.deb

    # Check again if Python is installed after installation
    check_python
}

check_python

# Get the Python version
"$PYTHON_PATH" --version > "python_version.txt" 2>&1
PYTHON_VERSION_TEXT=$(< "python_version.txt")
echo "Python Version: $PYTHON_VERSION_TEXT"
rm "python_version.txt"

# Switch to script directory
SCRIPT_DIR="$(dirname "$0")"
echo "Switching to script directory: $SCRIPT_DIR"
cd "$SCRIPT_DIR" || { echo "Failed to change directory to $SCRIPT_DIR"; exit 1; }

SCRIPT_PATH="fix_save.py"

# Check if fix_save.py exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "fix_save.py not found in $SCRIPT_DIR"
    exit 1
fi

# Check if Level.sav exists
LEVEL_SAV_PATH="Level.sav"
if [ ! -f "$LEVEL_SAV_PATH" ]; then
    echo "Level.sav not found in $SCRIPT_DIR"
    exit 1
fi

# Clean up old log files
echo "Cleaning up old log files..."
rm -f fix_save.log players.log sort_players.log

# Delete the Pal Logger folder and its contents
if [ -d "Pal Logger" ]; then
    echo "Deleting Pal Logger folder..."
    rm -rf "Pal Logger"
fi

# Execute the Python script using the found Python path
echo "Executing fix_save.py using $PYTHON_PATH..."
"$PYTHON_PATH" "$SCRIPT_PATH" "$LEVEL_SAV_PATH"
