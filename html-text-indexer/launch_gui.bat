@echo off
REM HTML Text Indexer - GUI Launcher
REM Double-click this file to launch the GUI

echo Starting HTML Text Indexer GUI...
echo.
echo Installing/updating CustomTkinter if needed...
pip install -q customtkinter>=5.2.0
echo.
python gui.py

REM If there's an error, keep the window open
if %errorlevel% neq 0 (
    echo.
    echo Error launching GUI. Make sure Python is installed.
    echo If CustomTkinter is missing, run: pip install customtkinter
    echo Press any key to exit...
    pause >nul
)

