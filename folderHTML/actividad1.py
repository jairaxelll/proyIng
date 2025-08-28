import os
import time
import re
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

def remove_html_tags(filename):
    """
    Recibe el nombre del archivo HTML como parámetro.
    Elimina las etiquetas HTML y crea un nuevo archivo sin etiquetas.
    Retorna el tiempo que tardó en procesar el archivo.
    """
    file_path = Path(FOLDER) / filename
    
    # Verificar que el archivo existe
    if not file_path.exists():
        print(f"El archivo {filename} no existe en {FOLDER}")
        return 0
    
    # Cronometrar el tiempo de procesamiento
    start_time = time.time()
    
    content = open_file(file_path)
    
    if content.startswith("Failed"):
        print(f"Error al leer {filename}: {content}")
        return 0
    
    # Eliminar etiquetas HTML usando regex
    clean_content = re.sub(r'<[^>]+>', '', content)

    # Crear carpeta de salida si no existe
    output_folder = Path('folderHTML/CleanFiles')
    output_folder.mkdir(parents=True, exist_ok=True)
    
    clean_filename = file_path.stem + '_clean.txt'
    output_path = output_folder / clean_filename

    # Guardar contenido limpio en el nuevo archivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    end_time = time.time()
    processing_time = end_time - start_time

    return processing_time

def create_log_file():
    """Procesa todos los archivos HTML y genera el archivo log con tiempos."""
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
    
    log_lines.append("=== REPORTE DE PROCESAMIENTO HTML ===")
    log_lines.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append("")
    log_lines.append("Archivos procesados:")
    log_lines.append("-" * 50)
    
    for html_file in html_files:
        processing_time = remove_html_tags(html_file.name)
        total_processing_time += processing_time
        
        log_lines.append(f"{html_file.name:<30} {processing_time:.4f} segundos")
        print(f"Procesado: {html_file.name} en {processing_time:.4f} segundos")
    
    program_end = time.time()
    total_program_time = program_end - program_start
    
    log_lines.extend([
        "",
        "=== ESTADÍSTICAS ===",
        f"Archivos procesados: {len(html_files)}",
        f"Tiempo total procesando archivos: {total_processing_time:.4f} segundos",
        f"Tiempo promedio por archivo: {total_processing_time/len(html_files):.4f} segundos",
        f"Tiempo total del programa: {total_program_time:.4f} segundos",
        "",
        f"Diferencia (overhead del programa): {total_program_time - total_processing_time:.4f} segundos"
    ])
    
    log_path = Path('folderHTML/log_file.txt')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    print(f"\nReporte guardado en: {log_path}")
    print(f"Archivos limpios guardados en: folderHTML/CleanFiles/")
    print(f"\nRESUMEN:")
    print(f"- Archivos procesados: {len(html_files)}")
    print(f"- Tiempo total procesando: {total_processing_time:.4f} segundos")
    print(f"- Tiempo total del programa: {total_program_time:.4f} segundos")

def test_single_file():
    """Función para probar con un solo archivo (ejemplo de uso)"""
    filename = "001.html"  
    tiempo = remove_html_tags(filename)
    print(f"Tiempo para procesar {filename}: {tiempo:.4f} segundos")

if __name__ == "__main__":
    create_log_file()
        # test_single_file()