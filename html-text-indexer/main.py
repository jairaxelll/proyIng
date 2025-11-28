import os
import time
import re
import sys
import argparse
from pathlib import Path
from collections import Counter
import html

# Default folder for backward compatibility
# Use relative path based on script location
_script_dir = Path(__file__).parent
FOLDER = str(_script_dir / "data" / "html_sources")

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

def actividad1():
    print("=== EJECUTANDO ACTIVIDAD 1: ABRIR ARCHIVOS HTML ===")
    
    folder_path = Path(FOLDER)
    
    if not folder_path.exists():
        print(f"Folder {FOLDER} does not exist")
        return
    
    program_start = time.time()
    
    html_files = list(folder_path.glob('*.html'))
    
    if not html_files:
        print("No HTML files found in folder")
        return
    
    log_lines = []
    total_opening_time = 0
    successful_files = 0
    
    log_lines.append("=== ACTIVIDAD 1: REPORTE DE APERTURA DE ARCHIVOS HTML ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio: {FOLDER}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 60)
    
    for html_file in html_files:
        file_start = time.time()
        
        content = open_file(html_file)
        
        file_end = time.time()
        opening_time = file_end - file_start
        
        if not content.startswith("Failed"):
            successful_files += 1
            total_opening_time += opening_time
            file_size = html_file.stat().st_size
            log_lines.append(f"{html_file.name:<25} {opening_time:.6f}s  {file_size:>8} bytes")
            print(f"Abierto: {html_file.name} en {opening_time:.6f} segundos")
        else:
            log_lines.append(f"{html_file.name:<25} ERROR: {content}")
            print(f"Error: {html_file.name} - {content}")
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "",
        "=== ESTADÍSTICAS ===",
        f"Total archivos encontrados: {len(html_files)}",
        f"Archivos abiertos exitosamente: {successful_files}",
        f"Tiempo total abriendo archivos: {total_opening_time:.6f} segundos",
        f"Tiempo promedio por archivo: {total_opening_time/successful_files if successful_files > 0 else 0:.6f} segundos",
        f"Tiempo total del programa: {total_program_time:.6f} segundos",
        f"Tiempo del programa: {total_program_time - total_opening_time:.6f} segundos"
    ])
    
    log_path = Path('results/reports/activity_1_file_opening.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 1 completada.")
    print(f"Reporte guardado en: {log_path}")
    print(f"Archivos procesados: {successful_files}/{len(html_files)}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def remove_html_tags(filename):
    file_path = Path(FOLDER) / filename
    
    if not file_path.exists():
        print(f"El archivo {filename} no existe en {FOLDER}")
        return 0
    
    start_time = time.time()
    
    content = open_file(file_path)
    
    if content.startswith("Failed"):
        print(f"Error al leer {filename}: {content}")
        return 0
    
    clean_content = re.sub(r'<[^>]+>', '', content)
    clean_content = html.unescape(clean_content)
    clean_content = re.sub(r'\s+', ' ', clean_content)
    clean_content = clean_content.strip()
    
    output_folder = Path('data/extracted_text')
    output_folder.mkdir(exist_ok=True)
    
    clean_filename = file_path.stem + '_clean.txt'
    output_path = output_folder / clean_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return processing_time

def actividad2():
    print("=== EJECUTANDO ACTIVIDAD 2: ELIMINAR ETIQUETAS HTML ===")
    
    folder_path = Path(FOLDER)
    
    if not folder_path.exists():
        print(f"Folder {FOLDER} does not exist")
        return
    
    program_start = time.time()
    
    html_files = list(folder_path.glob('*.html'))
    
    if not html_files:
        print("No HTML files found in folder")
        return
    
    log_lines = []
    total_processing_time = 0
    successful_files = 0
    
    log_lines.append("=== ACTIVIDAD 2: REPORTE DE ELIMINACIÓN DE ETIQUETAS HTML ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio: {FOLDER}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 60)
    
    for html_file in html_files:
        processing_time = remove_html_tags(html_file.name)
        
        if processing_time > 0:
            successful_files += 1
            total_processing_time += processing_time
            log_lines.append(f"{html_file.name:<30} {processing_time:.6f} segundos")
            print(f"Procesado: {html_file.name} en {processing_time:.6f} segundos")
        else:
            log_lines.append(f"{html_file.name:<30} ERROR")
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "",
        "=== ESTADÍSTICAS ===",
        f"Total archivos encontrados: {len(html_files)}",
        f"Archivos procesados exitosamente: {successful_files}",
        f"Tiempo total procesando archivos: {total_processing_time:.6f} segundos",
        f"Tiempo promedio por archivo: {total_processing_time/successful_files if successful_files > 0 else 0:.6f} segundos",
        f"Tiempo total del programa: {total_program_time:.6f} segundos",
        f"Overhead del programa: {total_program_time - total_processing_time:.6f} segundos",
        "",
        f"Archivos limpios guardados en: ./data/extracted_text/"
    ])
    
    log_path = Path('results/reports/activity_2_html_cleaning.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 2 completada.")
    print(f"Reporte guardado en: {log_path}")
    print(f"Archivos limpios guardados en: ./data/extracted_text/")
    print(f"Archivos procesados: {successful_files}/{len(html_files)}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def process_words(text):
    text = text.lower()
    word_pattern = r'\b[a-záéíóúüñç][a-záéíóúüñç0-9\-]*[a-záéíóúüñç0-9]\b|\b[a-záéíóúüñç]\b'
    words = re.findall(word_pattern, text)
    
    cleaned_words = []
    for word in words:
        word = word.strip('-')
        if len(word) >= 2 and not word.isdigit():
            cleaned_words.append(word)
    
    return cleaned_words

def extract_and_sort_words(clean_filename):
    start_time = time.time()
    
    clean_file_path = Path('data/extracted_text') / clean_filenamepp
    
    if not clean_file_path.exists():
        print(f"El archivo limpio {clean_filename} no existe")
        return 0, 0
    
    content = open_file(clean_file_path)
    
    if content.startswith("Failed"):
        print(f"Error al leer {clean_filename}: {content}")
        return 0, 0
    
    words = process_words(content)
    word_counter = Counter(words)
    sorted_words = sorted(word_counter.items())
    
    words_folder = Path('data/sorted_words')
    words_folder.mkdir(exist_ok=True)
    
    base_name = clean_file_path.stem.replace('_clean', '')
    output_filename = f"{base_name}_words_sorted.txt"
    output_path = words_folder / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== PALABRAS ORDENADAS ALFABÉTICAMENTE ===\n")
        f.write(f"Archivo fuente: {clean_filename}\n")
        f.write(f"Total de palabras únicas: {len(sorted_words)}\n")
        f.write(f"Total de palabras: {sum(word_counter.values())}\n")
        f.write("-" * 50 + "\n\n")
        
        for word, count in sorted_words:
            f.write(f"{word:<30} ({count} veces)\n")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return processing_time, len(sorted_words)

def actividad3():
    print("=== EJECUTANDO ACTIVIDAD 3: PROCESAMIENTO DE PALABRAS ===")
    
    clean_folder = Path('data/extracted_text')
    if not clean_folder.exists():
        print("No se encontró la carpeta data/extracted_text.")
        print("Ejecuta primero actividad2() para generar los archivos limpios.")
        return
    
    program_start = time.time()
    
    clean_files = list(clean_folder.glob('*_clean.txt'))
    
    if not clean_files:
        print("No se encontraron archivos limpios para procesar")
        return
    
    log_lines = []
    total_words_processing_time = 0
    total_unique_words = 0
    successful_files = 0
    
    log_lines.append("=== ACTIVIDAD 3: REPORTE DE PROCESAMIENTO DE PALABRAS ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append("")
    log_lines.append("Archivos procesados para extracción de palabras:")
    log_lines.append("-" * 70)
    
    for clean_file in clean_files:
        processing_time, unique_words = extract_and_sort_words(clean_file.name)
        
        if processing_time > 0:
            successful_files += 1
            total_words_processing_time += processing_time
            total_unique_words += unique_words
            
            log_lines.append(f"{clean_file.name:<40} {processing_time:.6f}s  {unique_words:>6} palabras")
            print(f"Palabras procesadas: {clean_file.name} en {processing_time:.6f} segundos")
        else:
            log_lines.append(f"{clean_file.name:<40} ERROR")
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "",
        "=== ESTADÍSTICAS ===",
        f"Archivos encontrados: {len(clean_files)}",
        f"Archivos procesados exitosamente: {successful_files}",
        f"Total palabras únicas encontradas: {total_unique_words}",
        f"Promedio palabras únicas por archivo: {total_unique_words/successful_files if successful_files > 0 else 0:.1f}",
        f"Tiempo total procesando palabras: {total_words_processing_time:.6f} segundos",
        f"Tiempo promedio por archivo: {total_words_processing_time/successful_files if successful_files > 0 else 0:.6f} segundos",
        f"Tiempo total del programa: {total_program_time:.6f} segundos",
        f"Overhead del programa: {total_program_time - total_words_processing_time:.6f} segundos",
        "",
        "Archivos de palabras ordenadas guardados en: ./data/sorted_words/"
    ])
    
    log_path = Path('results/reports/activity_3_word_processing.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 3 completada.")
    print(f"Reporte guardado en: {log_path}")
    print(f"Archivos de palabras ordenadas en: ./data/sorted_words/")
    print(f"Archivos procesados: {successful_files}/{len(clean_files)}")
    print(f"Total palabras únicas: {total_unique_words}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def tokenize_file(input_file, output_file):
    """Tokenize a single HTML file and save the result."""
    start_time = time.time()
    
    content = open_file(input_file)
    
    if content.startswith("Failed"):
        print(f"Error al leer {input_file}: {content}")
        return 0, 0
    
    # Remove HTML tags
    clean_content = re.sub(r'<[^>]+>', '', content)
    clean_content = html.unescape(clean_content)
    clean_content = re.sub(r'\s+', ' ', clean_content)
    clean_content = clean_content.strip()
    
    # Extract words
    words = process_words(clean_content)
    word_counter = Counter(words)
    
    # Save tokenized file (sorted alphabetically, case-insensitive)
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, count in sorted(word_counter.items(), key=lambda x: x[0].lower()):
            f.write(f"{word} {count}\n")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return processing_time, len(word_counter)

def actividad5(input_dir, output_dir):
    """Actividad 5: Command-line tokenizer for specific files."""
    print("=== EJECUTANDO ACTIVIDAD 5: TOKENIZADOR DE ARCHIVOS ESPECÍFICOS ===")
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Error: El directorio de entrada {input_dir} no existe")
        return
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    tokenized_path = output_path / 'tokenized'
    tokenized_path.mkdir(parents=True, exist_ok=True)
    
    files_to_process = ['simple.html', 'medium.html', 'hard.html', '002.html']
    
    program_start = time.time()
    
    log_lines = []
    all_word_frequencies = Counter()
    total_processing_time = 0
    successful_files = 0
    
    log_lines.append("=== ACTIVIDAD 5: REPORTE DE TOKENIZACIÓN DE ARCHIVOS ESPECÍFICOS ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio de entrada: {input_dir}")
    log_lines.append(f"Directorio de salida: {output_dir}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 70)
    
    # Process each specified file
    for filename in files_to_process:
        input_file = input_path / filename
        output_file = tokenized_path / f"{Path(filename).stem}_tokens.txt"
        
        if not input_file.exists():
            log_lines.append(f"{filename:<40} NO ENCONTRADO")
            print(f"Archivo no encontrado: {filename}")
            continue
        
        processing_time, unique_words = tokenize_file(input_file, output_file)
        
        if processing_time > 0:
            successful_files += 1
            total_processing_time += processing_time
            
            # Read the tokenized file to get word frequencies
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(' ', 1)
                    if len(parts) == 2:
                        word, count = parts[0], int(parts[1])
                        all_word_frequencies[word] += count
            
            log_lines.append(f"{filename:<40} {processing_time:.6f}s  {unique_words:>6} palabras")
            print(f"Procesado: {filename} en {processing_time:.6f} segundos - {unique_words} palabras únicas")
        else:
            log_lines.append(f"{filename:<40} ERROR")
    
    consolidation_start = time.time()
    
    alphabetically_sorted = sorted(all_word_frequencies.items(), key=lambda x: x[0].lower())
    consolidated_alpha_path = output_path / 'actividad5alfabetico.txt'
    with open(consolidated_alpha_path, 'w', encoding='utf-8') as f:
        for word, count in alphabetically_sorted:
            f.write(f"{word} {count}\n")
    
    frequency_sorted = sorted(all_word_frequencies.items(), key=lambda x: (-x[1], x[0].lower()))
    consolidated_freq_path = output_path / 'consolidated_tokens_freq.txt'
    with open(consolidated_freq_path, 'w', encoding='utf-8') as f:
        for word, count in frequency_sorted:
            f.write(f"{word} {count}\n")
    
    consolidation_end = time.time()
    consolidation_time = consolidation_end - consolidation_start
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "",
        f"tiempo total en crear el nuevo archivo: {consolidation_time:.2f} segundos",
        f"tiempo total de ejecucion: {total_program_time:.2f} segundos"
    ])
    
    log_path = output_path / 'reports' / 'activity_5_consolidate.txt'
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 5 completada.")
    print(f"Archivos tokenizados guardados en: {output_dir}")
    print(f"Archivo consolidado (alfabético): {consolidated_alpha_path}")
    print(f"Archivo consolidado (por frecuencia): {consolidated_freq_path}")
    print(f"Reporte guardado en: {log_path}")
    print(f"Total palabras únicas: {len(all_word_frequencies)}")
    print(f"Tiempo de consolidación: {consolidation_time:.6f} segundos")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def actividad6(input_dir, output_dir):
    """Actividad 6: Create dictionary file with unique tokens and file counts."""
    print("=== EJECUTANDO ACTIVIDAD 6: CREACIÓN DE DICCIONARIO DE TOKENS ===")
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    tokenized_path = output_path / 'tokenized'
    
    if not tokenized_path.exists():
        print(f"Error: El directorio tokenized {tokenized_path} no existe")
        print("Ejecuta primero actividad5() para generar los archivos tokenizados.")
        return
    
    program_start = time.time()
    
    files_to_process = ['simple.html', 'medium.html', 'hard.html', '002.html']
    
    log_lines = []
    token_data = {}  # {token: {'count': total_count, 'files': set_of_files}}
    file_processing_times = {}
    
    log_lines.append("=== ACTIVIDAD 6: REPORTE DE CREACIÓN DE DICCIONARIO ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio de entrada: {input_dir}")
    log_lines.append(f"Directorio de salida: {output_dir}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 70)
    
    for filename in files_to_process:
        token_file = tokenized_path / f"{Path(filename).stem}_tokens.txt"
        
        if not token_file.exists():
            log_lines.append(f"{filename:<40} NO ENCONTRADO")
            print(f"Archivo tokenizado no encontrado: {filename}")
            continue
        
        file_start = time.time()
        
        with open(token_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    token, count = parts[0], int(parts[1])
                    
                    if token not in token_data:
                        token_data[token] = {'count': 0, 'files': set()}
                    
                    token_data[token]['count'] += count
                    token_data[token]['files'].add(filename)
        
        file_end = time.time()
        processing_time = file_end - file_start
        file_processing_times[filename] = processing_time
        
        log_lines.append(f"{filename:<40} {processing_time:.6f}s")
        print(f"Procesado: {filename} en {processing_time:.6f} segundos")
    
    dictionary_start = time.time()
    
    dictionary_path = output_path / 'a6_dictionary.txt'
    with open(dictionary_path, 'w', encoding='utf-8') as f:
        # No header - format: token;count;num_files
        # Sort tokens alphabetically
        for token in sorted(token_data.keys(), key=lambda x: x.lower()):
            data = token_data[token]
            file_count = len(data['files'])
            # Format: token;count;num_files
            f.write(f"{token};{data['count']};{file_count}\n")
    
    dictionary_end = time.time()
    dictionary_time = dictionary_end - dictionary_start
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "",
        "=== ARCHIVOS PROCESADOS ==="
    ])
    
    for filename in files_to_process:
        if filename in file_processing_times:
            log_lines.append(f"c:\\cs13309\\files\\{filename} {file_processing_times[filename]:.2f}")
    
    log_lines.extend([
        "",
        f"tiempo total en crear el nuevo archivo: {dictionary_time:.2f} segundos",
        f"tiempo total de ejecucion del programa: {total_program_time:.2f} segundos"
    ])
    
    # Save log file
    log_path = output_path / 'reports' / 'activity_6_matricula.txt'
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 6 completada.")
    print(f"Diccionario guardado en: {dictionary_path}")
    print(f"Reporte guardado en: {log_path}")
    print(f"Total tokens únicos: {len(token_data)}")
    print(f"Tiempo de creación del diccionario: {dictionary_time:.6f} segundos")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def actividad4():
    print("=== EJECUTANDO ACTIVIDAD 4: ARCHIVO CONSOLIDADO DE PALABRAS ===")
    
    clean_folder = Path('data/extracted_text')
    if not clean_folder.exists():
        print("No se encontró la carpeta data/extracted_text.")
        print("Ejecuta primero actividad2() para generar los archivos limpios.")
        return
    
    program_start = time.time()
    
    clean_files = list(clean_folder.glob('*_clean.txt'))
    
    if not clean_files:
        print("No se encontraron archivos limpios para procesar")
        return
    
    log_lines = []
    all_words = []  # List to keep all words (with duplicates)
    total_consolidation_time = 0
    successful_files = 0
    
    log_lines.append("=== ACTIVIDAD 4: REPORTE DE CONSOLIDACIÓN DE PALABRAS ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append("")
    log_lines.append("Archivos procesados para consolidación:")
    log_lines.append("-" * 70)
    
    for clean_file in clean_files:
        file_start = time.time()
        
        content = open_file(clean_file)
        
        if content.startswith("Failed"):
            log_lines.append(f"{clean_file.name:<40} ERROR")
            continue
        
        words = process_words(content)
        all_words.extend(words)  # Add all words (keeping duplicates)
        
        file_end = time.time()
        processing_time = file_end - file_start
        total_consolidation_time += processing_time
        successful_files += 1
        
        log_lines.append(f"{clean_file.name:<40} {processing_time:.6f}s  {len(words):>6} palabras")
        print(f"Procesado: {clean_file.name} en {processing_time:.6f} segundos - {len(words)} palabras")
    
    consolidation_start = time.time()
    
    sorted_words = sorted(all_words)  # Sort all words (with duplicates)
    
    consolidated_path = Path('results/consolidated_words.txt')
    consolidated_path.parent.mkdir(parents=True, exist_ok=True)
    with open(consolidated_path, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(f"{word}\n")
    
    consolidation_end = time.time()
    consolidation_time = consolidation_end - consolidation_start
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    unique_count = len(set(all_words))
    total_count = len(all_words)
    
    log_lines.extend([
        "",
        f"Total palabras: {total_count}",
        f"Total palabras únicas: {unique_count}",
        f"tiempo total en crear el nuevo archivo: {consolidation_time:.2f} segundos",
        f"tiempo total de ejecucion: {total_program_time:.2f} segundos"
    ])
    
    log_path = Path('results/reports/activity_4_sorting.txt')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 4 completada.")
    print(f"Archivo consolidado guardado en: {consolidated_path}")
    print(f"Reporte guardado en: {log_path}")
    print(f"Total palabras: {total_count}")
    print(f"Total palabras únicas: {unique_count}")
    print(f"Tiempo de consolidación: {consolidation_time:.6f} segundos")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def test_single_file():
    filename = "467.html"
    print(f"Probando con archivo: {filename}")
    
    tiempo = remove_html_tags(filename)
    print(f"Tiempo para procesar {filename}: {tiempo:.6f} segundos")
    
    clean_file = Path('data/extracted_text') / f"{Path(filename).stem}_clean.txt"
    if clean_file.exists():
        with open(clean_file, 'r', encoding='utf-8') as f:
            content_sample = f.read()[:200]
            print(f"Muestra del contenido limpio: {content_sample}...")
    
    clean_filename = f"{Path(filename).stem}_clean.txt"
    tiempo, palabras = extract_and_sort_words(clean_filename)
    print(f"Tiempo para extraer palabras de {clean_filename}: {tiempo:.6f} segundos")
    print(f"Palabras únicas encontradas: {palabras}")
    
    words_file = Path('data/sorted_words') / f"{Path(filename).stem}_words_sorted.txt"
    if words_file.exists():
        with open(words_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print("\nAlgunas palabras encontradas (con acentos):")
            word_count = 0
            for line in lines[5:]:
                if word_count >= 10:
                    break
                if line.strip() and ('ó' in line or 'á' in line or 'é' in line or 'í' in line or 'ú' in line or 'ñ' in line):
                    print(f"  {line.strip()}")
                    word_count += 1


                    import os



def actividad7(output_dir="results"):
    """
    Actividad 7: Crear diccionario y archivo posting desde archivos tokenizados.
    """
    import os
    import time
    from collections import defaultdict
    from pathlib import Path

    print("=== EJECUTANDO ACTIVIDAD 7: CREACIÓN DEL DICCIONARIO Y ARCHIVO POSTING ===")
    
    base_dir = Path(output_dir)
    token_dir = base_dir / "tokenized"
    dict_posting_dir = base_dir / "dictionary_posting"
    dict_posting_dir.mkdir(parents=True, exist_ok=True)

    dict_file = dict_posting_dir / "a7_Diccionario.txt"
    post_file = dict_posting_dir / "a7_Posting.txt"
    report_file = base_dir / "reports" / "activity_7_dictionary_posting.txt"

    program_start = time.time()
    log_lines = []
    
    log_lines.append("=== ACTIVIDAD 7: REPORTE DE CREACIÓN DE DICCIONARIO Y POSTING ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio de tokens: {token_dir}")
    log_lines.append("")

    # Verify token directory exists
    if not token_dir.exists():
        error_msg = f"No se encontró la carpeta de tokens: {token_dir}"
        log_lines.append(error_msg)
        print(error_msg)
        print("Ejecuta primero actividad5() para generar los archivos tokenizados.")
        
        with open(report_file, "w", encoding="utf-8") as log:
            log.write('\n'.join(log_lines))
        return

    # Step 1: Read tokenized files and collect word data
    word_docs = defaultdict(lambda: defaultdict(int))  # {token: {filename: frequency}}
    token_files = list(token_dir.glob("*_tokens.txt"))
    
    if not token_files:
        error_msg = "No se encontraron archivos tokenizados (_tokens.txt)"
        log_lines.append(error_msg)
        print(error_msg)
        
        with open(report_file, "w", encoding="utf-8") as log:
            log.write('\n'.join(log_lines))
        return

    log_lines.append("Archivos tokenizados procesados:")
    log_lines.append("-" * 70)
    
    for token_file in token_files:
        file_start = time.time()
        
        # Extract original filename (remove _tokens.txt suffix and add .html)
        original_filename = token_file.stem.replace('_tokens', '') + '.html'
        
        try:
            with open(token_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse "token count" format
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        token, count_str = parts
                        try:
                            count = int(count_str)
                            word_docs[token][original_filename] = count
                        except ValueError:
                            continue
            
            file_end = time.time()
            processing_time = file_end - file_start
            
            log_lines.append(f"{token_file.name:<40} {processing_time:.6f}s")
            print(f"Procesado: {token_file.name} en {processing_time:.6f} segundos")
            
        except Exception as e:
            log_lines.append(f"{token_file.name:<40} ERROR: {e}")
            print(f"Error procesando {token_file.name}: {e}")

    log_lines.extend([
        "",
        f"Total archivos tokenizados procesados: {len(token_files)}",
        f"Total tokens únicos encontrados: {len(word_docs)}",
        ""
    ])

    # Step 2: Build posting and dictionary
    posting_start = time.time()
    
    posting_lines = []
    dict_lines = []
    position = 0  # Initial posting position

    # Sort tokens alphabetically (case-insensitive)
    sorted_tokens = sorted(word_docs.keys(), key=lambda x: x.lower())
    
    for token in sorted_tokens:
        docs = word_docs[token]
        num_docs = len(docs)
        
        # Calculate total repetitions (sum of frequencies across all documents)
        total_repetitions = sum(docs.values())

        # Add to dictionary: token;repetitions;num_docs
        dict_lines.append(f"{token};{total_repetitions};{num_docs}\n")

        # Add to posting: Archivo, Frecuencia (sorted by filename)
        for doc in sorted(docs.keys()):
            freq = docs[doc]
            posting_lines.append(f"{doc};{freq}\n")

        # Update posting position for next token
        position += num_docs

    # Step 3: Write dictionary file
    with open(dict_file, "w", encoding="utf-8") as df:
        # No header needed, just write the data lines
        df.writelines(dict_lines)

    # Step 4: Write posting file
    with open(post_file, "w", encoding="utf-8") as pf:
        # No header - format: archivo.html;frecuencia
        pf.writelines(posting_lines)

    posting_end = time.time()
    posting_time = posting_end - posting_start
    
    program_end = time.time()
    total_program_time = program_end - program_start

    log_lines.extend([
        "=== ARCHIVOS GENERADOS ===",
        f"Diccionario: {dict_file}",
        f"Posting: {post_file}",
        "",
        "=== ESTADÍSTICAS ===",
        f"Total tokens únicos en diccionario: {len(sorted_tokens)}",
        f"Total registros en posting: {len(posting_lines)}",
        f"Tiempo creando diccionario y posting: {posting_time:.6f} segundos",
        f"Tiempo total de ejecución: {total_program_time:.6f} segundos",
        "",
        "Proceso completado correctamente."
    ])

    # Step 5: Write report file
    with open(report_file, "w", encoding="utf-8") as log:
        log.write('\n'.join(log_lines))

    print(f"\n Actividad 7 completada.")
    print(f"Diccionario generado: {dict_file}")
    print(f"Archivo Posting generado: {post_file}")
    print(f"Reporte guardado en: {report_file}")
    print(f"Total tokens únicos: {len(sorted_tokens)}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")


def hash_function(key, size):
    """Implementa una versión simple de la función hash DJB2."""
    hash_value = 5381
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value % size

def search_word(word, output_dir="results", use_stoplist=False):
    """
    Actividad 12: Buscar una palabra en el diccionario y posting.
    
    Args:
        word: Palabra a buscar
        output_dir: Directorio donde están los archivos de resultados
        use_stoplist: Si True, usa los archivos de actividad 9 (con stoplist),
                     si False, usa los archivos de actividad 8 (sin stoplist)
    
    Returns:
        Lista de documentos que contienen la palabra, o lista vacía si no se encuentra
    """
    from pathlib import Path
    import re
    
    # Convertir palabra a minúsculas para coincidir con el diccionario
    word = word.lower().strip()
    
    if not word:
        return []
    
    base_dir = Path(output_dir)
    HASH_TABLE_SIZE = 20000
    EMPTY_SLOT_INDICATOR = "vacio"
    
    # Seleccionar archivos según si se usa stoplist o no
    if use_stoplist:
        dict_file = base_dir / "a9_diccionario_refinado.txt"
        posting_file = base_dir / "a9_posting.txt"
    else:
        dict_file = base_dir / "a8_diccionario_hash.txt"
        posting_file = base_dir / "a8_posting.txt"
    
    # Verificar que los archivos existan
    if not dict_file.exists():
        print(f"Error: No se encontró el archivo de diccionario: {dict_file}")
        return []
    
    if not posting_file.exists():
        print(f"Error: No se encontró el archivo de posting: {posting_file}")
        return []
    
    # Calcular hash de la palabra
    hash_index = hash_function(word, HASH_TABLE_SIZE)
    
    # Paso 1: Construir índice completo del diccionario
    # Mapeo: token -> (num_docs, posting_offset)
    token_info = {}  # {token: num_docs}
    all_tokens = []  # Lista de todos los tokens en orden alfabético
    
    with open(dict_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parsear línea del diccionario
            # Formato: Posición Hash: X, Token: Y, Frecuencia: Z, Archivos: W, Posición Posting: P
            match = re.search(r'Posición Hash: \d+, Token: ([^,]+), Frecuencia: \d+, Archivos: (\d+), Posición Posting: -?\d+', line)
            if match:
                token, archivos = match.groups()
                token = token.strip()
                archivos = int(archivos)
                
                if token != EMPTY_SLOT_INDICATOR and archivos > 0:
                    if token not in token_info:
                        token_info[token] = archivos
                        all_tokens.append(token)
    
    # Ordenar tokens alfabéticamente
    all_tokens.sort()
    
    # Verificar si el token existe
    if word not in token_info:
        return []
    
    # Paso 2: Calcular el offset en el posting
    # El posting está ordenado alfabéticamente por token
    posting_offset = 0
    for token in all_tokens:
        if token == word:
            break
        posting_offset += token_info[token]
    
    # Paso 3: Leer los documentos del posting
    num_docs = token_info[word]
    documents = []
    
    with open(posting_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Leer las líneas correspondientes a nuestro token
        for i in range(posting_offset, min(posting_offset + num_docs, len(lines))):
            line = lines[i].strip()
            if line:
                parts = line.split(';')
                if len(parts) >= 1:
                    doc_name = parts[0].strip()
                    if doc_name and doc_name not in documents:  # Evitar duplicados
                        documents.append(doc_name)
    
    return sorted(documents) if documents else []

def actividad8(output_dir="results"):
    """
    Actividad 8:
    Genera archivos 'diccionario_hash.txt', 'posting.txt' y 'a8_<matricula>.txt' (log de tiempos).
    Usa una hash table para almacenar los tokens.
    """
    import os
    import time
    from collections import defaultdict
    from pathlib import Path

    matricula = "2878113"
    HASH_TABLE_SIZE = 20000
    EMPTY_SLOT_INDICATOR = "vacio"
    EMPTY_POSTING_POSITION = -1
    
    print("=== EJECUTANDO ACTIVIDAD 8: DICCIONARIO CON HASH TABLE ===")

    base_dir = Path(output_dir)
    folder_path = Path(FOLDER)
    
    if not folder_path.exists():
        print(f"Error: El directorio {FOLDER} no existe")
        return

    # --- Step 1: Preparar estructuras de datos ---
    token_data = defaultdict(lambda: defaultdict(int))  # {token: {archivo: frecuencia}}
    hash_table = [[] for _ in range(HASH_TABLE_SIZE)]  # Lista de listas para chaining
    colisiones = 0
    posting_data = []                                   # [(archivo, frecuencia)]

    # --- Step 2: Leer archivos HTML y contar tiempos individuales ---
    start_total = time.time()
    file_durations = []

    html_files = sorted(folder_path.glob('*.html'))
    
    if not html_files:
        print("No se encontraron archivos HTML")
        return

    for html_file in html_files:
        start_file = time.time()
        filename = html_file.name
        
        try:
            # Read HTML file
            content = open_file(html_file)
            if content.startswith("Failed"):
                print(f"Error: {content}")
                continue
            
            # Clean HTML tags
            clean_content = re.sub(r'<[^>]+>', '', content)
            
            # Extract and process words
            words = process_words(clean_content)
            
            # Count token frequencies per file
            for word in words:
                token_data[word][filename] += 1
                
        except Exception as e:
            print(f"Error procesando {filename}: {e}")
            continue

        end_file = time.time()
        duration = end_file - start_file
        file_durations.append((filename, duration))
        print(f"Procesado: {filename} en {duration:.4f} segundos")

    posting_start = time.time()
    
    posting_file = base_dir / "a8_posting.txt"

    with open(posting_file, "w", encoding="utf-8") as post:
        # Sort tokens alphabetically for consistent ordering
        sorted_tokens = sorted(token_data.keys())
        
        for token in sorted_tokens:
            docs = token_data[token]
            num_docs = len(docs)
            total_freq = sum(docs.values())
            
            for archivo in sorted(docs.keys()): 
                frecuencia = docs[archivo]
                post.write(f"{archivo};{frecuencia}\n")
                posting_data.append((archivo, frecuencia))

            # Calcular hash del token usando DJB2
            hash_index = hash_function(token, HASH_TABLE_SIZE)
            
            # Manejo de colisiones con chaining (listas de listas)
            if hash_table[hash_index]:
                colisiones += 1
            
            # Almacenar en la lista de ese índice
            hash_table[hash_index].append((token, total_freq, num_docs, hash_index))

    posting_end = time.time()
    posting_time = posting_end - posting_start

    # --- Step 4: Crear archivo diccionario hash (ASCII legible) ---
    dict_start = time.time()
    
    dict_file = base_dir / "a8_diccionario_hash.txt"
    with open(dict_file, "w", encoding="utf-8") as dic:
        occupied_slots = 0
        for i, slot in enumerate(hash_table):
            if not slot:
                dic.write(f"Posición Hash: {i}, Token: {EMPTY_SLOT_INDICATOR}, Frecuencia: 0, Archivos: 0, Posición Posting: {EMPTY_POSTING_POSITION}\n")
            else:
                occupied_slots += 1
                for token, freq, num_files, pos in slot:
                    dic.write(f"Posición Hash: {i}, Token: {token}, Frecuencia: {freq}, Archivos: {num_files}, Posición Posting: {pos}\n")
    
    dict_end = time.time()
    dict_time = dict_end - dict_start

    # --- Step 5: Crear archivo log (medición de tiempos) ---
    end_total = time.time()
    total_time = end_total - start_total

    log_file = base_dir / f"a8_{matricula}.txt"
    with open(log_file, "w", encoding="utf-8") as log:
        for filename, duration in file_durations:
            log.write(f"{filename}           {duration:.4f} \n")

    print(f"\n Archivos generados exitosamente:")
    print(f"- {dict_file}")
    print(f"- {posting_file}")
    print(f"- {log_file}")
    print(f"\nEstadísticas:")
    print(f"- Total tokens únicos: {len(token_data)}")
    print(f"- Total colisiones: {colisiones}")
    occupied = sum(1 for slot in hash_table if slot)
    print(f"- Slots ocupados: {occupied}/{HASH_TABLE_SIZE} ({occupied/HASH_TABLE_SIZE:.2%})")
    print(f"- Tiempo total: {total_time:.4f} segundos")

                    

def actividad9(output_dir="results", stoplist_path="stoplist.txt"):
    """
    Actividad 9:
    Refinar el diccionario con una stop list y eliminar tokens de una sola letra o dígito. 
    Incluye medición de tiempos y reporte de factores del sistema.
    """
    import os
    import time
    from collections import defaultdict
    from pathlib import Path

    matricula = "A00837763"
    HASH_TABLE_SIZE = 20000
    EMPTY_SLOT_INDICATOR = "vacio"
    EMPTY_POSTING_POSITION = -1

    print("=== EJECUTANDO ACTIVIDAD 9: REFINAMIENTO DEL DICCIONARIO ===")

    # --- Step 1: Factores externos e internos del sistema ---
    factores_externos = [
        "Disponibilidad del hardware y tiempo de ejecución (puede afectar el rendimiento).",
        "Tamaño y calidad de los archivos HTML procesados (impacta la cantidad de tokens).",
        "Uso de técnicas hash y colisiones (afectan la eficiencia de acceso y almacenamiento)."
    ]

    calidad_interna = [
        "Eficiencia del algoritmo de tokenización.",
        "Modularidad del código y reutilización de funciones.",
        "Precisión del filtrado de palabras y stop list."
    ]

    historias_usuario = [
        "Como desarrollador, quiero aplicar una lista de stop words para que el diccionario sea más relevante.",
        "Como usuario, quiero eliminar tokens de una sola letra o solo dígitos para mejorar la calidad del diccionario.",
        "Como analista, quiero medir el tiempo de procesamiento para evaluar el rendimiento del sistema."
    ]

    # --- Step 2: Setup paths ---
    base_dir = Path(output_dir)
    token_dir = base_dir / "tokenized"
    
    if not token_dir.exists():
        print(f"Error: El directorio tokenized {token_dir} no existe")
        print("Ejecuta primero actividad5() para generar los archivos tokenizados.")
        return

    # --- Step 3: Cargar stop list ---
    stop_words = set()
    stoplist_file = Path(stoplist_path)
    
    if stoplist_file.exists():
        with open(stoplist_file, 'r', encoding='utf-8') as stopf:
            for line in stopf:
                word = line.strip().lower()
                if word:
                    stop_words.add(word)
        print(f"Stop list cargada: {len(stop_words)} palabras")
    else:
        print(f"Advertencia: No se encontró el archivo {stoplist_path}")
        print("Continuando sin stop list...")

    # --- Step 4: Procesar archivos tokenizados ---
    token_data = defaultdict(lambda: defaultdict(int))  # {token: {archivo: frecuencia}}
    start_total = time.time()
    log_lines = []
    
    log_lines.append("=== ACTIVIDAD 9: REPORTE DE REFINAMIENTO ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Matrícula: {matricula}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 70)

    token_files = list(token_dir.glob("*_tokens.txt"))
    
    if not token_files:
        print("No se encontraron archivos tokenizados")
        return

    tokens_before_filter = 0
    
    for token_file in token_files:
        start_file = time.time()
        
        # Extract original filename
        original_filename = token_file.stem.replace('_tokens', '') + '.html'
        
        try:
            with open(token_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse "token count" format
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        token, count_str = parts
                        try:
                            count = int(count_str)
                            tokens_before_filter += 1
                            
                            # Apply stop list filter
                            if token.lower() not in stop_words:
                                token_data[token][original_filename] = count
                                
                        except ValueError:
                            continue
        except Exception as e:
            print(f"Error leyendo {token_file.name}: {e}")
            continue

        end_file = time.time()
        log_lines.append(f"c:\\cs13309\\files\\{original_filename} {end_file - start_file:.2f}")
        print(f"Procesado: {original_filename} en {end_file - start_file:.4f} segundos")

    # --- Step 5: Aplicar filtros de refinamiento ---
    print("\nAplicando filtros de refinamiento...")
    
    refined_tokens = {}
    tokens_removed_single_char = 0
    tokens_removed_stoplist = tokens_before_filter - len(token_data)
    
    for token, docs in token_data.items():
        # Filtro 1: Eliminar tokens de una sola letra o dígito
        if len(token) <= 1:
            tokens_removed_single_char += 1
            continue
        
        # Filtro 2: Eliminar tokens que son solo dígitos
        if token.isdigit():
            tokens_removed_single_char += 1
            continue
        
        refined_tokens[token] = docs

    print(f"Tokens antes del filtrado: {len(token_data)}")
    print(f"Tokens después del filtrado: {len(refined_tokens)}")
    print(f"Removidos por stop list: {tokens_removed_stoplist}")
    print(f"Removidos por longitud/dígitos: {tokens_removed_single_char}")

    # --- Step 6: Crear archivo posting refinado ---
    posting_start = time.time()
    
    hash_table = [[] for _ in range(HASH_TABLE_SIZE)]  # Lista de listas para chaining
    colisiones = 0

    posting_file = base_dir / "a9_posting.txt"
    
    with open(posting_file, "w", encoding="utf-8") as post:
        # Sort tokens alphabetically
        sorted_tokens = sorted(refined_tokens.keys())
        
        for token in sorted_tokens:
            docs = refined_tokens[token]
            num_docs = len(docs)
            total_freq = sum(docs.values())
            
            # Guardar en posting (ordenado por archivo)
            for archivo in sorted(docs.keys()):
                freq = docs[archivo]
                post.write(f"{archivo};{freq}\n")

            # Calcular hash del token usando DJB2
            hash_index = hash_function(token, HASH_TABLE_SIZE)
            
            # Manejo de colisiones con chaining (listas de listas)
            if hash_table[hash_index]:
                colisiones += 1
            
            # Almacenar en la lista de ese índice
            hash_table[hash_index].append((token, total_freq, num_docs, hash_index))

    posting_end = time.time()
    posting_time = posting_end - posting_start

    # --- Step 7: Generar diccionario refinado ---
    dict_start = time.time()
    
    dict_file = base_dir / "a9_diccionario_refinado.txt"
    
    with open(dict_file, "w", encoding="utf-8") as dic:
        occupied_slots = 0
        for i, slot in enumerate(hash_table):
            if not slot:
                dic.write(f"Posición Hash: {i}, Token: {EMPTY_SLOT_INDICATOR}, Frecuencia: 0, Archivos: 0, Posición Posting: {EMPTY_POSTING_POSITION}\n")
            else:
                occupied_slots += 1
                for token, freq, num_files, pos in slot:
                    dic.write(f"Posición Hash: {i}, Token: {token}, Frecuencia: {freq}, Archivos: {num_files}, Posición Posting: {pos}\n")
        
        dic.write("\n=== ESTADÍSTICAS DE FILTRADO ===\n")
        dic.write(f"Tokens originales: {tokens_before_filter}\n")
        dic.write(f"Removidos por stop list: {tokens_removed_stoplist}\n")
        dic.write(f"Removidos por longitud/dígitos: {tokens_removed_single_char}\n")
        dic.write(f"Tokens finales: {len(refined_tokens)}\n")
        dic.write(f"Número total de colisiones: {colisiones}\n")
        dic.write(f"Slots ocupados: {occupied_slots}/{HASH_TABLE_SIZE}\n")
        dic.write(f"Factor de carga: {occupied_slots/HASH_TABLE_SIZE:.2%}\n")
    
    dict_end = time.time()
    dict_time = dict_end - dict_start

    # --- Step 8: Crear log de tiempo y documentación técnica ---
    end_total = time.time()
    total_time = end_total - start_total
    
    log_lines.extend([
        "",
        f"tiempo total en crear el nuevo archivo: {posting_time + dict_time:.2f} segundos",
        f"tiempo total de ejecucion: {total_time:.2f} segundos",
        "",
        "=== ESTADÍSTICAS DE REFINAMIENTO ===",
        f"Tokens originales (con stop list): {len(token_data)}",
        f"Tokens refinados: {len(refined_tokens)}",
        f"Tokens removidos por stop list: {tokens_removed_stoplist}",
        f"Tokens removidos por longitud/dígitos: {tokens_removed_single_char}",
        f"Número total de colisiones: {colisiones}",
        f"Slots ocupados: {sum(1 for slot in hash_table if slot)}/{HASH_TABLE_SIZE}"
    ])

    log_file = base_dir / "reports" / f"activity_9_{matricula}.txt"
    
    with open(log_file, "w", encoding="utf-8") as log:
        log.write('\n'.join(log_lines))
        log.write("\n\n== Factores externos del sistema ==\n")
        for f in factores_externos:
            log.write(f"- {f}\n")

        log.write("\n== Factores de calidad interna ==\n")
        for q in calidad_interna:
            log.write(f"- {q}\n")

        log.write("\n== Historias de usuario ==\n")
        for h in historias_usuario:
            log.write(f"- {h}\n")

    print(f"\n Archivos generados:")
    print(f"- {posting_file}")
    print(f"- {dict_file}")
    print(f"- {log_file}")
    print(f"\nEstadísticas finales:")
    print(f"- Tokens refinados: {len(refined_tokens)}")
    print(f"- Reducción: {(1 - len(refined_tokens)/len(token_data))*100:.1f}%")
    print(f"- Colisiones: {colisiones}")
    print(f"- Tiempo total: {total_time:.4f} segundos")


def actividad10(output_dir="results"):
    """
    Actividad 10: Weight tokens using tf.idf formula.
    
    Formula: tf.idf = (# de repeticiones * 100) / # de total de tokens en el documento
    
    Modifies the posting file to replace frequency with weight.
    Uses fixed column sizes (20 bytes for dictionary, 10 bytes for posting).
    """
    import time
    from collections import defaultdict
    from pathlib import Path
    
    print("=== EJECUTANDO ACTIVIDAD 10: PESO DE TOKENS (TF.IDF) ===")
    
    base_dir = Path(output_dir)
    token_dir = base_dir / "tokenized"
    dict_posting_dir = base_dir / "dictionary_posting"
    
    # Output files
    dict_file = dict_posting_dir / "a7_Diccionario.txt"
    post_file = dict_posting_dir / "a7_Posting.txt"
    weighted_post_file = dict_posting_dir / "a10_Posting_Weighted.txt"
    weighted_dict_file = dict_posting_dir / "a10_Diccionario_Weighted.txt"
    report_file = base_dir / "reports" / "activity_10_weighting.txt"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    program_start = time.time()
    log_lines = []
    
    log_lines.append("=== ACTIVIDAD 10: REPORTE DE PESO DE TOKENS (TF.IDF) ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio base: {base_dir}")
    log_lines.append("")
    
    # Verify required files exist
    if not dict_file.exists() or not post_file.exists():
        error_msg = "No se encontraron los archivos a7_Diccionario.txt o a7_Posting.txt"
        error_msg += "\nEjecuta primero actividad7() para generar estos archivos."
        log_lines.append(error_msg)
        print(error_msg)
        
        with open(report_file, "w", encoding="utf-8") as log:
            log.write('\n'.join(log_lines))
        return
    
    if not token_dir.exists():
        error_msg = f"No se encontró la carpeta de tokens: {token_dir}"
        error_msg += "\nEjecuta primero actividad5() para generar los archivos tokenizados."
        log_lines.append(error_msg)
        print(error_msg)
        
        with open(report_file, "w", encoding="utf-8") as log:
            log.write('\n'.join(log_lines))
        return
    
    # Step 1: Calculate total tokens per document
    log_lines.append("=== PASO 1: CALCULANDO TOTAL DE TOKENS POR DOCUMENTO ===")
    log_lines.append("-" * 70)
    
    doc_total_tokens = {}  # {filename: total_tokens}
    token_files = list(token_dir.glob("*_tokens.txt"))
    
    for token_file in token_files:
        file_start = time.time()
        original_filename = token_file.stem.replace('_tokens', '') + '.html'
        total_tokens = 0
        
        try:
            with open(token_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        try:
                            count = int(parts[1])
                            total_tokens += count
                        except ValueError:
                            continue
            
            doc_total_tokens[original_filename] = total_tokens
            
            file_end = time.time()
            processing_time = file_end - file_start
            
            log_lines.append(f"{original_filename:<40} {total_tokens:>8} tokens  {processing_time:.6f}s")
            print(f"Procesado: {original_filename} - {total_tokens} tokens en {processing_time:.6f}s")
            
        except Exception as e:
            log_lines.append(f"{original_filename:<40} ERROR: {e}")
            print(f"Error procesando {original_filename}: {e}")
    
    log_lines.append("")
    log_lines.append(f"Total documentos procesados: {len(doc_total_tokens)}")
    if doc_total_tokens:
        log_lines.append("Archivos en doc_total_tokens:")
        for filename, total in list(doc_total_tokens.items())[:5]:  # Show first 5
            log_lines.append(f"  {filename}: {total} tokens")
        if len(doc_total_tokens) > 5:
            log_lines.append(f"  ... y {len(doc_total_tokens) - 5} más")
    log_lines.append("")
    
    # Step 2: Read dictionary and posting, then calculate weights
    log_lines.append("=== PASO 2: CALCULANDO PESOS TF.IDF ===")
    log_lines.append("-" * 70)
    
    weight_start = time.time()
    
    # Read dictionary to get token order and positions
    token_list = []  # List of (token, repetitions, num_docs)
    with open(dict_file, 'r', encoding='utf-8') as f:
        # No header in dictionary file from actividad7
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Dictionary format from actividad7: token;repetitions;num_docs
            parts = line.split(';')
            if len(parts) >= 3:
                token = parts[0]
                repetitions = int(parts[1])
                num_docs = int(parts[2])
                token_list.append((token, repetitions, num_docs))
    
    # Read posting file and calculate weights
    posting_data = []  # List of (token, filename, frequency, weight)
    posting_index = 0
    
    with open(post_file, 'r', encoding='utf-8') as f:
        # No header in posting file - format: archivo.html;frecuencia
        
        for token, repetitions, num_docs in token_list:
            # Read num_docs entries for this token
            for _ in range(num_docs):
                line = f.readline().strip()
                if not line:
                    break
                
                parts = line.split(';')
                if len(parts) >= 2:
                    filename = parts[0]
                    frequency = int(parts[1])
                    
                    # Calculate weight: tf.idf = (frequency * 100) / total_tokens_in_doc
                    total_tokens_in_doc = doc_total_tokens.get(filename)
                    if total_tokens_in_doc is None:
                        # If filename not found, try to find it (case-insensitive or without extension)
                        found = False
                        for key in doc_total_tokens.keys():
                            if key.lower() == filename.lower() or key == filename:
                                total_tokens_in_doc = doc_total_tokens[key]
                                found = True
                                break
                        if not found:
                            # Log warning and use a default (but this shouldn't happen)
                            log_lines.append(f"WARNING: No se encontró total_tokens para {filename}, usando 1")
                            total_tokens_in_doc = 1
                    
                    if total_tokens_in_doc == 0:
                        total_tokens_in_doc = 1  # Avoid division by zero
                    
                    # Calculate weight: (frequency * 100) / total_tokens_in_doc
                    # This gives a percentage-like value (0-100 range typically)
                    weight = (frequency * 100) / total_tokens_in_doc
                    
                    posting_data.append((token, filename, frequency, weight))
    
    weight_end = time.time()
    weight_time = weight_end - weight_start
    
    log_lines.append(f"Total registros procesados: {len(posting_data)}")
    log_lines.append(f"Tiempo calculando pesos: {weight_time:.6f} segundos")
    log_lines.append("")
    
    # Step 3: Write weighted posting file with fixed column sizes
    log_lines.append("=== PASO 3: ESCRIBIENDO ARCHIVOS CON COLUMNAS DE TAMAÑO FIJO ===")
    log_lines.append("-" * 70)
    
    write_start = time.time()
    
    # Fixed column sizes (divisible by 80 bytes)
    # Dictionary: 20 bytes per line (20 * 4 = 80 bytes per 4 lines)
    # Posting: 10 bytes per line (10 * 8 = 80 bytes per 8 lines)
    DICT_COL_SIZE = 20
    POST_COL_SIZE = 10
    
    # Write weighted dictionary (same structure, fixed width)
    weighted_dict_lines = []
    weighted_dict_lines.append(f"{'Token':<15}{'N°Docs':<5}\n")  # Header
    
    for token, repetitions, num_docs in token_list:
        # Format: Token (15 chars) + N°Docs (5 chars) = 20 bytes
        token_short = token[:15] if len(token) > 15 else token
        line = f"{token_short:<15}{num_docs:<5}\n"
        weighted_dict_lines.append(line)
    
    with open(weighted_dict_file, 'w', encoding='utf-8') as f:
        f.writelines(weighted_dict_lines)
    
    # Write weighted posting file
    weighted_posting_lines = []
    weighted_posting_lines.append(f"{'Archivo':<8}{' P':>2}\n")  # Header (10 bytes): 8 chars filename, 2 chars weight (right-aligned, " P" for Peso)
    
    # Group posting data by token (maintain order)
    posting_by_token = defaultdict(list)
    for token, filename, freq, weight in posting_data:
        posting_by_token[token].append((filename, freq, weight))
    
    # Write in token order
    for token, repetitions, num_docs in token_list:
        if token in posting_by_token:
            for filename, freq, weight in sorted(posting_by_token[token]):
                # Format: Archivo (8 chars) + Peso (2 chars) = 10 bytes
                # Formula: tf.idf = (frequency * 100) / total_tokens_in_doc
                # Scale by 100 to preserve precision: converts 0.03→3, 0.33→33, 8.0→99 (capped)
                # This preserves the relative differences between weights
                weight_scaled = weight * 100
                weight_int = min(99, max(0, int(round(weight_scaled))))  # Cap at 99 for 2-digit display
                # Ensure filename is exactly 8 characters: truncate if longer, pad with spaces if shorter
                filename_short = (filename[:8] if len(filename) >= 8 else filename).ljust(8)
                # Format: exactly 8 chars for filename, exactly 2 chars for weight (right-aligned)
                line = f"{filename_short}{weight_int:>2}\n"  # No space between, exact widths
                weighted_posting_lines.append(line)
    
    with open(weighted_post_file, 'w', encoding='utf-8') as f:
        f.writelines(weighted_posting_lines)
    
    write_end = time.time()
    write_time = write_end - write_start
    
    log_lines.append(f"Archivo diccionario: {weighted_dict_file}")
    log_lines.append(f"Archivo posting: {weighted_post_file}")
    log_lines.append(f"Tamaño columna diccionario: {DICT_COL_SIZE} bytes")
    log_lines.append(f"Tamaño columna posting: {POST_COL_SIZE} bytes")
    log_lines.append(f"Tiempo escribiendo archivos: {write_time:.6f} segundos")
    log_lines.append("")
    
    # Step 4: Statistics
    program_end = time.time()
    total_program_time = program_end - program_start
    
    # Calculate statistics
    total_tokens_weighted = len(posting_data)
    unique_tokens = len(token_list)
    avg_weight = sum(weight for _, _, _, weight in posting_data) / len(posting_data) if posting_data else 0
    max_weight = max(weight for _, _, _, weight in posting_data) if posting_data else 0
    min_weight = min(weight for _, _, _, weight in posting_data) if posting_data else 0
    
    # Count weights that round to 0 vs non-zero
    weights_rounded_to_zero = sum(1 for _, _, _, w in posting_data if int(round(w * 100)) == 0)
    weights_non_zero = total_tokens_weighted - weights_rounded_to_zero
    
    # Count files in posting
    files_in_posting = {}
    for _, filename, _, _ in posting_data:
        files_in_posting[filename] = files_in_posting.get(filename, 0) + 1
    
    # Sample some weights for debugging
    sample_weights = [w for _, _, _, w in posting_data[:10]] if posting_data else []
    
    log_lines.extend([
        "=== ESTADÍSTICAS ===",
        f"Total tokens únicos: {unique_tokens}",
        f"Total registros en posting: {total_tokens_weighted}",
        f"Peso promedio: {avg_weight:.6f}",
        f"Peso máximo: {max_weight:.6f}",
        f"Peso mínimo: {min_weight:.6f}",
        f"Pesos que se redondean a 0: {weights_rounded_to_zero}",
        f"Pesos no-cero (redondeados): {weights_non_zero}",
        f"Total documentos procesados para total_tokens: {len(doc_total_tokens)}",
        f"Archivos en posting: {len(files_in_posting)}",
        f"Distribución de archivos: {dict(sorted(files_in_posting.items(), key=lambda x: x[1], reverse=True))}",
        f"Muestra de primeros 10 pesos calculados: {[f'{w:.4f}' for w in sample_weights]}",
        "",
        "=== TIEMPOS ===",
        f"Tiempo calculando pesos: {weight_time:.6f} segundos",
        f"Tiempo escribiendo archivos: {write_time:.6f} segundos",
        f"Tiempo total de ejecución: {total_program_time:.6f} segundos",
        "",
        "Proceso completado correctamente."
    ])
    
    # Write report file
    with open(report_file, 'w', encoding='utf-8') as log:
        log.write('\n'.join(log_lines))
    
    print(f"\nActividad 10 completada.")
    print(f"Archivos generados:")
    print(f"  - Diccionario con pesos: {weighted_dict_file}")
    print(f"  - Posting con pesos: {weighted_post_file}")
    print(f"  - Reporte: {report_file}")
    print(f"Total tokens procesados: {total_tokens_weighted}")
    print(f"Peso promedio: {avg_weight:.4f}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")


def actividad11(output_dir="results"):
    """
    Actividad 11: Document Index
    
    Creates a document index file that maps document names to unique IDs.
    Modifies the posting file to use document IDs instead of filenames.
    """
    import time
    from collections import defaultdict, OrderedDict
    from pathlib import Path
    
    print("=== EJECUTANDO ACTIVIDAD 11: ÍNDICE DE DOCUMENTOS ===")
    
    base_dir = Path(output_dir)
    dict_posting_dir = base_dir / "dictionary_posting"
    
    # Input files (try weighted first, then regular)
    weighted_post_file = dict_posting_dir / "a10_Posting_Weighted.txt"
    post_file = dict_posting_dir / "a7_Posting.txt"
    dict_file = dict_posting_dir / "a7_Diccionario.txt"
    
    # Output files
    documents_file = dict_posting_dir / "a11_Documentos.txt"
    indexed_post_file = dict_posting_dir / "a11_Posting_Indexed.txt"
    indexed_dict_file = dict_posting_dir / "a11_Diccionario_Indexed.txt"
    report_file = base_dir / "reports" / "activity_11_document_index.txt"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    program_start = time.time()
    log_lines = []
    
    log_lines.append("=== ACTIVIDAD 11: REPORTE DE ÍNDICE DE DOCUMENTOS ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio base: {base_dir}")
    log_lines.append("")
    
    # Determine which posting file to use
    posting_file_to_use = None
    has_weights = False
    
    if weighted_post_file.exists():
        posting_file_to_use = weighted_post_file
        has_weights = True
        log_lines.append(f"Usando archivo de posting con pesos: {weighted_post_file}")
        print(f"Usando archivo de posting con pesos: {weighted_post_file}")
    elif post_file.exists():
        posting_file_to_use = post_file
        has_weights = False
        log_lines.append(f"Usando archivo de posting regular: {post_file}")
        print(f"Usando archivo de posting regular: {post_file}")
    else:
        error_msg = "No se encontró ningún archivo de posting."
        error_msg += "\nEjecuta primero actividad7() (genera a7_Posting.txt) o actividad10() (genera a10_Posting_Weighted.txt)."
        log_lines.append(error_msg)
        print(error_msg)
        
        with open(report_file, "w", encoding="utf-8") as log:
            log.write('\n'.join(log_lines))
        return
    
    if not dict_file.exists():
        error_msg = "No se encontró el archivo a7_Diccionario.txt"
        error_msg += "\nEjecuta primero actividad7() para generar el diccionario."
        log_lines.append(error_msg)
        print(error_msg)
        
        with open(report_file, "w", encoding="utf-8") as log:
            log.write('\n'.join(log_lines))
        return
    
    # Step 1: Extract unique documents and assign IDs
    log_lines.append("=== PASO 1: CREANDO ÍNDICE DE DOCUMENTOS ===")
    log_lines.append("-" * 70)
    
    index_start = time.time()
    
    unique_documents = OrderedDict()  # Preserves insertion order
    document_id_map = {}  # {filename: doc_id}
    doc_id_counter = 1
    
    # Read posting file to extract all document names
    with open(posting_file_to_use, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line (format depends on whether it's weighted or not)
            if has_weights:
                # Weighted format: "Archivo    Peso" (fixed width)
                if len(line) >= 8:
                    filename = line[:8].strip()
                else:
                    continue
            else:
                # Regular format: "Archivo;Frecuencia"
                parts = line.split(';')
                if len(parts) >= 1:
                    filename = parts[0].strip()
                else:
                    continue
            
            # Add to unique documents if not seen before
            if filename and filename not in unique_documents:
                unique_documents[filename] = doc_id_counter
                document_id_map[filename] = doc_id_counter
                doc_id_counter += 1
    
    index_end = time.time()
    index_time = index_end - index_start
    
    log_lines.append(f"Total documentos únicos encontrados: {len(unique_documents)}")
    log_lines.append(f"Tiempo creando índice: {index_time:.6f} segundos")
    log_lines.append("")
    
    # Step 2: Write documents file
    log_lines.append("=== PASO 2: ESCRIBIENDO ARCHIVO DE DOCUMENTOS ===")
    log_lines.append("-" * 70)
    
    write_docs_start = time.time()
    
    # Get full paths for documents (try to find actual files)
    html_sources_dir = base_dir.parent / "data" / "html_sources"
    
    documents_lines = []
    documents_lines.append(f"{'ID':<5}{'Documento':<50}\n")  # Header
    
    for filename, doc_id in unique_documents.items():
        # Try to find full path
        full_path = None
        if html_sources_dir.exists():
            potential_file = html_sources_dir / filename
            if potential_file.exists():
                full_path = str(potential_file)
            else:
                full_path = filename  # Just use filename if not found
        else:
            full_path = filename
        
        # Format: ID (5 chars) + Documento (50 chars) = 55 bytes (not exactly 80, but reasonable)
        # Actually, let's make it divisible by 80: 80 bytes = ID (10) + Documento (70)
        documents_lines.append(f"{doc_id:<10}{full_path:<70}\n")
    
    with open(documents_file, 'w', encoding='utf-8') as f:
        f.writelines(documents_lines)
    
    write_docs_end = time.time()
    write_docs_time = write_docs_end - write_docs_start
    
    log_lines.append(f"Archivo de documentos creado: {documents_file}")
    log_lines.append(f"Total documentos: {len(unique_documents)}")
    log_lines.append(f"Tiempo escribiendo archivo: {write_docs_time:.6f} segundos")
    log_lines.append("")
    
    # Step 3: Read dictionary and posting, create indexed versions
    log_lines.append("=== PASO 3: CREANDO POSTING Y DICCIONARIO INDEXADOS ===")
    log_lines.append("-" * 70)
    
    posting_start = time.time()
    
    # Read dictionary
    token_list = []  # List of (token, repetitions, num_docs)
    with open(dict_file, 'r', encoding='utf-8') as f:
        # No header in dictionary file from actividad7 - format: token;repetitions;num_docs
        position = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(';')
            if len(parts) >= 3:
                token = parts[0]
                repetitions = int(parts[1])
                num_docs = int(parts[2])
                token_list.append((token, repetitions, num_docs))
                # Position is cumulative based on num_docs
                position += num_docs
    
    # Read posting and create indexed version
    indexed_posting_data = []  # List of (token, doc_id, weight/frequency)
    
    with open(posting_file_to_use, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        
        for token, num_docs, position in token_list:
            # Read num_docs entries for this token
            for _ in range(num_docs):
                line = f.readline().strip()
                if not line:
                    break
                
                if has_weights:
                    # Weighted format: "Archivo    Peso" (fixed width)
                    if len(line) >= 8:
                        filename = line[:8].strip()
                        weight_str = line[8:].strip() if len(line) > 8 else "0"
                        try:
                            weight = int(weight_str)
                        except ValueError:
                            weight = 0
                    else:
                        continue
                else:
                    # Regular format: "Archivo;Frecuencia"
                    parts = line.split(';')
                    if len(parts) >= 2:
                        filename = parts[0].strip()
                        weight = int(parts[1])  # Using frequency as weight
                    else:
                        continue
                
                # Get document ID
                doc_id = document_id_map.get(filename, 0)
                if doc_id == 0:
                    continue  # Skip if document not found
                
                indexed_posting_data.append((token, doc_id, weight))
    
    posting_end = time.time()
    posting_time = posting_end - posting_start
    
    log_lines.append(f"Total registros procesados: {len(indexed_posting_data)}")
    log_lines.append(f"Tiempo procesando posting: {posting_time:.6f} segundos")
    log_lines.append("")
    
    # Step 4: Write indexed posting and dictionary files
    log_lines.append("=== PASO 4: ESCRIBIENDO ARCHIVOS INDEXADOS ===")
    log_lines.append("-" * 70)
    
    write_start = time.time()
    
    # Fixed column sizes (divisible by 80 bytes)
    # Posting: 10 bytes per line (DocID: 5 chars + Peso: 5 chars = 10 bytes)
    # Dictionary: 20 bytes per line (Token: 15 chars + N°Docs: 5 chars = 20 bytes)
    POST_COL_SIZE = 10
    DICT_COL_SIZE = 20
    
    # Write indexed posting file
    indexed_posting_lines = []
    indexed_posting_lines.append(f"{'DocID':<5}{'Peso':<5}\n")  # Header (10 bytes)
    
    # Group posting data by token (maintain order)
    posting_by_token = defaultdict(list)
    for token, doc_id, weight in indexed_posting_data:
        posting_by_token[token].append((doc_id, weight))
    
    # Write in token order
    for token, num_docs, position in token_list:
        if token in posting_by_token:
            for doc_id, weight in sorted(posting_by_token[token]):  # Sort by doc_id
                # Format: DocID (5 chars) + Peso (5 chars) = 10 bytes
                weight_str = str(min(99999, int(weight)))[:5]  # Cap at 5 digits
                line = f"{doc_id:<5}{weight_str:<5}\n"
                indexed_posting_lines.append(line)
    
    with open(indexed_post_file, 'w', encoding='utf-8') as f:
        f.writelines(indexed_posting_lines)
    
    # Write indexed dictionary file
    indexed_dict_lines = []
    indexed_dict_lines.append(f"{'Token':<15}{'N°Docs':<5}\n")  # Header (20 bytes)
    
    position = 0
    for token, repetitions, num_docs in token_list:
        # Format: Token (15 chars) + N°Docs (5 chars) = 20 bytes
        token_short = token[:15] if len(token) > 15 else token
        line = f"{token_short:<15}{num_docs:<5}\n"
        indexed_dict_lines.append(line)
        position += num_docs
    
    with open(indexed_dict_file, 'w', encoding='utf-8') as f:
        f.writelines(indexed_dict_lines)
    
    write_end = time.time()
    write_time = write_end - write_start
    
    log_lines.append(f"Archivo de documentos: {documents_file}")
    log_lines.append(f"Archivo posting indexado: {indexed_post_file}")
    log_lines.append(f"Archivo diccionario indexado: {indexed_dict_file}")
    log_lines.append(f"Tamaño columna posting: {POST_COL_SIZE} bytes")
    log_lines.append(f"Tamaño columna diccionario: {DICT_COL_SIZE} bytes")
    log_lines.append(f"Tiempo escribiendo archivos: {write_time:.6f} segundos")
    log_lines.append("")
    
    # Step 5: Statistics
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "=== ESTADÍSTICAS ===",
        f"Total documentos únicos: {len(unique_documents)}",
        f"Total tokens únicos: {len(token_list)}",
        f"Total registros en posting: {len(indexed_posting_data)}",
        "",
        "=== TIEMPOS ===",
        f"Tiempo creando índice: {index_time:.6f} segundos",
        f"Tiempo escribiendo documentos: {write_docs_time:.6f} segundos",
        f"Tiempo procesando posting: {posting_time:.6f} segundos",
        f"Tiempo escribiendo archivos indexados: {write_time:.6f} segundos",
        f"Tiempo total de ejecución: {total_program_time:.6f} segundos",
        "",
        "Proceso completado correctamente."
    ])
    
    # Write report file
    with open(report_file, 'w', encoding='utf-8') as log:
        log.write('\n'.join(log_lines))
    
    print(f"\nActividad 11 completada.")
    print(f"Archivos generados:")
    print(f"  - Archivo de documentos: {documents_file}")
    print(f"  - Posting indexado: {indexed_post_file}")
    print(f"  - Diccionario indexado: {indexed_dict_file}")
    print(f"  - Reporte: {report_file}")
    print(f"Total documentos: {len(unique_documents)}")
    print(f"Total registros: {len(indexed_posting_data)}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")


def cleanFolders(clean_data=True, clean_results=True):
    """
    Clean output directories to start fresh.
    
    Args:
        clean_data: If True, clean data/extracted_text and data/sorted_words
        clean_results: If True, clean results/ directory
    """
    import shutil
    from pathlib import Path
    
    print("=== LIMPIANDO DIRECTORIOS ===")
    
    script_dir = Path(__file__).parent
    cleaned_folders = []
    errors = []
    
    if clean_data:
        # Clean extracted text files
        extracted_text_dir = script_dir / "data" / "extracted_text"
        if extracted_text_dir.exists():
            try:
                files = list(extracted_text_dir.glob("*_clean.txt"))
                file_count = len(files)
                for file in files:
                    file.unlink()
                cleaned_folders.append(f"data/extracted_text/ ({file_count} archivos)")
                print(f"✓ Limpiado: {extracted_text_dir} ({file_count} archivos)")
            except Exception as e:
                errors.append(f"Error limpiando data/extracted_text: {e}")
        
        # Clean sorted words files
        sorted_words_dir = script_dir / "data" / "sorted_words"
        if sorted_words_dir.exists():
            try:
                files = list(sorted_words_dir.glob("*_words_sorted.txt"))
                file_count = len(files)
                for file in files:
                    file.unlink()
                cleaned_folders.append(f"data/sorted_words/ ({file_count} archivos)")
                print(f"✓ Limpiado: {sorted_words_dir} ({file_count} archivos)")
            except Exception as e:
                errors.append(f"Error limpiando data/sorted_words: {e}")
    
    if clean_results:
        results_dir = script_dir / "results"
        if results_dir.exists():
            try:
                # Clean tokenized files
                tokenized_dir = results_dir / "tokenized"
                if tokenized_dir.exists():
                    for file in tokenized_dir.glob("*_tokens.txt"):
                        file.unlink()
                    cleaned_folders.append(f"results/tokenized/")
                
                # Clean dictionary_posting files
                dict_posting_dir = results_dir / "dictionary_posting"
                if dict_posting_dir.exists():
                    for file in dict_posting_dir.glob("*.txt"):
                        file.unlink()
                    cleaned_folders.append(f"results/dictionary_posting/")
                
                # Clean report files
                reports_dir = results_dir / "reports"
                if reports_dir.exists():
                    for file in reports_dir.glob("*.txt"):
                        file.unlink()
                    cleaned_folders.append(f"results/reports/")
                
                # Clean root results files
                for file in results_dir.glob("*.txt"):
                    file.unlink()
                
                # Clean other result files
                for pattern in ["consolidated_*.txt", "dictionary*.txt", "posting*.txt", "diccionario*.txt", "actividad*.txt"]:
                    for file in results_dir.glob(pattern):
                        file.unlink()
                
                cleaned_folders.append(f"results/ (archivos raíz)")
                print(f"✓ Limpiado: {results_dir}")
            except Exception as e:
                errors.append(f"Error limpiando results: {e}")
    
    print(f"\n=== RESUMEN DE LIMPIEZA ===")
    if cleaned_folders:
        print(f"Directorios limpiados: {len(cleaned_folders)}")
        for folder in cleaned_folders:
            print(f"  - {folder}")
    else:
        print("No se encontraron directorios para limpiar.")
    
    if errors:
        print(f"\nErrores encontrados: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    
    print("\nLimpieza completada.")
    print("Nota: Los archivos HTML fuente en data/html_sources/ NO fueron eliminados.")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Tokenizador de archivos HTML')
    parser.add_argument('input_dir', help='Directorio de entrada con archivos HTML')
    parser.add_argument('output_dir', help='Directorio de salida para archivos tokenizados')
    parser.add_argument('--mode', choices=['all', 'actividad5'], default='actividad5',
                       help='Modo de ejecución: all (actividades 1-4) o actividad5 (solo tokenización)')
    
    args = parser.parse_args()
    
    if args.mode == 'all':
        print("=== PROYECTO HTML - ACTIVIDADES 1, 2, 3 y 4 ===\n")
        
        actividad1()
        print("\n" + "="*60 + "\n")
        
        actividad2()
        print("\n" + "="*60 + "\n")
        
        actividad3()
        print("\n" + "="*60 + "\n")
        
        actividad4()
    else:
        actividad5(args.input_dir, args.output_dir)
        print("\n" + "="*60 + "\n")
        actividad6(args.input_dir, args.output_dir)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("=== PROYECTO HTML - ACTIVIDADES 1, 2, 3, 4, 5, 6, 7, 8 y 9 ===\n")

        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        input_dir = script_dir / "data" / "html_sources"
        output_dir = script_dir / "results"
        stoplist_path = script_dir / "stoplist.txt"    

        
        print("Ejecutando actividad 5 (tokenización)...")
        actividad5(str(input_dir), str(output_dir))
        print("\n" + "="*60 + "\n")
        
        print("Ejecutando actividad 6 (diccionario con conteo de archivos)...")
        actividad6(str(input_dir), str(output_dir))
        print("\n" + "="*60 + "\n")
        
        print("Ejecutando actividad 7 (diccionario y posting)...")
        actividad7(str(output_dir))
        print("\n" + "="*60 + "\n")
        
        print("Ejecutando actividad 8 (diccionario con hash table)...")
        actividad8(str(output_dir))
        print("\n" + "="*60 + "\n")
        
        print("Ejecutando actividad 9 (refinamiento del diccionario)...")
        actividad9(str(output_dir), str(stoplist_path))
        print("\n" + "="*60 + "\n")

        print("="*60)
        
    else:
        main()