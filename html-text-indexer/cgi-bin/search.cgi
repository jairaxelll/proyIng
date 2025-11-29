#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Text Indexer - Search Handler
Handles word search in dictionary
"""

import cgi
import cgitb
import sys
from pathlib import Path

# Enable error reporting
cgitb.enable()

# Add parent directory to path
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

import main as main_module

def get_html_header(title="Search"):
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
            <p class="subtitle">Search Dictionary</p>
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
        <a href="index.cgi" class="nav-link">Home</a>
        <a href="activities.cgi" class="nav-link">Activities</a>
        <a href="search.cgi" class="nav-link active">Search</a>
        <a href="config.cgi" class="nav-link">Configuration</a>
    </nav>
"""

def get_search_page(search_word=None, results=None, use_stoplist=False, limit=20):
    """Generate search page"""
    html = """
    <main class="main-content">
        <h2>Search in Dictionary</h2>
        <p>Enter a word to search in the dictionary and posting files.</p>
        
        <form method="POST" action="search.cgi" class="search-form">
            <div class="form-group">
                <label for="word">Word to search:</label>
                <input type="text" name="word" id="word" value="""" + (cgi.escape(search_word) if search_word else "") + """" required class="form-input">
            </div>
            
            <div class="form-group">
                <label>Dictionary version:</label>
                <div class="radio-group">
                    <label>
                        <input type="radio" name="dict_version" value="no_stoplist" """ + ("checked" if not use_stoplist else "") + """>
                        Full dictionary (without stoplist - Activity 8)
                    </label>
                    <label>
                        <input type="radio" name="dict_version" value="with_stoplist" """ + ("checked" if use_stoplist else "") + """>
                        Filtered dictionary (with stoplist - Activity 9)
                    </label>
                </div>
            </div>
            
            <div class="form-group">
                <label>Results limit:</label>
                <select name="limit" class="form-select">
                    <option value="5" """ + ("selected" if limit == 5 else "") + """>5</option>
                    <option value="10" """ + ("selected" if limit == 10 else "") + """>10</option>
                    <option value="20" """ + ("selected" if limit == 20 else "") + """>20</option>
                    <option value="50" """ + ("selected" if limit == 50 else "") + """>50</option>
                    <option value="100" """ + ("selected" if limit == 100 else "") + """>100</option>
                </select>
            </div>
            
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
"""
    
    if search_word and results is not None:
        html += """
        <div class="results-section">
            <h3>Search Results</h3>
"""
        if results:
            dict_type = "filtered (with stoplist)" if use_stoplist else "full (without stoplist)"
            html += f"""
            <div class="success-box">
                <p><strong>Found '{cgi.escape(search_word)}' in {len(results)} document(s) using {dict_type} dictionary:</strong></p>
                <ol class="results-list">
"""
            limited_results = results[:limit]
            for i, doc in enumerate(limited_results, 1):
                html += f"<li>{cgi.escape(doc)}</li>"
            
            if len(results) > limit:
                html += f"<li><em>... and {len(results) - limit} more document(s) (limit: {limit} results)</em></li>"
            
            html += """
                </ol>
            </div>
"""
        else:
            html += f"""
            <div class="error-box">
                <p>Word '{cgi.escape(search_word)}' not found in the dictionary.</p>
                <p>Please try:</p>
                <ul>
                    <li>Checking the spelling</li>
                    <li>Using a different dictionary (with/without stoplist)</li>
                    <li>Searching for a different word</li>
                </ul>
            </div>
"""
        html += "</div>"
    
    html += """
    </main>
"""
    return html

def main():
    """Main handler"""
    form = cgi.FieldStorage()
    
    print("Content-Type: text/html; charset=utf-8\n")
    
    html = get_html_header()
    html += get_navigation()
    
    search_word = form.getvalue('word')
    dict_version = form.getvalue('dict_version', 'no_stoplist')
    limit = int(form.getvalue('limit', 20))
    
    use_stoplist = (dict_version == 'with_stoplist')
    results = None
    
    if search_word:
        try:
            output_dir = str(script_dir / "results")
            results = main_module.search_word(search_word, output_dir, use_stoplist)
        except Exception as e:
            html += f"""
            <main class="main-content">
                <div class="error-box">
                    <h3>Search Error</h3>
                    <p>{cgi.escape(str(e))}</p>
                </div>
            </main>
"""
            html += get_html_footer()
            print(html)
            return
    
    html += get_search_page(search_word, results, use_stoplist, limit)
    html += get_html_footer()
    
    print(html)

if __name__ == "__main__":
    main()


