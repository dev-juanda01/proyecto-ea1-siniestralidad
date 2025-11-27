import pandas as pd
import sqlite3
import os

# --- 0. Definir Rutas ---
# Archivo CSV de entrada
input_csv_path = "data/SECTORES_CRITICOS_DE_SINIESTRALIDAD_VIAL_20251109.csv"

# Directorio de salida para la BD y el CSV
db_directory = "db"

# Ruta completa de la Base de Datos
db_path = os.path.join(db_directory, "proyecto.db")

# Ruta completa del CSV de exportación
output_csv_path = os.path.join(db_directory, "export.csv")

# Nombre de la tabla en la BD
table_name = "sectores_criticos"

print(f"--- Iniciando el Proceso (Paso 4) ---")

try:
    # --- 1. Crear Directorio ---
    # Aseguramos que la carpeta 'db' exista
    os.makedirs(db_directory, exist_ok=True)
    print(f"Directorio '{db_directory}' asegurado.")

    # --- 2. (CSV -> DataFrame) Cargar el dataset original ---
    # Leemos el CSV, tratando "<Null>" como un valor nulo (NaN)
    df = pd.read_csv(input_csv_path, na_values="<Null>")
    print(f"Dataset original '{input_csv_path}' cargado en Pandas: {df.shape[0]} filas, {df.shape[1]} columnas.")

    # --- 3. (DataFrame -> SQLite) Crear BD y cargar datos ---
    # Conectamos con la base de datos (se crea si no existe)
    conn = sqlite3.connect(db_path)
    
    # Cargamos el DataFrame en la tabla 'sectores_criticos'
    # if_exists='replace': borra la tabla si ya existe (útil para re-ejecutar)
    # index=False: no guarda el índice de Pandas como una columna
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    print(f"Datos cargados exitosamente en la tabla '{table_name}' de la BD '{db_path}'.")
    
    conn.close()
    print("Conexión a la BD cerrada (carga).")

    # --- 4. (SQLite -> DataFrame) Evidenciar flujo (EXPORTACIÓN) ---
    print(f"\n--- Iniciando Exportación (SQLite -> CSV) ---")
    
    # Nos conectamos de nuevo para leer los datos
    conn = sqlite3.connect(db_path)
    print(f"Re-conectado a {db_path} para consulta.")

    # Definimos la consulta SQL (Caso de Uso: Top 20 más críticos por fallecidos)
    # Usamos comillas dobles en "Fallecidos" por si acaso.
    query = """
    SELECT * FROM sectores_criticos 
    ORDER BY "Fallecidos" DESC 
    LIMIT 20
    """
    print(f"Ejecutando consulta: {query.strip()}")

    # Ejecutamos la consulta y cargamos el resultado en un nuevo DataFrame
    df_from_db = pd.read_sql_query(query, conn)
    print(f"Consulta exitosa. Se obtuvieron {df_from_db.shape[0]} filas (Top 20).")
    
    conn.close()
    print("Conexión a la BD cerrada (consulta).")

    # --- 5. (DataFrame -> CSV) Guardar el CSV exportado ---
    # Guardamos el nuevo DataFrame (el del Top 20) en el archivo de exportación
    df_from_db.to_csv(output_csv_path, index=False)
    print(f"\n¡Éxito! Archivo exportado guardado en: {output_csv_path}")

except Exception as e:
    print(f"\n--- ¡ERROR! ---")
    print(f"Ocurrió un error durante la ejecución: {e}")