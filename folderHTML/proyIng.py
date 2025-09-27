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
    