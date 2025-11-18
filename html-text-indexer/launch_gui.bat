@echo off
REM HTML Text Indexer - GUI Launcher
REM Double-click this file to launch the GUI

echo Starting HTML Text Indexer GUI...
python gui.py

REM If there's an error, keep the window open
if %errorlevel% neq 0 (
    echo.
    echo Error launching GUI. Make sure Python and tkinter are installed.
    echo Press any key to exit...
    pause >nul
)

