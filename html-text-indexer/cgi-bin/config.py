#!C:/Python313/python.exe
# -*- coding: utf-8 -*-
"""
HTML Text Indexer - Configuration Handler
Windows-compatible version
"""

import sys
from pathlib import Path

# Python 3.13 compatible - cgi module removed, using alternatives
# No form handling needed for config page

# Add parent directory to path
script_dir = Path(__file__).parent.parent

def get_html_header(title="Configuration"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../static/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>HTML Text Indexer</h1>
            <p class="subtitle">Configuration</p>
        </header>
"""

def get_html_footer():
    return """
    </div>
    <footer>
        <p>HTML Text Indexer - CGI Web Application</p>
    </footer>
</body>
</html>
"""

def get_navigation():
    return """
    <nav class="nav-menu">
        <a href="index.py" class="nav-link">Home</a>
        <a href="activities.py" class="nav-link">Activities</a>
        <a href="search.py" class="nav-link">Search</a>
        <a href="config.py" class="nav-link active">Configuration</a>
    </nav>
"""

def get_config_page():
    """Generate configuration page"""
    html_sources = script_dir / "data" / "html_sources"
    results_dir = script_dir / "results"
    stoplist_file = script_dir / "stoplist.txt"
    
    html = """
    <main class="main-content">
        <h2>Configuration</h2>
        <p>Current system paths and settings:</p>
        
        <div class="config-section">
            <h3>Paths</h3>
            <div class="config-grid">
                <div class="config-item">
                    <strong>Project Directory:</strong>
                    <code>""" + str(script_dir) + """</code>
                </div>
                <div class="config-item">
                    <strong>HTML Sources Directory:</strong>
                    <code>""" + str(html_sources) + """</code>
                    <span class="status """ + ("exists" if html_sources.exists() else "missing") + """">
                        """ + ("✓ Exists" if html_sources.exists() else "✗ Missing") + """
                    </span>
                </div>
                <div class="config-item">
                    <strong>Results Directory:</strong>
                    <code>""" + str(results_dir) + """</code>
                    <span class="status """ + ("exists" if results_dir.exists() else "missing") + """">
                        """ + ("✓ Exists" if results_dir.exists() else "✗ Missing") + """
                    </span>
                </div>
                <div class="config-item">
                    <strong>Stoplist File:</strong>
                    <code>""" + str(stoplist_file) + """</code>
                    <span class="status """ + ("exists" if stoplist_file.exists() else "missing") + """">
                        """ + ("✓ Exists" if stoplist_file.exists() else "✗ Missing") + """
                    </span>
                </div>
            </div>
        </div>
        
        <div class="info-section">
            <h3>Configuration Notes</h3>
            <ul>
                <li><strong>HTML Sources:</strong> Directory containing the HTML files to process</li>
                <li><strong>Results:</strong> Directory where all output files and reports will be saved</li>
                <li><strong>Stoplist:</strong> Text file containing stop words (one per line) for filtering</li>
            </ul>
            <p><em>Note: To change these paths, modify the configuration in the CGI scripts or update the environment variables.</em></p>
        </div>
    </main>
"""
    return html

def main():
    """Main handler"""
    print("Content-Type: text/html; charset=utf-8\n")
    
    html = get_html_header()
    html += get_navigation()
    html += get_config_page()
    html += get_html_footer()
    
    print(html)

if __name__ == "__main__":
    main()

