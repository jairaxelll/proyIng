import os
import time
from pathlib import Path

FOLDER = 'folderHTML/Files'

def open_file(file_path):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"Failed to open {file_path.name}: {e}"
    
    return f"Failed to decode {file_path.name} with any encoding"

def create_log_file():

    folder_path = Path(FOLDER)
    
    if not folder_path.exists():
        print(f"Folder {FOLDER} does not exist")
        return
    
    total_open_time = 0
    function_start = time.time()
    output_lines = []
    
    html_files = list(folder_path.glob('*.html'))
    
    if not html_files:
        print("No HTML files found in folder")
        return
    
    for file_path in html_files:
        start_time = time.time()
        content = open_file(file_path)  
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        total_open_time += elapsed_time
        output_lines.append(f"{file_path.name} - {elapsed_time:.4f} seconds")
    
    function_end = time.time()
    total_function_time = function_end - function_start
    
    output_lines.extend([
        "",
        f"Files processed: {len(html_files)}",
        f"Total time opening all files: {total_open_time:.4f} seconds",
        f"Average time per file: {total_open_time/len(html_files):.4f} seconds",
        f"Total execution time: {total_function_time:.4f} seconds"
    ])
    
    output_path = Path('folderHTML/timing_results.txt')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"Results written to {output_path}")
    print(f"Processed {len(html_files)} files in {total_function_time:.4f} seconds")

if __name__ == "__main__":
    create_log_file()