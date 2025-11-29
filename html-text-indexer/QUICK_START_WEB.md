# Quick Start Guide - Web Application

## Testing the CGI Web Application

### Method 1: Python Built-in Server (Easiest - Recommended for Testing)

This is the simplest way to test the web application without installing Apache.

#### On Windows:

1. **Double-click** `start_web_server.bat`
   - OR open Command Prompt/PowerShell in the project folder and run:
   ```cmd
   python -m http.server 8000 --cgi
   ```

2. **Open your web browser** and go to:
   ```
   http://localhost:8000/cgi-bin/index.cgi
   ```

3. **Test CGI is working:**
   ```
   http://localhost:8000/cgi-bin/test.cgi
   ```
   You should see "✓ CGI is Working!"

#### On Linux/Mac:

1. **Make the script executable:**
   ```bash
   chmod +x start_web_server.sh
   ```

2. **Run the script:**
   ```bash
   ./start_web_server.sh
   ```
   OR:
   ```bash
   python3 -m http.server 8000 --cgi
   ```

3. **Open your web browser** and go to:
   ```
   http://localhost:8000/cgi-bin/index.cgi
   ```

### Method 2: Using XAMPP (Windows)

If you have XAMPP installed:

1. **Copy the project** to:
   ```
   C:\xampp\htdocs\html-text-indexer\
   ```

2. **Edit** `C:\xampp\apache\conf\httpd.conf`:
   - Find and uncomment: `LoadModule cgi_module modules/mod_cgi.so`
   - Add or modify:
   ```apache
   ScriptAlias /cgi-bin/ "C:/xampp/htdocs/html-text-indexer/cgi-bin/"
   <Directory "C:/xampp/htdocs/html-text-indexer/cgi-bin">
       AllowOverride All
       Options +ExecCGI
       AddHandler cgi-script .cgi .py
       Require all granted
   </Directory>
   ```

3. **Start Apache** from XAMPP Control Panel

4. **Access:**
   ```
   http://localhost/html-text-indexer/cgi-bin/index.cgi
   ```

### Method 3: Using Apache (Linux/Production)

For production use, see `CGI_README.md` for detailed Apache setup instructions.

## Troubleshooting

### "CGI scripts download instead of executing"

**Solution:**
- Make sure you're using `--cgi` flag: `python -m http.server 8000 --cgi`
- Check file permissions (Linux/Mac): `chmod +x cgi-bin/*.cgi`

### "500 Internal Server Error"

**Solution:**
- Check Python path in CGI scripts (first line: `#!/usr/bin/env python3`)
- On Windows, you might need to change to: `#!C:/Python3/python.exe`
- Check error logs in browser or terminal

### "Module not found" errors

**Solution:**
- Make sure `main.py` is in the parent directory of `cgi-bin/`
- Verify the path in CGI scripts: `script_dir = Path(__file__).parent.parent`

### "Permission denied" errors

**Solution (Linux/Mac):**
```bash
chmod +x cgi-bin/*.cgi
chmod 755 cgi-bin/
```

## What to Test

1. **Home Page:** `http://localhost:8000/cgi-bin/index.cgi`
   - Should show welcome page with navigation

2. **Activities:** `http://localhost:8000/cgi-bin/activities.cgi`
   - Select activities and run them
   - Check results appear

3. **Search:** `http://localhost:8000/cgi-bin/search.cgi`
   - Enter a word (e.g., "the", "and")
   - Select dictionary version
   - View search results

4. **Configuration:** `http://localhost:8000/cgi-bin/config.cgi`
   - View system paths and status

## Next Steps

Once testing works with Python's built-in server:
- For production, set up Apache (see `CGI_README.md`)
- Configure proper file permissions
- Set up authentication if needed
- Use HTTPS for production


