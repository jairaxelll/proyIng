# Windows Setup Guide - CGI Web Application

## Quick Fix for Windows

The issue you're experiencing is that Windows can't execute `.cgi` files directly. I've created `.py` versions that work on Windows.

## How to Use (Windows)

1. **Stop the current server** (if running) - Press `Ctrl+C` in the terminal

2. **Start the server again:**
   ```cmd
   cd html-text-indexer
   python -m http.server 8000 --cgi
   ```

3. **Open your browser and use `.py` URLs instead:**
   - **Home:** `http://localhost:8000/cgi-bin/index.py`
   - **Test:** `http://localhost:8000/cgi-bin/test.py`
   - **Activities:** `http://localhost:8000/cgi-bin/activities.py`
   - **Search:** `http://localhost:8000/cgi-bin/search.py`
   - **Config:** `http://localhost:8000/cgi-bin/config.py`

## What Changed

I created Windows-compatible `.py` versions of all scripts:
- `index.py` - Main page
- `activities.py` - Activities page
- `search.py` - Search page
- `config.py` - Configuration page
- `run_activity.py` - Activity runner
- `test.py` - Test script

These use Windows-compatible shebangs (`#!C:/Python313/python.exe`) and all links point to `.py` files.

## Alternative: Use the Batch File

You can also use the provided batch file:
1. Double-click `start_web_server.bat`
2. Open `http://localhost:8000/cgi-bin/index.py`

## Why This Happens

Windows doesn't recognize Unix shebangs (`#!/usr/bin/env python3`) in `.cgi` files. Python's HTTP server on Windows needs `.py` files to execute properly.

## For Production (Apache/XAMPP)

If you're using Apache or XAMPP, you can configure it to handle `.cgi` files properly. See `CGI_README.md` for Apache setup instructions.


