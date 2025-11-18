#!/bin/bash
# HTML Text Indexer - GUI Launcher
# Run this file to launch the GUI

echo "Starting HTML Text Indexer GUI..."
python3 gui.py

# If there's an error, show message
if [ $? -ne 0 ]; then
    echo ""
    echo "Error launching GUI. Make sure Python and tkinter are installed."
    echo "On Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "On macOS: tkinter should be included with Python"
    read -p "Press Enter to exit..."
fi

