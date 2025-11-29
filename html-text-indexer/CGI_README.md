# HTML Text Indexer - CGI Web Application

This document explains how to set up and use the HTML Text Indexer as a CGI-BIN web application.

## Overview

The CGI web application provides a web-based interface for the HTML Text Indexer, allowing you to:
- Run activities through a web browser
- Search the dictionary
- View configuration and system information
- Access all features without a desktop GUI

## Requirements

- Python 3.7 or higher
- Web server with CGI support (Apache, Nginx with FastCGI, etc.)
- Apache mod_cgi enabled (for Apache)
- Write permissions for the `results/` directory

## Installation

### 1. Apache Setup (Recommended)

#### On Linux/Unix:

1. **Install Apache and enable CGI:**
   ```bash
   sudo apt-get install apache2  # Ubuntu/Debian
   sudo yum install httpd        # CentOS/RHEL
   sudo a2enmod cgi             # Enable CGI module
   sudo systemctl restart apache2
   ```

2. **Configure Apache to allow CGI execution:**
   
   Edit `/etc/apache2/sites-available/000-default.conf` (or your site config):
   ```apache
   <Directory /var/www/html/html-text-indexer>
       Options +ExecCGI
       AddHandler cgi-script .cgi .py
       AllowOverride All
       Require all granted
   </Directory>
   ```

3. **Set proper permissions:**
   ```bash
   chmod +x cgi-bin/*.cgi
   chmod 755 cgi-bin/
   chmod 755 static/
   ```

4. **Copy or link the project:**
   ```bash
   sudo cp -r /path/to/html-text-indexer /var/www/html/
   # OR create a symlink
   sudo ln -s /path/to/html-text-indexer /var/www/html/html-text-indexer
   ```

#### On Windows (XAMPP/WAMP):

1. **Install XAMPP or WAMP**
2. **Place project in `htdocs` folder:**
   ```
   C:\xampp\htdocs\html-text-indexer\
   ```
3. **Edit `httpd.conf` to enable CGI:**
   ```apache
   LoadModule cgi_module modules/mod_cgi.so
   ScriptAlias /cgi-bin/ "C:/xampp/htdocs/html-text-indexer/cgi-bin/"
   <Directory "C:/xampp/htdocs/html-text-indexer/cgi-bin">
       AllowOverride All
       Options +ExecCGI
       AddHandler cgi-script .cgi .py
       Require all granted
   </Directory>
   ```
4. **Restart Apache**

### 2. Python CGI Setup

1. **Make CGI scripts executable:**
   ```bash
   chmod +x cgi-bin/*.cgi
   ```

2. **Update Python path in CGI scripts if needed:**
   - Edit each `.cgi` file
   - Update the `#!/usr/bin/env python3` shebang if Python is in a different location
   - On Windows, you may need: `#!C:/Python3/python.exe`

3. **Test Python CGI:**
   Create a test file `cgi-bin/test.cgi`:
   ```python
   #!/usr/bin/env python3
   print("Content-Type: text/html\n")
   print("<h1>CGI Works!</h1>")
   ```
   Access: `http://localhost/html-text-indexer/cgi-bin/test.cgi`

## Directory Structure

```
html-text-indexer/
├── cgi-bin/              # CGI scripts
│   ├── index.cgi        # Main page
│   ├── activities.cgi   # Activities page
│   ├── run_activity.cgi # Activity runner
│   ├── search.cgi       # Search interface
│   └── config.cgi       # Configuration page
├── static/              # Static files
│   ├── style.css       # Stylesheet
│   └── script.js       # JavaScript
├── .htaccess           # Apache configuration
├── main.py             # Main module (imported by CGI)
├── data/               # Data files
└── results/            # Output directory
```

## Usage

### Accessing the Application

1. **Start your web server** (if not already running)
2. **Open a web browser** and navigate to:
   ```
   http://localhost/html-text-indexer/cgi-bin/index.cgi
   ```
   Or if using a virtual host:
   ```
   http://your-domain.com/html-text-indexer/cgi-bin/index.cgi
   ```

### Running Activities

1. Click on **"Activities"** in the navigation menu
2. Select one or more activities using checkboxes
3. Click **"Run Selected Activities"**
4. Wait for execution to complete
5. View results in the browser

### Searching

1. Click on **"Search"** in the navigation menu
2. Enter a word to search
3. Select dictionary version (with/without stoplist)
4. Set results limit
5. Click **"Search"**
6. View documents containing the word

### Configuration

1. Click on **"Configuration"** in the navigation menu
2. View current paths and settings
3. Verify that all required directories exist

## Troubleshooting

### CGI Scripts Not Executing

**Problem:** Scripts download instead of executing

**Solutions:**
- Check file permissions: `chmod +x cgi-bin/*.cgi`
- Verify Apache CGI module is enabled: `a2enmod cgi`
- Check `.htaccess` file is present and correct
- Verify `AddHandler cgi-script .cgi` is in Apache config

### Python Path Issues

**Problem:** "Command not found" or Python errors

**Solutions:**
- Update shebang line in CGI scripts: `#!/usr/bin/env python3`
- On some systems: `#!/usr/bin/python3`
- Check Python location: `which python3`
- Update `PYTHONPATH` in `.htaccess` if needed

### Permission Denied

**Problem:** Cannot write to results directory

**Solutions:**
```bash
chmod 755 results/
chmod 755 data/
# Or set ownership to web server user
chown www-data:www-data results/ data/
```

### Import Errors

**Problem:** Cannot import main module

**Solutions:**
- Verify `main.py` is in the parent directory of `cgi-bin/`
- Check `sys.path.insert(0, str(script_dir))` in CGI scripts
- Verify Python can access the directory

### 500 Internal Server Error

**Problem:** Server error when accessing CGI scripts

**Solutions:**
- Check Apache error logs: `/var/log/apache2/error.log`
- Enable CGI error reporting (already enabled in scripts)
- Verify file permissions
- Check Python syntax: `python3 -m py_compile cgi-bin/*.cgi`

## Security Considerations

1. **File Permissions:**
   - CGI scripts should be executable but not writable by others
   - Data directories should have appropriate permissions
   - Never expose sensitive files

2. **Input Validation:**
   - All user input is sanitized using `cgi.escape()`
   - File paths are validated to prevent directory traversal

3. **Access Control:**
   - Consider adding authentication for production use
   - Use HTTPS in production
   - Restrict access to sensitive directories

4. **Error Reporting:**
   - `cgitb.enable()` is enabled for debugging
   - Disable in production or limit error visibility

## Alternative: Using Python's Built-in HTTP Server (Development Only)

For testing without Apache:

```bash
cd html-text-indexer
python3 -m http.server 8000 --cgi
```

Then access: `http://localhost:8000/cgi-bin/index.cgi`

**Note:** This is for development only. Use a proper web server (Apache/Nginx) for production.

## Support

For issues or questions:
1. Check Apache error logs
2. Verify file permissions
3. Test CGI scripts individually
4. Review Python error messages in browser

## License

Same as the main HTML Text Indexer project.


