#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Text Indexer - Activities Handler
Handles activity execution via web interface
"""

import cgi
import cgitb
import sys
import os
import json
from pathlib import Path

# Enable error reporting
cgitb.enable()

# Add parent directory to path
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

import main as main_module

def get_html_header(title="Activities"):
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
            <p class="subtitle">Activities</p>
        </header>
"""

def get_html_footer():
    return """
    </div>
    <footer>
        <p>HTML Text Indexer - CGI Web Application</p>
    </footer>
    <script src="../static/script.js"></script>
</body>
</html>
"""

def get_navigation():
    return """
    <nav class="nav-menu">
        <a href="index.cgi" class="nav-link">Home</a>
        <a href="activities.cgi" class="nav-link active">Activities</a>
        <a href="search.cgi" class="nav-link">Search</a>
        <a href="config.cgi" class="nav-link">Configuration</a>
    </nav>
"""

def get_activities_page():
    """Generate activities page"""
    activities = [
        ("1", "Open HTML Files", "Open and read HTML files, measure loading times"),
        ("2", "Clean HTML", "Remove HTML tags and extract clean text"),
        ("3", "Process Words", "Extract and sort words from cleaned text"),
        ("4", "Consolidate Words", "Create consolidated sorted word list"),
        ("5", "Tokenize", "Tokenize text files for indexing"),
        ("6", "Build Dictionary", "Create dictionary with document frequency"),
        ("7", "Dictionary & Posting", "Generate dictionary and posting lists"),
        ("8", "Hash Table Dictionary", "Build hash table-based dictionary"),
        ("9", "Refine Dictionary", "Remove stop words and filter tokens"),
        ("10", "Weight Tokens", "Calculate TF.IDF weights for tokens"),
        ("11", "Document Index", "Create document index with unique IDs"),
    ]
    
    html = """
    <main class="main-content">
        <h2>Run Activities</h2>
        <p>Select an activity to execute. Activities will run sequentially if multiple are selected.</p>
        
        <form method="POST" action="run_activity.cgi" id="activities-form">
            <div class="activities-grid">
"""
    
    for num, title, desc in activities:
        html += f"""
                <div class="activity-card">
                    <input type="checkbox" name="activity" value="{num}" id="activity-{num}" class="activity-checkbox">
                    <label for="activity-{num}" class="activity-label">
                        <div class="activity-badge">{num}</div>
                        <div class="activity-content">
                            <h4>Activity {num}: {title}</h4>
                            <p>{desc}</p>
                        </div>
                    </label>
                </div>
"""
    
    html += """
            </div>
            
            <div class="form-actions">
                <button type="button" onclick="selectAll()" class="btn btn-secondary">Select All</button>
                <button type="button" onclick="deselectAll()" class="btn btn-secondary">Deselect All</button>
                <button type="button" onclick="selectBasic()" class="btn btn-secondary">Basic (1-4)</button>
                <button type="button" onclick="selectAdvanced()" class="btn btn-secondary">Advanced (5-11)</button>
                <button type="submit" class="btn btn-primary">Run Selected Activities</button>
            </div>
        </form>
        
        <div id="results-area" style="display: none;">
            <h3>Execution Results</h3>
            <div id="results-content" class="results-box"></div>
        </div>
    </main>
"""
    return html

def main():
    """Main handler"""
    form = cgi.FieldStorage()
    
    # If this is a POST request, redirect to run_activity.cgi
    if form.getvalue('activity'):
        print("Content-Type: text/html; charset=utf-8\n")
        print("""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=run_activity.cgi">
</head>
<body>
    <p>Redirecting...</p>
</body>
</html>""")
        return
    
    # Otherwise, show the activities page
    print("Content-Type: text/html; charset=utf-8\n")
    
    html = get_html_header()
    html += get_navigation()
    html += get_activities_page()
    html += get_html_footer()
    
    print(html)

if __name__ == "__main__":
    main()


