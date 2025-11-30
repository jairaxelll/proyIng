#!C:/Python313/python.exe
# -*- coding: utf-8 -*-
"""
HTML Text Indexer - Search Handler
Windows-compatible version
"""

import sys
import os
import time
from pathlib import Path

# Python 3.13 compatible - cgi module removed, using alternatives
sys.path.insert(0, str(Path(__file__).parent))
from cgi_helper import FieldStorage, escape

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
        <a href="index.py" class="nav-link">Home</a>
        <a href="activities.py" class="nav-link">Activities</a>
        <a href="search.py" class="nav-link active">Search</a>
        <a href="config.py" class="nav-link">Configuration</a>
    </nav>
"""

def get_search_page(search_word=None, results=None, use_stoplist=False, limit=20):
    """Generate search page"""
    html = """
    <main class="main-content">
        <h2>Search in Dictionary</h2>
        <p>Enter a word to search in the dictionary and posting files.</p>
        
        <form method="POST" action="search.py" class="search-form">
            <div class="form-group">
                <label for="word">Word to search:</label>
                <input type="text" name="word" id="word" value="""" + (escape(search_word) if search_word else "") + """" required class="form-input">
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
            
            <div class="form-actions">
                <button type="submit" name="action" value="search" class="btn btn-primary">Search</button>
                <button type="submit" name="action" value="stress" class="btn btn-secondary">Local Stress Test</button>
            </div>
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
                <p><strong>Found '{escape(search_word)}' in {len(results)} document(s) using {dict_type} dictionary:</strong></p>
                <ol class="results-list">
"""
            limited_results = results[:limit]
            for i, doc in enumerate(limited_results, 1):
                # Each result links to the corresponding HTML file in data/html_sources
                safe_doc = escape(doc)
                html += (
                    f'<li><a href="../data/html_sources/{safe_doc}" '
                    f'target="_blank">{safe_doc}</a></li>'
                )
            
            if len(results) > limit:
                html += f"<li><em>... and {len(results) - limit} more document(s) (limit: {limit} results)</em></li>"
            
            html += """
                </ol>
            </div>
"""
        else:
            html += f"""
            <div class="error-box">
                <p>Word '{escape(search_word)}' not found in the dictionary.</p>
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
    form = FieldStorage()
    
    print("Content-Type: text/html; charset=utf-8\n")
    
    html = get_html_header()
    html += get_navigation()
    
    search_word = form.getvalue('word')
    dict_version = form.getvalue('dict_version', 'no_stoplist')
    limit = int(form.getvalue('limit', 20))
    action = form.getvalue('action', 'search')
    
    use_stoplist = (dict_version == 'with_stoplist')
    results = None
    stress_info = None
    
    if search_word:
        try:
            output_dir = str(script_dir / "results")
            
            if action == "stress":
                # Ejecutar una prueba de estrés local: múltiples búsquedas consecutivas
                iterations = 100  # número de veces que se repetirá la búsqueda
                
                start_time = time.time()
                for _ in range(iterations):
                    main_module.search_word(search_word, output_dir, use_stoplist)
                end_time = time.time()
                
                total_time = end_time - start_time
                avg_time = total_time / iterations if iterations > 0 else 0.0
                
                # Ejecutar una vez más para mostrar los documentos encontrados
                results = main_module.search_word(search_word, output_dir, use_stoplist)
                
                stress_info = {
                    "iterations": iterations,
                    "total_time": total_time,
                    "avg_time": avg_time,
                    "docs_found": len(results) if results else 0,
                }
            else:
                # Búsqueda normal
                results = main_module.search_word(search_word, output_dir, use_stoplist)
        except Exception as e:
            html += f"""
            <main class="main-content">
                <div class="error-box">
                    <h3>Search Error</h3>
                    <p>{escape(str(e))}</p>
                </div>
            </main>
"""
            html += get_html_footer()
            print(html)
            return
    
    html += get_search_page(search_word, results, use_stoplist, limit)
    
    # Si se ejecutó una prueba de estrés, mostrar un resumen debajo de los resultados
    if stress_info is not None:
        html += f"""
        <section class="info-section">
            <h3>Local Stress Test Summary</h3>
            <p><strong>Search term(s):</strong> {escape(search_word)}</p>
            <p><strong>Iterations:</strong> {stress_info['iterations']}</p>
            <p><strong>Total time:</strong> {stress_info['total_time']:.4f} seconds</p>
            <p><strong>Average time per search:</strong> {stress_info['avg_time']*1000:.2f} ms</p>
            <p><strong>Documents found (per search):</strong> {stress_info['docs_found']}</p>
        </section>
        """
    
    html += get_html_footer()
    
    print(html)

if __name__ == "__main__":
    main()

