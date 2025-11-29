#!C:/Python313/python.exe
# -*- coding: utf-8 -*-
"""
HTML Text Indexer - Activity Runner
Windows-compatible version
"""

import sys
import os
from pathlib import Path
from io import StringIO
import contextlib

# Python 3.13 compatible - cgi module removed, using alternatives
sys.path.insert(0, str(Path(__file__).parent))
from cgi_helper import FieldStorage, escape

# Add parent directory to path
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

import main as main_module

def get_html_header(title="Running Activity"):
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
            <p class="subtitle">Activity Execution</p>
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
        <a href="config.py" class="nav-link">Configuration</a>
    </nav>
"""

def run_activity(activity_num):
    """Run a specific activity"""
    results = []
    errors = []
    
    try:
        # Capture stdout
        output = StringIO()
        
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            if activity_num == "1":
                main_module.actividad1()
            elif activity_num == "2":
                main_module.actividad2()
            elif activity_num == "3":
                main_module.actividad3()
            elif activity_num == "4":
                main_module.actividad4()
            elif activity_num == "5":
                input_dir = str(script_dir / "data" / "html_sources")
                output_dir = str(script_dir / "results")
                main_module.actividad5(input_dir, output_dir)
            elif activity_num == "6":
                input_dir = str(script_dir / "data" / "html_sources")
                output_dir = str(script_dir / "results")
                main_module.actividad6(input_dir, output_dir)
            elif activity_num == "7":
                output_dir = str(script_dir / "results")
                main_module.actividad7(output_dir)
            elif activity_num == "8":
                output_dir = str(script_dir / "results")
                main_module.actividad8(output_dir)
            elif activity_num == "9":
                output_dir = str(script_dir / "results")
                stoplist_path = str(script_dir / "stoplist.txt")
                main_module.actividad9(output_dir, stoplist_path)
            elif activity_num == "10":
                output_dir = str(script_dir / "results")
                main_module.actividad10(output_dir)
            elif activity_num == "11":
                output_dir = str(script_dir / "results")
                main_module.actividad11(output_dir)
            else:
                errors.append(f"Unknown activity: {activity_num}")
                return results, errors
        
        output_text = output.getvalue()
        results.append(f"Activity {activity_num} completed successfully")
        results.append(output_text)
        
    except Exception as e:
        errors.append(f"Error running activity {activity_num}: {str(e)}")
        import traceback
        errors.append(traceback.format_exc())
    
    return results, errors

def main():
    """Main handler"""
    form = FieldStorage()
    
    print("Content-Type: text/html; charset=utf-8\n")
    
    html = get_html_header()
    html += get_navigation()
    
    # Get selected activities
    activities = form.getlist('activity')
    
    if not activities:
        html += """
        <main class="main-content">
            <div class="error-box">
                <h3>No Activities Selected</h3>
                <p>Please go back and select at least one activity to run.</p>
                <a href="activities.py" class="btn btn-primary">Go Back</a>
            </div>
        </main>
"""
    else:
        html += """
        <main class="main-content">
            <h2>Running Activities</h2>
            <div class="results-box">
"""
        
        all_results = []
        all_errors = []
        
        for activity_num in activities:
            html += f"<h3>Running Activity {activity_num}...</h3>"
            
            results, errors = run_activity(activity_num)
            all_results.extend(results)
            all_errors.extend(errors)
            
            if errors:
                html += f"<div class='error-box'><h4>Errors in Activity {activity_num}:</h4>"
                for error in errors:
                    # Escape HTML and preserve formatting
                    escaped_error = escape(str(error)).replace('\n', '<br>')
                    html += f"<pre>{escaped_error}</pre>"
                html += "</div>"
            else:
                html += f"<div class='success-box'><h4>Activity {activity_num} Completed:</h4>"
                for result in results:
                    # Escape HTML and preserve formatting
                    escaped_result = escape(str(result)).replace('\n', '<br>')
                    html += f"<pre>{escaped_result}</pre>"
                html += "</div>"
        
        html += """
            </div>
            <div class="form-actions">
                <a href="activities.py" class="btn btn-primary">Run More Activities</a>
                <a href="index.py" class="btn btn-secondary">Home</a>
            </div>
        </main>
"""
    
    html += get_html_footer()
    print(html)

if __name__ == "__main__":
    main()

