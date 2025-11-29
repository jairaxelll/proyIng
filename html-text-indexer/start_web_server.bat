@echo off
REM Start Python HTTP Server with CGI support for HTML Text Indexer
echo ========================================
echo HTML Text Indexer - Web Server
echo ========================================
echo.
echo Starting web server on http://localhost:8000
echo.
echo Open your browser and go to:
echo   http://localhost:8000/cgi-bin/index.cgi
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
python -m http.server 8000 --cgi
pause


