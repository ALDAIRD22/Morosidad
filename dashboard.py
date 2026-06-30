import pandas as pd
import numpy as np

# ==========================================
# 1. CARGAR Y LIMPIAR TABLA: BIMENSUAL
# ==========================================
print("Procesando tabla BIMENSUAL...")

# Cargar el archivo asegurando que la primera fila se lea como datos
df_bimensual_raw = pd.read_csv("Todo_aldair_2026_BIMENSUAL.csv", header=None)

# Asignar la primera fila como encabezado y limpiar los nombres de columnas
df_bimensual_raw.columns = df_bimensual_raw.iloc[0].str.strip()
df_bimensual = df_bimensual_raw.iloc[1:].reset_index(drop=True)

# Convertir columnas numéricas clave (reemplazando vacíos por NaN)
columnas_numericas_bim = [
    'ASIST. ALUMNOS', 'ASIST. TUTORES', 'ASISTENCIA Y PUNTUALIDAD', 
    'ENCUESTA S.T.', 'ASISTENCIA S.T.', 'STUDY TIME', 'CI', 'EPPFF', 
    'ORIENTACIÓN', 'CUMP. DE META', 'ASIST. EVALUACIONES', 'PLAN DE ACCIÓN', 
    'META ACADÉMICA', 'DESERCIÓN', 'ENCUESTA TUTOR', 'PART. ENC. DOCENTE', 
    'PROMEDIO FINAL EVA. Y DESEMPEÑO', 'NOTA FINAL'
]

for col in columnas_numericas_bim:
    if col in df_bimensual.columns:
        try:
            df_bimensual[col] = pd.to_numeric(df_bimensual[col], errors='raise')
        except Exception as e:
            # Si hay caracteres extraños, limpiamos espacios y reintentamos
            df_bimensual[col] = df_bimensual[col].astype(str).str.strip()
            df_bimensual[col] = pd.to_numeric(df_bimensual[col].replace(['', 'None', 'NaN'], np.nan), errors='coerce')

print("Tabla BIMENSUAL lista. Dimensiones:", df_bimensual.shape)


# ==========================================
# 2. CARGAR Y LIMPIAR TABLA: ANALISIS
# ==========================================
print("\nProcesando tabla ANALISIS...")

df_analisis_raw = pd.read_csv("Todo_aldair_2026_ANALISIS.csv", header=None)
df_analisis_raw.columns = df_analisis_raw.iloc[0].str.strip()
df_analisis = df_analisis_raw.iloc[1:].reset_index(drop=True)

# Filtrar filas donde el Tutor o Código estén vacíos (filas incompletas al final)
df_analisis = df_analisis.dropna(subset=['TUTOR', 'CÓDIGO']).reset_index(drop=True)

# Limpiar y convertir columnas numéricas
for col in ['ASISTENCIA', 'FALTA', 'NOTA']:
    if col in df_analisis.columns:
        df_analisis[col] = pd.to_numeric(df_analisis[col], errors='coerce')

print("Tabla ANALISIS lista. Dimensiones:", df_analisis.shape)


# ==========================================
# 3. CARGAR Y LIMPIAR TABLA: OLIMPIADAS
# ==========================================
print("\nProcesando tabla OLIMPIADAS...")

df_olimpiadas_raw = pd.read_csv("Todo_aldair_2026_OLIMPIADAS.csv", header=None)
df_olimpiadas_raw.columns = df_olimpiadas_raw.iloc[0].str.strip()
df_olimpiadas = df_olimpiadas_raw.iloc[1:].reset_index(drop=True)

# Excluir la fila de totales para evitar distorsiones en los promedios/análisis
df_olimpiadas = df_olimpiadas[df_olimpiadas['Tutor'].str.upper() != 'TOTALES'].reset_index(drop=True)

# Limpiar caracteres especiales de las columnas numéricas (como 'S/ ' o '%')
cols_limpiar = ['Matriculados', 'Meta ', 'Pagantes', 'Meta Dinero', 'EFECTIVO', 'YAPE', 'Recaudado', 'Falta', 'Avance %']
for col in cols_limpiar:
    if col in df_olimpiadas.columns:
        df_olimpiadas[col] = df_olimpiadas[col].astype(str)\
            .str.replace('S/', '', regex=False)\
            .str.replace('%', '', regex=False)\
            .str.replace('-', '0', regex=False)\
            .str.strip()
        df_olimpiadas[col] = pd.to_numeric(df_olimpiadas[col], errors='coerce')

print("Tabla OLIMPIADAS lista. Dimensiones:", df_olimpiadas.shape)


# ==========================================
# 4. CARGAR Y LIMPIAR TABLA: MOROSIDAD
# ==========================================
print("\nProcesando tabla MOROSIDAD...")

df_morosidad_raw = pd.read_csv("Todo_aldair_2026_MOROSIDAD.csv", header=None)

# Esta tabla contiene una estructura mixta. Extraemos el detalle de alumnos (columnas de la 23 en adelante)
df_detalle_alumnos = df_morosidad_raw.iloc[1:, 23:].reset_index(drop=True)
df_detalle_alumnos.columns = df_detalle_alumnos.iloc[0].str.strip()
df_detalle_alumnos = df_detalle_alumnos.iloc[1:].dropna(subset=['ALUMNO']).reset_index(drop=True)

print("Tabla Detalle de Morosidad de Alumnos lista. Dimensiones:", df_detalle_alumnos.shape)

# ==========================================
# EJEMPLO DE VISTA DE DATOS PROCESADOS
# ==========================================
print("\n--- RESUMEN DE NOTAS FINALES POR TUTOR (BIMENSUAL) ---")
print(df_bimensual[['PERIODO DE EVALUACION', 'TUTOR', 'NOTA FINAL']].head())
