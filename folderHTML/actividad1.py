import os
import time
import re
from pathlib import Path
from collections import Counter

# Ruta específica de los archivos
FOLDER = r'C:\Users\jairm\OneDrive\Documentos\proyIng\folderHTML\Files'

def open_file(file_path):
    """
    Función para abrir archivos con múltiples encodings.
    Utilizada en todas las actividades.
    """
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
    """
    ACTIVIDAD 1: Abrir archivos HTML y cronometrar tiempos.
    Genera reporte a1.txt
    """
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
    
    # Encabezado del reporte
    log_lines.append("=== ACTIVIDAD 1: REPORTE DE APERTURA DE ARCHIVOS HTML ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio: {FOLDER}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 60)
    
    # Procesar cada archivo HTML
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
    
    # Estadísticas
    log_lines.extend([
        "",
        "=== ESTADÍSTICAS ===",
        f"Total archivos encontrados: {len(html_files)}",
        f"Archivos abiertos exitosamente: {successful_files}",
        f"Tiempo total abriendo archivos: {total_opening_time:.6f} segundos",
        f"Tiempo promedio por archivo: {total_opening_time/successful_files if successful_files > 0 else 0:.6f} segundos",
        f"Tiempo total del programa: {total_program_time:.6f} segundos",
        f"Overhead del programa: {total_program_time - total_opening_time:.6f} segundos"
    ])
    
    # Guardar reporte
    log_path = Path('a1.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 1 completada.")
    print(f"Reporte guardado en: {log_path}")
    print(f"Archivos procesados: {successful_files}/{len(html_files)}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def remove_html_tags(filename):
    """
    Función para la Actividad 2: elimina etiquetas HTML de un archivo.
    Retorna el tiempo de procesamiento.
    """
    file_path = Path(FOLDER) / filename
    
    if not file_path.exists():
        print(f"El archivo {filename} no existe en {FOLDER}")
        return 0
    
    start_time = time.time()
    
    content = open_file(file_path)
    
    if content.startswith("Failed"):
        print(f"Error al leer {filename}: {content}")
        return 0
    
    # Eliminar etiquetas HTML usando regex
    clean_content = re.sub(r'<[^>]+>', '', content)
    
    # Crear carpeta de salida si no existe
    output_folder = Path('CleanFiles')
    output_folder.mkdir(exist_ok=True)
    
    clean_filename = file_path.stem + '_clean.txt'
    output_path = output_folder / clean_filename
    
    # Guardar contenido limpio
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return processing_time

def actividad2():
    """
    ACTIVIDAD 2: Eliminar etiquetas HTML y cronometrar tiempos.
    Genera reporte a2.txt
    """
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
    
    # Encabezado del reporte
    log_lines.append("=== ACTIVIDAD 2: REPORTE DE ELIMINACIÓN DE ETIQUETAS HTML ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Directorio: {FOLDER}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 60)
    
    # Procesar cada archivo HTML
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
    
    # Estadísticas
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
    
    # Guardar reporte
    log_path = Path('a2.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nActividad 2 completada.")
    print(f"Reporte guardado en: {log_path}")
    print(f"Archivos limpios guardados en: ./CleanFiles/")
    print(f"Archivos procesados: {successful_files}/{len(html_files)}")
    print(f"Tiempo total: {total_program_time:.6f} segundos")

def process_words(text):
    """
    Procesa el texto para extraer palabras, manejando caracteres especiales.
    
    Lógica para caracteres especiales:
    - Palabras con guiones (ej: "Automata-based") se mantienen como una sola palabra
    - Se eliminan signos de puntuación al final/inicio de palabras
    - Se convierten a minúsculas para consistencia
    - Se eliminan palabras muy cortas (menos de 2 caracteres)
    """
    text = text.lower()
    
    # Encontrar palabras usando regex
    # Incluye letras, números y guiones internos
    word_pattern = r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ][a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9\-]*[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9]\b|\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]\b'
    words = re.findall(word_pattern, text)
    
    cleaned_words = []
    for word in words:
        word = word.strip('-')
        if len(word) >= 2 and not word.isdigit():
            cleaned_words.append(word)
    
    return cleaned_words

def extract_and_sort_words(clean_filename):
    """
    Extrae palabras de un archivo limpio y las ordena alfabéticamente.
    """
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
    """
    ACTIVIDAD 3: Extraer y ordenar palabras de archivos limpios.
    Genera reporte a3.txt
    """
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

def test_single_file():
    """Función para probar con un solo archivo"""
    filename = "001.html"
    print(f"Probando con archivo: {filename}")
    
    tiempo = remove_html_tags(filename)
    print(f"Tiempo para procesar {filename}: {tiempo:.6f} segundos")
    
    clean_filename = "001_clean.txt"
    tiempo, palabras = extract_and_sort_words(clean_filename)
    print(f"Tiempo para extraer palabras de {clean_filename}: {tiempo:.6f} segundos")
    print(f"Palabras únicas encontradas: {palabras}")

if __name__ == "__main__":
    print("=== PROYECTO HTML - ACTIVIDADES 1, 2 y 3 ===\n")
    
    actividad1()
    print("\n" + "="*60 + "\n")
    
    actividad2()
    print("\n" + "="*60 + "\n")
    
    actividad3()