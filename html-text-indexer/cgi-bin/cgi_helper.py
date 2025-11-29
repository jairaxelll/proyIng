# -*- coding: utf-8 -*-
"""
CGI Helper for Python 3.13+
Replaces deprecated cgi module functionality
"""

import sys
import os
from urllib.parse import parse_qs
import html as html_escape

class FieldStorage:
    """Replacement for cgi.FieldStorage"""
    def __init__(self):
        self._data = {}
        self._parse_form_data()
    
    def _parse_form_data(self):
        """Parse form data from environment"""
        if os.environ.get('REQUEST_METHOD') == 'POST':
            content_length = int(os.environ.get('CONTENT_LENGTH', 0))
            if content_length > 0:
                post_data = sys.stdin.buffer.read(content_length).decode('utf-8')
                self._data = parse_qs(post_data, keep_blank_values=True)
        elif os.environ.get('REQUEST_METHOD') == 'GET':
            query_string = os.environ.get('QUERY_STRING', '')
            if query_string:
                self._data = parse_qs(query_string, keep_blank_values=True)
    
    def getvalue(self, key, default=None):
        """Get a single value"""
        if key in self._data:
            values = self._data[key]
            return values[0] if values else default
        return default
    
    def getlist(self, key):
        """Get a list of values"""
        return self._data.get(key, [])

def escape(text):
    """Escape HTML characters"""
    return html_escape.escape(str(text))

