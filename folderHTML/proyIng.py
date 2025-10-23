import os
import time
import re
import sys
import argparse
from pathlib import Path
from collections import Counter
import html

# Default folder for backward compatibility
FOLDER = r'C:\Users\jairm\OneDrive\Documentos\proyIng\folderHTML\Files'

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
    
    log_path = Path('a1.txt')
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
    
    output_folder = Path('CleanFiles')
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
        f"Archivos limpios guardados en: ./CleanFiles/"
    ])
    
    log_path = Path('a2.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 2 completada.")
    print(f"Reporte guardado en: {log_path}")
    print(f"Archivos limpios guardados en: ./CleanFiles/")
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
    
    clean_file_path = Path('CleanFiles') / clean_filename
    
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
    
    words_folder = Path('SortedWords')
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
    
    clean_folder = Path('CleanFiles')
    if not clean_folder.exists():
        print("No se encontró la carpeta CleanFiles.")
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
        "Archivos de palabras ordenadas guardados en: ./SortedWords/"
    ])
    
    log_path = Path('a3.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 3 completada.")
    print(f"Reporte guardado en: {log_path}")
    print(f"Archivos de palabras ordenadas en: ./SortedWords/")
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
    consolidated_alpha_path = output_path / 'a5.txt'
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
    
    log_path = output_path / 'a5_log.txt'
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
    log_path = output_path / 'a6_matricula.txt'
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
    
    clean_folder = Path('CleanFiles')
    if not clean_folder.exists():
        print("No se encontró la carpeta CleanFiles.")
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
    
    log_path = Path('a4.txt')
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
    
    clean_file = Path('CleanFiles') / f"{Path(filename).stem}_clean.txt"
    if clean_file.exists():
        with open(clean_file, 'r', encoding='utf-8') as f:
            content_sample = f.read()[:200]
            print(f"Muestra del contenido limpio: {content_sample}...")
    
    clean_filename = f"{Path(filename).stem}_clean.txt"
    tiempo, palabras = extract_and_sort_words(clean_filename)
    print(f"Tiempo para extraer palabras de {clean_filename}: {tiempo:.6f} segundos")
    print(f"Palabras únicas encontradas: {palabras}")
    
    words_file = Path('SortedWords') / f"{Path(filename).stem}_words_sorted.txt"
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
import time
import hashlib
from collections import defaultdict

def actividad8(folder_path):
    """
    Actividad 8:
    Genera archivos 'diccionario_hash.txt', 'posting.txt' y 'a8_<matricula>.txt' (log de tiempos).
    Usa una hash table para almacenar los tokens.
    """

    matricula = "123456"  # 🔁 <-- Replace with your actual student ID

    # --- Step 1: Preparar estructuras de datos ---
    token_data = defaultdict(lambda: defaultdict(int))  # {token: {archivo: frecuencia}}
    hash_table = {}                                     # {hash_index: (token, num_docs, posting_pos)}
    colisiones = 0
    posting_data = []                                   # [(archivo, frecuencia)]

    # --- Step 2: Leer archivos y contar tiempos individuales ---
    start_total = time.time()
    log_lines = []

    for filename in os.listdir(folder_path):
        if not filename.endswith(".html"):
            continue

        filepath = os.path.join(folder_path, filename)
        start_file = time.time()

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()

        # Tokenización básica
        tokens = [word.strip(".,!?;:()[]{}\"'") for word in text.split()]
        for token in tokens:
            if token:
                token_data[token][filename] += 1

        end_file = time.time()
        log_lines.append(f"Archivo: {filename} -> Tiempo: {end_file - start_file:.4f} segundos")

    # --- Step 3: Crear archivo posting y calcular posiciones ---
    pos_in_posting = 0
    posting_file = "posting.txt"

    with open(posting_file, "w", encoding="utf-8") as post:
        for token, docs in token_data.items():
            # Guardar cada (archivo, frecuencia)
            for archivo, frecuencia in docs.items():
                post.write(f"{archivo}\t{frecuencia}\n")
                posting_data.append((archivo, frecuencia))

            # Calcular hash del token (tabla hash)
            hash_index = int(hashlib.sha1(token.encode()).hexdigest(), 16) % 101  # tamaño 101 recomendado (número primo)
            num_docs = len(docs)

            # Manejo de colisiones
            if hash_index in hash_table:
                colisiones += 1
                while hash_index in hash_table:  # linear probing
                    hash_index = (hash_index + 1) % 101

            hash_table[hash_index] = (token, num_docs, pos_in_posting)
            pos_in_posting += num_docs  # avanzar según el número de documentos

    # --- Step 4: Crear archivo diccionario hash (ASCII legible) ---
    with open("diccionario_hash.txt", "w", encoding="utf-8") as dic:
        dic.write("PosiciónHash\tToken\tNumDocs\tPosPosting\n")
        for i in range(101):
            if i in hash_table:
                token, num_docs, pos = hash_table[i]
                dic.write(f"{i}\t{token}\t{num_docs}\t{pos}\n")
            else:
                dic.write(f"{i}\t-\t0\t-1\n")

        dic.write(f"\nNúmero total de colisiones: {colisiones}\n")

    # --- Step 5: Crear archivo log (medición de tiempos) ---
    end_total = time.time()
    total_time = end_total - start_total

    log_file = f"a8_{matricula}.txt"
    with open(log_file, "w", encoding="utf-8") as log:
        log.write("== LOG DE TIEMPOS ==\n")
        log.write("\n".join(log_lines))
        log.write(f"\n\nTiempo total de procesamiento: {total_time:.4f} segundos\n")
        log.write(f"Número total de colisiones: {colisiones}\n")

    print("✅ Archivos generados exitosamente:")
    print("- diccionario_hash.txt")
    print("- posting.txt")
    print(f"- {log_file}")

                    
def actividad7():
    import os
    import re
    from collections import defaultdict, Counter

    base_dir = os.getcwd()
    token_dir = os.path.join(base_dir, "tokenized")  # folder with tokenized files
    output_dir = os.path.join(base_dir, "Diccionario_Posting")
    os.makedirs(output_dir, exist_ok=True)

    dict_file = os.path.join(output_dir, "Diccionario.txt")
    post_file = os.path.join(output_dir, "Posting.txt")
    report_file = os.path.join(output_dir, "a7.txt")

    with open(report_file, "w", encoding="utf-8") as log:
        log.write("Actividad 7: Creación del Diccionario y Archivo Posting\n\n")

        if not os.path.exists(token_dir):
            log.write(f"No se encontró la carpeta de tokens: {token_dir}\n")
            return

        log.write(f"Usando carpeta de tokens: {token_dir}\n")

        # Step 1: Collect all words per document
        word_docs = defaultdict(lambda: defaultdict(int))  # {token: {file: freq}}
        files = [f for f in os.listdir(token_dir) if f.endswith(".txt")]

        for file in files:
            file_path = os.path.join(token_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().lower()
                tokens = re.findall(r'\b\w+\b', text)
                counts = Counter(tokens)
                for token, freq in counts.items():
                    word_docs[token][file] = freq

        log.write(f"Archivos procesados: {len(files)}\n")
        log.write(f"Tokens únicos encontrados: {len(word_docs)}\n\n")

        # Step 2: Build posting and dictionary
        posting_lines = []
        dict_lines = []
        position = 0  # initial posting position

        for token in sorted(word_docs.keys()):
            docs = word_docs[token]
            num_docs = len(docs)

            # Add to dictionary file
            dict_lines.append(f"{token}\t{num_docs}\t{position}\n")

            # Add to posting file
            for doc, freq in docs.items():
                posting_lines.append(f"{doc}\t{freq}\n")

            # Update posting position for next token
            position += num_docs

        # Step 3: Write dictionary and posting files
        with open(dict_file, "w", encoding="utf-8") as df:
            df.write("Token\tN°Documentos\tPosiciónPrimerRegistro\n")
            df.writelines(dict_lines)

        with open(post_file, "w", encoding="utf-8") as pf:
            pf.write("Archivo\tFrecuencia\n")
            pf.writelines(posting_lines)

        log.write(f"Diccionario generado: {dict_file}\n")
        log.write(f"Archivo Posting generado: {post_file}\n")
        log.write("Proceso completado correctamente.\n")


    def actividad9(folder_path, stoplist_path="stoplist.txt"):
        """
        Actividad 9:
        Refinar el diccionario con una stop list, eliminar palabras de baja frecuencia
        y tokens de una sola letra o dígito. 
        Incluye medición de tiempos y reporte de factores del sistema.
        """

        matricula = "123456"  # 🔁 Reemplaza con tu matrícula

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

        # --- Step 2: Cargar stop list ---
        stop_words = set()
        if os.path.exists(stoplist_path):
            with open(stoplist_path, 'r', encoding='utf-8') as stopf:
                for line in stopf:
                    stop_words.add(line.strip().lower())

        # --- Step 3: Procesar archivos y crear conteos ---
        token_data = defaultdict(lambda: defaultdict(int))
        start_total = time.time()
        log_lines = []

        for filename in os.listdir(folder_path):
            if not filename.endswith(".html"):
                continue

            filepath = os.path.join(folder_path, filename)
            start_file = time.time()

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read().lower()

            # Tokenización básica
            tokens = [word.strip(".,!?;:()[]{}\"'") for word in text.split()]
            for token in tokens:
                if token and token not in stop_words:
                    token_data[token][filename] += 1

            end_file = time.time()
            log_lines.append(f"Archivo: {filename} -> Tiempo: {end_file - start_file:.4f} segundos")

        # --- Step 4: Filtros de refinamiento ---
        # a) Eliminar tokens de una sola letra o dígito
        # b) Eliminar tokens de baja frecuencia total
        refined_tokens = {}
        for token, docs in token_data.items():
            total_freq = sum(docs.values())
            if len(token) <= 1:
                continue
            if total_freq < 3:  # 🔁 criterio: frecuencia mínima 3 (ajústalo a gusto)
                continue
            refined_tokens[token] = docs

        # --- Step 5: Crear archivo posting y diccionario hash ---
        hash_table = {}
        posting_data = []
        posting_pos = 0
        colisiones = 0
        table_size = 101  # tamaño primo óptimo

        with open("posting_a9.txt", "w", encoding="utf-8") as post:
            for token, docs in refined_tokens.items():
                # Guardar en posting
                for archivo, freq in docs.items():
                    post.write(f"{archivo}\t{freq}\n")
                    posting_data.append((archivo, freq))

                num_docs = len(docs)
                hash_index = int(hashlib.sha1(token.encode()).hexdigest(), 16) % table_size

                # Manejo de colisiones (linear probing)
                if hash_index in hash_table:
                    colisiones += 1
                    while hash_index in hash_table:
                        hash_index = (hash_index + 1) % table_size

                hash_table[hash_index] = (token, num_docs, posting_pos)
                posting_pos += num_docs

        # --- Step 6: Generar diccionario refinado ---
        with open("diccionario_refinado.txt", "w", encoding="utf-8") as dic:
            dic.write("PosHash\tToken\tNumDocs\tPosPosting\n")
            for i in range(table_size):
                if i in hash_table:
                    token, num_docs, pos = hash_table[i]
                    dic.write(f"{i}\t{token}\t{num_docs}\t{pos}\n")
                else:
                    dic.write(f"{i}\t-\t0\t-1\n")

            dic.write(f"\nNúmero total de colisiones: {colisiones}\n")

        # --- Step 7: Crear log de tiempo y documentación técnica ---
        end_total = time.time()
        total_time = end_total - start_total
        log_file = f"a9_{matricula}.txt"

        with open(log_file, "w", encoding="utf-8") as log:
            log.write("== LOG DE TIEMPOS Y REFINAMIENTO ==\n\n")
            for line in log_lines:
                log.write(line + "\n")
            log.write(f"\nTiempo total de procesamiento: {total_time:.4f} segundos\n")
            log.write(f"Número total de colisiones: {colisiones}\n")
            log.write(f"Número total de tokens refinados: {len(refined_tokens)}\n")

            log.write("\n== Factores externos del sistema ==\n")
            for f in factores_externos:
                log.write(f"- {f}\n")

            log.write("\n== Factores de calidad interna ==\n")
            for q in calidad_interna:
                log.write(f"- {q}\n")

            log.write("\n== Historias de usuario ==\n")
            for h in historias_usuario:
                log.write(f"- {h}\n")

        print("✅ Archivos generados:")
        print("- posting_a9.txt")
        print("- diccionario_refinado.txt")
        print(f"- {log_file}")

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
        # Si no hay argumentos, ejecutar todas las actividades (1-6)
        print("=== PROYECTO HTML - ACTIVIDADES 1, 2, 3, 4, 5 y 6 ===\n")
        
        actividad1()
        print("\n" + "="*60 + "\n")
        
        actividad2()
        print("\n" + "="*60 + "\n")
        
        actividad3()
        print("\n" + "="*60 + "\n")
        
        actividad4()
        print("\n" + "="*60 + "\n")
        
        input_dir = "Files"
        output_dir = "output"
        actividad5(input_dir, output_dir)
        print("\n" + "="*60 + "\n")
        actividad6(input_dir, output_dir)
    else:
        main()
    