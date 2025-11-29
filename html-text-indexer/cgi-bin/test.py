#!C:/Python313/python.exe
# -*- coding: utf-8 -*-
"""
Test CGI script to verify CGI is working
Windows-compatible version
"""

print("Content-Type: text/html; charset=utf-8\n")
print("""
<!DOCTYPE html>
<html>
<head>
    <title>CGI Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .success { color: green; font-size: 24px; }
    </style>
</head>
<body>
    <h1 class="success">✓ CGI is Working!</h1>
    <p>If you can see this page, CGI is properly configured.</p>
    <p><a href="index.py">Go to HTML Text Indexer</a></p>
</body>
</html>
""")


