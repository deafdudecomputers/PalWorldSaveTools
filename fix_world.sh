#!/bin/bash
echo "Pylar's Fix World Tool"

# Function to check if Python is installed and capture its path
check_python() {
    for cmd in python3 python py; do
        PYTHON_PATH=$(which "$cmd" 2>/dev/null)
        if [ -n "$PYTHON_PATH" ]; then
            echo "Found Python at $PYTHON_PATH"
            return
        fi
    done

    # If Python is not found, download and install it
    echo "Python not found. Downloading Python..."
    echo "Downloading Python installer..."
    curl -o python_installer.sh https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz

    echo "Installing Python..."
    tar -xzf python_installer.sh
    cd Python-3.12.4
    ./configure
    make
    sudo make install
    cd ..
    rm -rf Python-3.12.4 python_installer.sh

    # Check again if Python is installed after installation
    check_python
}

check_python

# Get the Python version
PYTHON_VERSION_TEXT=$("$PYTHON_PATH" --version 2>&1)
echo "Python Version: $PYTHON_VERSION_TEXT"

# Switch to script directory
cd "$(dirname "$0")"

# Check if fix_save.py exists
if [ ! -f "fix_save.py" ]; then
    exit 1
fi

# Clean up old log files
[ -f "fix_save.log" ] && rm "fix_save.log"
[ -f "players.log" ] && rm "players.log"
[ -f "sort_players.log" ] && rm "sort_players.log"

# Delete the Pal Logger folder and its contents
[ -d "Pal Logger" ] && rm -rf "Pal Logger"

clear

echo "Executing fix_save.py using $PYTHON_PATH..."
"$PYTHON_PATH" fix_save.py "$1"
