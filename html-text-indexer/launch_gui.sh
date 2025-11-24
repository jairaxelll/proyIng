#!/bin/bash
# HTML Text Indexer - GUI Launcher
# Run this file to launch the GUI

echo "Starting HTML Text Indexer GUI..."
echo ""
echo "Installing/updating CustomTkinter if needed..."
pip3 install -q customtkinter>=5.2.0
echo ""
python3 gui.py

# If there's an error, show message
if [ $? -ne 0 ]; then
    echo ""
    echo "Error launching GUI. Make sure Python is installed."
    echo "If CustomTkinter is missing, run: pip3 install customtkinter"
    read -p "Press Enter to exit..."
fi

