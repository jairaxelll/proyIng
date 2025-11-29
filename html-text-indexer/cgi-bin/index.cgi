#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Text Indexer - CGI Web Application
Main entry point for the web interface
"""

import cgi
import cgitb
import sys
import os
from pathlib import Path

# Enable error reporting for debugging
cgitb.enable()

# Add parent directory to path to import main module
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

# Import main module
import main as main_module

def get_html_header(title="HTML Text Indexer"):
    """Generate HTML header"""
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
            <p class="subtitle">Professional Text Processing & Indexing System</p>
        </header>
"""

def get_html_footer():
    """Generate HTML footer"""
    return """
    </div>
    <footer>
        <p>HTML Text Indexer - CGI Web Application</p>
    </footer>
</body>
</html>
"""

def get_navigation():
    """Generate navigation menu"""
    return """
    <nav class="nav-menu">
        <a href="index.cgi" class="nav-link active">Home</a>
        <a href="activities.cgi" class="nav-link">Activities</a>
        <a href="search.cgi" class="nav-link">Search</a>
        <a href="config.cgi" class="nav-link">Configuration</a>
    </nav>
"""

def get_main_page():
    """Generate main page content"""
    return """
    <main class="main-content">
        <div class="welcome-section">
            <h2>Welcome to HTML Text Indexer</h2>
            <p>This web application allows you to process and index HTML files through a series of activities.</p>
        </div>
        
        <div class="quick-actions">
            <h3>Quick Actions</h3>
            <div class="action-grid">
                <a href="activities.cgi" class="action-card">
                    <h4>Run Activities</h4>
                    <p>Execute processing activities (1-11)</p>
                </a>
                <a href="search.cgi" class="action-card">
                    <h4>Search Dictionary</h4>
                    <p>Search for words in indexed documents</p>
                </a>
                <a href="config.cgi" class="action-card">
                    <h4>Configuration</h4>
                    <p>Configure paths and settings</p>
                </a>
            </div>
        </div>
        
        <div class="info-section">
            <h3>System Information</h3>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Project Directory:</strong>
                    <span id="project-dir">""" + str(script_dir) + """</span>
                </div>
                <div class="info-item">
                    <strong>HTML Sources:</strong>
                    <span id="html-sources">""" + str(script_dir / "data" / "html_sources") + """</span>
                </div>
                <div class="info-item">
                    <strong>Results Directory:</strong>
                    <span id="results-dir">""" + str(script_dir / "results") + """</span>
                </div>
            </div>
        </div>
    </main>
"""

def main():
    """Main CGI handler"""
    # Set content type
    print("Content-Type: text/html; charset=utf-8\n")
    
    # Generate and output HTML
    html = get_html_header()
    html += get_navigation()
    html += get_main_page()
    html += get_html_footer()
    
    print(html)

if __name__ == "__main__":
    main()


