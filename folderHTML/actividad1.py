import os
from bs4 import BeautifulSoup
import time



folder = 'folderHTML/Files'

def open_file(filename):
    file_path = os.path.join(folder, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.prettify()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                soup = BeautifulSoup(file, 'html.parser')
                return soup.prettify()
        except Exception as e:
            return f"Failed to open {filename}: {e}"



def create_log_file():
    total_open_time = 0
    function_start = time.time()
    output_lines = []
    for filename in os.listdir(folder):
        if filename.endswith('.html'):
            start_time = time.time()
            _ = open_file(filename)  # Not writing prettified HTML to file, just timing
            end_time = time.time()
            elapsed_time = end_time - start_time
            total_open_time += elapsed_time
            output_lines.append(f"{filename} - {elapsed_time:.2f} seconds")
    function_end = time.time()
    total_function_time = function_end - function_start
    output_lines.append(f"Total time opening all files: {total_open_time:.2f} seconds")
    output_lines.append(f"Total execution time: {total_function_time:.2f} seconds")
    with open('folderHTML/timing_results.txt', 'w', encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + '\n')



create_log_file()

