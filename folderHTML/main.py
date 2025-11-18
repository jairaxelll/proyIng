import os
import time
import re
import sys
import argparse
from pathlib import Path
from collections import Counter
import html

# Default folder for backward compatibility
FOLDER = r'C:\Users\jairm\OneDrive\Documentos\proyIng\folderHTML\data\html_sources'

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
    
    clean_file_path = Path('data/extracted_text') / clean_filename
    
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
    
    # Save tokenized file
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, count in sorted(word_counter.items()):
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
    
    alphabetically_sorted = sorted(all_word_frequencies.items())
    consolidated_alpha_path = output_path / 'reports' / 'a5.txt'
    with open(consolidated_alpha_path, 'w', encoding='utf-8') as f:
        for word, count in alphabetically_sorted:
            f.write(f"{word} {count}\n")
    
    frequency_sorted = sorted(all_word_frequencies.items(), key=lambda x: (-x[1], x[0]))
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
    print(f"Archivo consolidado (alfabético): a5.txt")
    print(f"Archivo consolidado (por frecuencia): consolidated_tokens_freq.txt")
    print(f"Reporte guardado en: a5_log.txt")
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
    
    dictionary_path = output_path / 'dictionary.txt'
    with open(dictionary_path, 'w', encoding='utf-8') as f:
        for token, data in token_data.items():
            file_count = len(data['files'])
            token_length = len(token)
            f.write(f"{token}\t{data['count']}\t{file_count}\t{token_length}\n")
    
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
    all_words = set()
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
        all_words.update(words)
        
        file_end = time.time()
        processing_time = file_end - file_start
        total_consolidation_time += processing_time
        successful_files += 1
        
        log_lines.append(f"{clean_file.name:<40} {processing_time:.6f}s  {len(words):>6} palabras")
        print(f"Procesado: {clean_file.name} en {processing_time:.6f} segundos - {len(words)} palabras")
    
    consolidation_start = time.time()
    
    sorted_words = sorted(all_words)
    
    consolidated_path = Path('consolidated_words.txt')
    with open(consolidated_path, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(f"{word}\n")
    
    consolidation_end = time.time()
    consolidation_time = consolidation_end - consolidation_start
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "",
        f"tiempo total en crear el nuevo archivo: {consolidation_time:.2f} segundos",
        f"tiempo total de ejecucion: {total_program_time:.2f} segundos"
    ])
    
    log_path = Path('results/reports/activity_4_sorting.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 4 completada.")
    print(f"Archivo consolidado guardado en: {consolidated_path}")
    print(f"Reporte guardado en: {log_path}")
    print(f"Total palabras únicas: {len(sorted_words)}")
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

    dict_file = dict_posting_dir / "Diccionario.txt"
    post_file = dict_posting_dir / "Posting.txt"
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

    # Sort tokens alphabetically
    sorted_tokens = sorted(word_docs.keys())
    
    for token in sorted_tokens:
        docs = word_docs[token]
        num_docs = len(docs)

        # Add to dictionary: Token, N°Documentos, PosiciónPrimerRegistro
        dict_lines.append(f"{token}\t{num_docs}\t{position}\n")

        # Add to posting: Archivo, Frecuencia (sorted by filename)
        for doc in sorted(docs.keys()):
            freq = docs[doc]
            posting_lines.append(f"{doc}\t{freq}\n")

        # Update posting position for next token
        position += num_docs

    # Step 3: Write dictionary file
    with open(dict_file, "w", encoding="utf-8") as df:
        df.write("Token\tN°Documentos\tPosiciónPrimerRegistro\n")
        df.writelines(dict_lines)

    # Step 4: Write posting file
    with open(post_file, "w", encoding="utf-8") as pf:
        pf.write("Archivo\tFrecuencia\n")
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


def actividad8(output_dir="results"):
    """
    Actividad 8:
    Genera archivos 'diccionario_hash.txt', 'posting.txt' y 'a8_<matricula>.txt' (log de tiempos).
    Usa una hash table para almacenar los tokens.
    """
    import os
    import time
    import hashlib
    from collections import defaultdict
    from pathlib import Path

    matricula = "2878113"  
    print("=== EJECUTANDO ACTIVIDAD 8: DICCIONARIO CON HASH TABLE ===")

    base_dir = Path(output_dir)
    token_dir = base_dir / "tokenized"
    
    if not token_dir.exists():
        print(f"Error: El directorio tokenized {token_dir} no existe")
        print("Ejecuta primero actividad5() para generar los archivos tokenizados.")
        return

    # --- Step 1: Preparar estructuras de datos ---
    token_data = defaultdict(lambda: defaultdict(int))  # {token: {archivo: frecuencia}}
    hash_table = {}                                     # {hash_index: (token, num_docs, posting_pos)}
    colisiones = 0
    posting_data = []                                   # [(archivo, frecuencia)]

    # --- Step 2: Leer archivos tokenizados y contar tiempos individuales ---
    start_total = time.time()
    log_lines = []
    
    log_lines.append("=== ACTIVIDAD 8: REPORTE DE HASH TABLE ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Matrícula: {matricula}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 70)

    token_files = list(token_dir.glob("*_tokens.txt"))
    
    if not token_files:
        print("No se encontraron archivos tokenizados")
        return

    for token_file in token_files:
        start_file = time.time()
        
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
                            token_data[token][original_filename] = count
                        except ValueError:
                            continue
        except Exception as e:
            print(f"Error leyendo {token_file.name}: {e}")
            continue

        end_file = time.time()
        log_lines.append(f"c:\\cs13309\\files\\{original_filename} {end_file - start_file:.2f}")
        print(f"Procesado: {original_filename} en {end_file - start_file:.4f} segundos")

    posting_start = time.time()
    
    pos_in_posting = 0
    posting_file = base_dir / "posting.txt"
    
    # Calculate optimal table size (prime number, ~2x the number of tokens)
    def next_prime(n):
        """Find the next prime number >= n"""
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    return False
            return True
        
        while not is_prime(n):
            n += 1
        return n
    
    table_size = next_prime(len(token_data) * 2)  # Dynamic table size

    with open(posting_file, "w", encoding="utf-8") as post:
        # Sort tokens alphabetically for consistent ordering
        sorted_tokens = sorted(token_data.keys())
        
        for token in sorted_tokens:
            docs = token_data[token]
            
            for archivo in sorted(docs.keys()): 
                frecuencia = docs[archivo]
                post.write(f"{archivo}\t{frecuencia}\n")
                posting_data.append((archivo, frecuencia))

            # Calcular hash del token (tabla hash)
            hash_index = int(hashlib.sha1(token.encode()).hexdigest(), 16) % table_size
            num_docs = len(docs)
            original_hash = hash_index

            # Manejo de colisiones con linear probing
            collision_count = 0
            while hash_index in hash_table:
                colisiones += 1
                collision_count += 1
                hash_index = (hash_index + 1) % table_size
                
                # Prevent infinite loop in case table is full
                if collision_count >= table_size:
                    print(f"ERROR: Hash table llena para token '{token}'")
                    break

            if collision_count < table_size:
                hash_table[hash_index] = (token, num_docs, pos_in_posting)
            
            pos_in_posting += num_docs  # avanzar según el número de documentos

    posting_end = time.time()
    posting_time = posting_end - posting_start

    # --- Step 4: Crear archivo diccionario hash (ASCII legible) ---
    dict_start = time.time()
    
    dict_file = base_dir / "diccionario_hash.txt"
    with open(dict_file, "w", encoding="utf-8") as dic:
        dic.write("PosiciónHash\tToken\tNumDocs\tPosPosting\n")
        dic.write("-" * 70 + "\n")
        
        occupied_slots = 0
        for i in range(table_size):
            if i in hash_table:
                token, num_docs, pos = hash_table[i]
                dic.write(f"{i}\t{token}\t{num_docs}\t{pos}\n")
                occupied_slots += 1
            else:
                dic.write(f"{i}\t-\t0\t-1\n")

        dic.write("\n" + "=" * 70 + "\n")
        dic.write(f"Número total de colisiones: {colisiones}\n")
        dic.write(f"Slots ocupados: {occupied_slots}/{table_size}\n")
        dic.write(f"Factor de carga: {occupied_slots/table_size:.2%}\n")
    
    dict_end = time.time()
    dict_time = dict_end - dict_start

    # --- Step 5: Crear archivo log (medición de tiempos) ---
    end_total = time.time()
    total_time = end_total - start_total

    log_lines.extend([
        "",
        f"tiempo total en crear el nuevo archivo: {posting_time + dict_time:.2f} segundos",
        f"tiempo total de ejecucion: {total_time:.2f} segundos"
    ])

    log_file = base_dir / "reports" / f"activity_8_{matricula}.txt"
    with open(log_file, "w", encoding="utf-8") as log:
        log.write('\n'.join(log_lines))

    print(f"\n Archivos generados exitosamente:")
    print(f"- {dict_file}")
    print(f"- {posting_file}")
    print(f"- {log_file}")
    print(f"\nEstadísticas:")
    print(f"- Total tokens únicos: {len(token_data)}")
    print(f"- Total colisiones: {colisiones}")
    print(f"- Factor de carga: {len(hash_table)}/{table_size} ({len(hash_table)/table_size:.2%})")
    print(f"- Tiempo total: {total_time:.4f} segundos")

                    

def actividad9(output_dir="results", stoplist_path="stoplist.txt", min_frequency=3):
    """
    Actividad 9:
    Refinar el diccionario con una stop list, eliminar palabras de baja frecuencia
    y tokens de una sola letra o dígito. 
    Incluye medición de tiempos y reporte de factores del sistema.
    """
    import os
    import time
    import hashlib
    from collections import defaultdict
    from pathlib import Path

    matricula = "A00837763"  # 🔁 Reemplaza con tu matrícula

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
        "Como usuario, quiero eliminar palabras poco frecuentes para reducir el tamaño del diccionario final.",
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
    tokens_removed_low_freq = 0
    tokens_removed_stoplist = tokens_before_filter - len(token_data)
    
    for token, docs in token_data.items():
        # Calcular frecuencia total
        total_freq = sum(docs.values())
        
        # Filtro 1: Eliminar tokens de una sola letra o dígito
        if len(token) <= 1:
            tokens_removed_single_char += 1
            continue
        
        # Filtro 2: Eliminar tokens que son solo dígitos
        if token.isdigit():
            tokens_removed_single_char += 1
            continue
        
        # Filtro 3: Eliminar tokens de baja frecuencia
        if total_freq < min_frequency:
            tokens_removed_low_freq += 1
            continue
        
        refined_tokens[token] = docs

    print(f"Tokens antes del filtrado: {len(token_data)}")
    print(f"Tokens después del filtrado: {len(refined_tokens)}")
    print(f"Removidos por stop list: {tokens_removed_stoplist}")
    print(f"Removidos por longitud/dígitos: {tokens_removed_single_char}")
    print(f"Removidos por baja frecuencia: {tokens_removed_low_freq}")

    # --- Step 6: Crear archivo posting refinado ---
    posting_start = time.time()
    
    hash_table = {}
    posting_pos = 0
    colisiones = 0
    
    # Calculate optimal table size (prime number, ~2x the number of tokens)
    def next_prime(n):
        """Find the next prime number >= n"""
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    return False
            return True
        
        while not is_prime(n):
            n += 1
        return n
    
    table_size = next_prime(len(refined_tokens) * 2)  # Dynamic table size

    posting_file = base_dir / "posting_a9.txt"
    
    with open(posting_file, "w", encoding="utf-8") as post:
        # Sort tokens alphabetically
        sorted_tokens = sorted(refined_tokens.keys())
        
        for token in sorted_tokens:
            docs = refined_tokens[token]
            
            # Guardar en posting (ordenado por archivo)
            for archivo in sorted(docs.keys()):
                freq = docs[archivo]
                post.write(f"{archivo}\t{freq}\n")

            num_docs = len(docs)
            
            # Calcular hash del token
            hash_index = int(hashlib.sha1(token.encode()).hexdigest(), 16) % table_size

            # Manejo de colisiones (linear probing)
            collision_count = 0
            while hash_index in hash_table:
                colisiones += 1
                collision_count += 1
                hash_index = (hash_index + 1) % table_size
                
                if collision_count >= table_size:
                    print(f"ERROR: Hash table llena para token '{token}'")
                    break

            if collision_count < table_size:
                hash_table[hash_index] = (token, num_docs, posting_pos)
            
            posting_pos += num_docs

    posting_end = time.time()
    posting_time = posting_end - posting_start

    # --- Step 7: Generar diccionario refinado ---
    dict_start = time.time()
    
    dict_file = base_dir / "diccionario_refinado.txt"
    
    with open(dict_file, "w", encoding="utf-8") as dic:
        dic.write("PosHash\tToken\tNumDocs\tPosPosting\n")
        dic.write("-" * 70 + "\n")
        
        occupied_slots = 0
        for i in range(table_size):
            if i in hash_table:
                token, num_docs, pos = hash_table[i]
                dic.write(f"{i}\t{token}\t{num_docs}\t{pos}\n")
                occupied_slots += 1
            else:
                dic.write(f"{i}\t-\t0\t-1\n")

        dic.write("\n" + "=" * 70 + "\n")
        dic.write(f"Número total de colisiones: {colisiones}\n")
        dic.write(f"Slots ocupados: {occupied_slots}/{table_size}\n")
        dic.write(f"Factor de carga: {occupied_slots/table_size:.2%}\n")
        dic.write("\n=== ESTADÍSTICAS DE FILTRADO ===\n")
        dic.write(f"Tokens originales: {tokens_before_filter}\n")
        dic.write(f"Removidos por stop list: {tokens_removed_stoplist}\n")
        dic.write(f"Removidos por longitud/dígitos: {tokens_removed_single_char}\n")
        dic.write(f"Removidos por baja frecuencia (< {min_frequency}): {tokens_removed_low_freq}\n")
        dic.write(f"Tokens finales: {len(refined_tokens)}\n")
    
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
        f"Tokens removidos por baja frecuencia: {tokens_removed_low_freq}",
        f"Número total de colisiones: {colisiones}",
        f"Factor de carga: {len(hash_table)}/{table_size} ({len(hash_table)/table_size:.2%})"
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
        
         ()
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