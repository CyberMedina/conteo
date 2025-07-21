import pandas as pd

# Datos de muestra con una mezcla de casos limpios y problemáticos
data = [
    # --- Casos que deberían pasar la limpieza ---
    ['Toyota', 'Hilux', 'Rojo', 2022],
    ['NISSAN', 'FRONTIER 4X4', 'NEGRO', 2023],
    ['  hyundai', 'Accent con extras', 'Blanco Perla', 'año 2021'],
    ['Kia', 'Rio Sedan', '  plata', 2020],
    ['Mitsubishi', 'L200', 'Gris Oscuro', 2024.0], # Año como decimal
    ['TOYOTA', 'Yaris', 'BLANCO', 'fabricado en 2023'],

    # --- Casos diseñados para ir al archivo de revisión ---
    ['Suzuki', 'Grand Vitara', 'Verde Militar', 2019], # "Verde Militar" no está en la lista maestra
    ['Mazda', 'BT-50', 'Rojo Vino', 'N/A'],           # Año inválido
    ['Honda', 'CRV', 'Turquesa', 2022],              # "Turquesa" no está en la lista maestra
    ['Toyota', 'Corolla', 'Blanco', None],           # Año vacío/nulo
    ['Marca Hyundai', None, 'Negro', 2018],          # Modelo vacío/nulo
    ['Nissan', 'Sentra', None, 2017],                # Color vacío/nulo
    ['Tesla', 'Model 3', 'Rojo multicapas', '2025'], # Otro color que no estará en la lista
    [None, 'Pathfinder', 'Azul', 2016],              # Marca vacía/nula
    ['Ford', 'Ranger', 'Gris', 'veinte diecinueve']  # Año como texto inválido
]

# Crear un DataFrame de Pandas
df = pd.DataFrame(data)

# Nombre del archivo de salida
nombre_archivo = 'datos_de_prueba_vehiculos.xlsx'

# Guardar en un archivo Excel sin el índice y sin la fila de encabezado
# para que coincida con el formato que lee tu script
df.to_excel(nombre_archivo, index=False, header=False)

print(f"¡Éxito! ✨ Se ha creado el archivo '{nombre_archivo}' con {len(data)} filas de prueba.")
print("Ya puedes usar este archivo para probar tu script de limpieza.")