"""
Organizador automático de descargas que clasifica archivos según su tipo.

Este script organiza automáticamente los archivos en la carpeta de descargas,
creando carpetas por categorías y moviendo los archivos correspondientes.

Características principales:
- Organización por categorías (imágenes, documentos, videos, música, etc.)
- Manejo de subcategorías para documentos
- Evita sobrescritura de archivos duplicados
- Muestra el progreso durante la organización
"""

import os
from pathlib import Path
from collections import defaultdict

def organizar_descargas(directorio_descargas):
    # Definir extensiones y categorías
    categorias = {
        "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Documentos": {
            "PDF": [".pdf"],
            "Word": [".doc", ".docx"],
            "Excel": [".xls", ".xlsx"],
            "Presentaciones": [".ppt", ".pptx"],
            "Textos": [".txt", ".csv"]
        },
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
        "Música": [".mp3", ".wav", ".aac", ".flac"],
        "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Ejecutables": [".exe", ".msi", ".bat", ".sh"],
        "PowerBI": [".pbix"],  # Nueva categoría para PowerBI
        "Otros": []
    }

    # Crear un diccionario para mapear extensiones a categorías
    extensiones_a_categorias = defaultdict(lambda: ("Otros", None))
    for categoria, subcategorias in categorias.items():
        if isinstance(subcategorias, dict):  # Categorías con subcarpetas (como Documentos)
            for subcategoria, extensiones in subcategorias.items():
                for extension in extensiones:
                    extensiones_a_categorias[extension.lower()] = (categoria, subcategoria)
        else:  # Categorías sin subcarpetas
            for extension in subcategorias:
                extensiones_a_categorias[extension.lower()] = (categoria, None)

    print("Categorías y extensiones mapeadas correctamente.")
    print(f"Procesando archivos en: {directorio_descargas}")

    # Mover archivos a sus respectivas carpetas
    for archivo in Path(directorio_descargas).iterdir():
        if archivo.is_file():
            extension = archivo.suffix.lower()  # Normalizar extensión a minúsculas
            categoria, subcategoria = extensiones_a_categorias[extension]

            # Definir carpeta destino
            if subcategoria:  # Si pertenece a una subcategoría (por ejemplo, PDF dentro de Documentos)
                carpeta_destino = Path(directorio_descargas) / categoria / subcategoria
            else:  # Categoría principal
                carpeta_destino = Path(directorio_descargas) / categoria

            # Crear la carpeta destino si no existe
            carpeta_destino.mkdir(parents=True, exist_ok=True)

            # Evitar sobrescribir archivos con el mismo nombre
            destino = carpeta_destino / archivo.name
            contador = 1
            while destino.exists():
                nuevo_nombre = f"{archivo.stem}_{contador}{archivo.suffix}"
                destino = carpeta_destino / nuevo_nombre
                contador += 1

            # Mover archivo y mostrar resultado
            try:
                archivo.rename(destino)
                print(f"Archivo movido: {archivo.name} -> {destino}")
            except Exception as e:
                print(f"Error al mover {archivo.name}: {e}")

    print("Organización completada.")

# Ruta de la carpeta Descargas
directorio_descargas = str(Path.home() / "Downloads")

# Llamar a la función
organizar_descargas(directorio_descargas)
