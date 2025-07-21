import pandas as pd
import re

# --- 1. CATÁLOGO MAESTRO (SOLO PARA COLORES) ---
COLORES_MAESTROS = [
    'rojo', 'azul', 'blanco', 'negro', 'plata', 'gris', 'verde', 'amarillo',
    'perla', 'vino', 'beige', 'dorado', 'marrón', 'naranja'
    # Agrega todos los colores base que manejes...
]

# --- 2. FUNCIONES DE LIMPIEZA (Sin cambios) ---

def limpiar_marca_modelo(texto):
    if not isinstance(texto, str):
        return None
    palabras = texto.strip().lower().split()
    if palabras:
        return palabras[0].capitalize()
    return None

def estandarizar_color(texto, lista_maestra):
    if not isinstance(texto, str):
        return None
    texto_limpio = texto.lower()
    for valor_maestro in lista_maestra:
        if re.search(r'\b' + re.escape(valor_maestro) + r'\b', texto_limpio):
            return valor_maestro.capitalize()
    palabras = texto_limpio.split()
    if palabras:
        return palabras[0].capitalize()
    return texto

def limpiar_ano(valor):
    try:
        texto = str(valor)
        coincidencia = re.search(r'\b(19|20)\d{2}\b', texto)
        if coincidencia:
            return int(coincidencia.group(0))
        return pd.NA
    except:
        return pd.NA

# --- 3. EJECUCIÓN PRINCIPAL ---

# Nombres de archivos
archivo_entrada = 'vehiculos_desordenados.xlsx'
archivo_limpio_salida = 'vehiculos_estandarizados.xlsx'
archivo_revision_salida = 'vehiculos_para_revision.xlsx'
archivo_conteo_salida = 'vehiculos_conteo_estandarizado.xlsx'

print(f" Cargando el archivo: {archivo_entrada}...")
try:
    df = pd.read_excel(archivo_entrada, header=None, names=['Marca', 'Modelo', 'Color', 'Año'])
except FileNotFoundError:
    print(f"Error: El archivo '{archivo_entrada}' no se encontró. Por favor, asegúrate de que el archivo exista en la misma carpeta que el script.")
    exit()

df_limpio = pd.DataFrame()
print("Aplicando limpieza y estandarización...")
df_limpio['Marca'] = df['Marca'].apply(limpiar_marca_modelo)
df_limpio['Modelo'] = df['Modelo'].apply(limpiar_marca_modelo)
df_limpio['Color'] = df['Color'].apply(lambda x: estandarizar_color(x, COLORES_MAESTROS))
df_limpio['Año'] = df['Año'].apply(limpiar_ano).astype('Int64')

# Unimos los datos originales con los limpios
df_final = pd.concat([df.add_suffix('_Original'), df_limpio], axis=1)

# --- 4. IDENTIFICAR Y SEPARAR FILAS ---
print("Identificando filas para revisión manual...")

condicion_ano = df_final['Año'].isna()
colores_maestros_capitalizados = [c.capitalize() for c in COLORES_MAESTROS]
condicion_color = ~df_final['Color'].isin(colores_maestros_capitalizados)
condicion_marca = df_final['Marca'].isna()
condicion_modelo = df_final['Modelo'].isna()

filas_para_revision_mask = condicion_ano | condicion_color | condicion_marca | condicion_modelo

df_revision = df_final[filas_para_revision_mask]
df_buenos = df_final[~filas_para_revision_mask]

# --- 5. GUARDAR RESULTADOS (LIMPIOS Y REVISIÓN) ---

if not df_buenos.empty:
    print(f" Guardando {len(df_buenos)} filas limpias en: {archivo_limpio_salida}...")
    # ### AJUSTE ### - Se guarda el DataFrame completo con columnas originales y limpias
    df_buenos.to_excel(archivo_limpio_salida, index=False)
else:
    print("No se encontraron filas completamente limpias.")

if not df_revision.empty:
    print(f" Guardando {len(df_revision)} filas para revisión en: {archivo_revision_salida}...")
    df_revision.to_excel(archivo_revision_salida, index=False)
else:
    print("¡Felicidades! Todas las filas se estandarizaron correctamente.")

# --- 6. GENERAR Y GUARDAR CONTEO ESTANDARIZADO ---

if not df_buenos.empty:
    print("Generando archivo de conteo estandarizado...")
    columnas_conteo = ['Marca', 'Modelo', 'Color', 'Año']
    df_conteo = df_buenos.groupby(columnas_conteo).size().reset_index(name='Cantidad')
    
    print(f" Guardando {len(df_conteo)} filas de conteo en: {archivo_conteo_salida}...")
    df_conteo.to_excel(archivo_conteo_salida, index=False)
else:
    print("No hay datos limpios para generar el archivo de conteo.")

print("\nProceso completado. ✨")