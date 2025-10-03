# base_datos_cultivos.py
"""
Base de datos de cultivos comunes en Panamá
Información basada en condiciones agroclimáticas de Panamá
Datos cargados desde archivo CSV
"""

import pandas as pd
import os

# Cargar datos desde CSV
def cargar_cultivos_desde_csv():
    """
    Carga los datos de cultivos desde el archivo CSV
    """
    try:
        # Obtener la ruta del archivo CSV
        directorio_actual = os.path.dirname(__file__)
        ruta_csv = os.path.join(directorio_actual, 'cultivos_panama.csv')
        
        # Leer el CSV
        df_cultivos = pd.read_csv(ruta_csv)
        
        # Convertir a diccionario con la misma estructura original
        cultivos_dict = {}
        
        for _, row in df_cultivos.iterrows():
            # Procesar temporada de siembra (convertir string a lista)
            temporadas = row['temporada_siembra'].split(',')
            temporadas = [temp.strip() for temp in temporadas]
            
            cultivos_dict[row['cultivo']] = {
                'nombre': row['nombre'],
                'duracion_dias': int(row['duracion_dias']),
                'temporada_siembra': temporadas,
                'temp_minima': float(row['temp_minima']),
                'temp_optima': float(row['temp_optima']),
                'temp_maxima': float(row['temp_maxima']),
                'precipitacion_min': float(row['precipitacion_min']),
                'precipitacion_optima': float(row['precipitacion_optima']),
                'precipitacion_max': float(row['precipitacion_max']),
                'humedad_optima': float(row['humedad_optima']),
                'tolerancia_sequia': row['tolerancia_sequia'],
                'tolerancia_lluvia': row['tolerancia_lluvia'],
                'descripcion': row['descripcion']
            }
        
        return cultivos_dict
        
    except FileNotFoundError:
        print("⚠️  Archivo cultivos_panama.csv no encontrado. Usando datos por defecto.")
        return cargar_cultivos_por_defecto()
    except Exception as e:
        print(f"⚠️  Error al cargar CSV: {e}. Usando datos por defecto.")
        return cargar_cultivos_por_defecto()

def cargar_cultivos_por_defecto():
    """
    Datos por defecto en caso de que falle la carga del CSV
    """
    return {
    'maiz': {
        'nombre': 'Maíz',
        'duracion_dias': 90,
        'temporada_siembra': ['abril', 'mayo', 'junio'],
        'temp_minima': 18,
        'temp_optima': 25,
        'temp_maxima': 32,
        'precipitacion_min': 400,  # mm durante el ciclo
        'precipitacion_optima': 600,
        'precipitacion_max': 800,
        'humedad_optima': 60,  # porcentaje
        'tolerancia_sequia': 'media',
        'tolerancia_lluvia': 'baja',
        'descripcion': 'Cultivo básico para alimentación y economía rural'
    },
    
    'arroz': {
        'nombre': 'Arroz',
        'duracion_dias': 120,
        'temporada_siembra': ['mayo', 'junio', 'julio'],
        'temp_minima': 20,
        'temp_optima': 28,
        'temp_maxima': 35,
        'precipitacion_min': 1000,
        'precipitacion_optima': 1500,
        'precipitacion_max': 2000,
        'humedad_optima': 80,
        'tolerancia_sequia': 'baja',
        'tolerancia_lluvia': 'alta',
        'descripcion': 'Requiere abundante agua, ideal para zonas húmedas'
    },
    
    'tomate': {
        'nombre': 'Tomate',
        'duracion_dias': 75,
        'temporada_siembra': ['marzo', 'abril', 'septiembre', 'octubre'],
        'temp_minima': 15,
        'temp_optima': 24,
        'temp_maxima': 30,
        'precipitacion_min': 300,
        'precipitacion_optima': 500,
        'precipitacion_max': 700,
        'humedad_optima': 65,
        'tolerancia_sequia': 'media',
        'tolerancia_lluvia': 'baja',
        'descripcion': 'Sensible al exceso de humedad, prefiere estación seca'
    },
    
    'yuca': {
        'nombre': 'Yuca',
        'duracion_dias': 240,
        'temporada_siembra': ['abril', 'mayo', 'junio', 'julio'],
        'temp_minima': 20,
        'temp_optima': 27,
        'temp_maxima': 35,
        'precipitacion_min': 600,
        'precipitacion_optima': 1000,
        'precipitacion_max': 1500,
        'humedad_optima': 65,
        'tolerancia_sequia': 'alta',
        'tolerancia_lluvia': 'media',
        'descripcion': 'Cultivo resistente, se adapta a diversas condiciones'
    },
    
    'frijol': {
        'nombre': 'Frijol',
        'duracion_dias': 70,
        'temporada_siembra': ['mayo', 'junio', 'agosto'],
        'temp_minima': 18,
        'temp_optima': 23,
        'temp_maxima': 28,
        'precipitacion_min': 300,
        'precipitacion_optima': 450,
        'precipitacion_max': 600,
        'humedad_optima': 60,
        'tolerancia_sequia': 'media',
        'tolerancia_lluvia': 'baja',
        'descripcion': 'Ciclo corto, sensible al exceso de agua'
    },
    
    'platano': {
        'nombre': 'Plátano',
        'duracion_dias': 300,
        'temporada_siembra': ['todo el año'],  # Cultivo perenne
        'temp_minima': 18,
        'temp_optima': 27,
        'temp_maxima': 35,
        'precipitacion_min': 1200,
        'precipitacion_optima': 2000,
        'precipitacion_max': 3000,
        'humedad_optima': 75,
        'tolerancia_sequia': 'baja',
        'tolerancia_lluvia': 'alta',
        'descripcion': 'Requiere humedad constante, importante en Panamá'
    },
    
    'cebolla': {
        'nombre': 'Cebolla',
        'duracion_dias': 100,
        'temporada_siembra': ['enero', 'febrero', 'septiembre', 'octubre'],
        'temp_minima': 13,
        'temp_optima': 20,
        'temp_maxima': 25,
        'precipitacion_min': 350,
        'precipitacion_optima': 500,
        'precipitacion_max': 650,
        'humedad_optima': 60,
        'tolerancia_sequia': 'media',
        'tolerancia_lluvia': 'baja',
        'descripcion': 'Prefiere temperaturas frescas y baja humedad'
    },
    
    'sandia': {
        'nombre': 'Sandía',
        'duracion_dias': 90,
        'temporada_siembra': ['enero', 'febrero', 'marzo'],
        'temp_minima': 18,
        'temp_optima': 26,
        'temp_maxima': 32,
        'precipitacion_min': 400,
        'precipitacion_optima': 550,
        'precipitacion_max': 700,
        'humedad_optima': 65,
        'tolerancia_sequia': 'media',
        'tolerancia_lluvia': 'baja',
        'descripcion': 'Necesita clima cálido y seco durante la maduración'
    }
}

# Cargar datos de cultivos (desde CSV o por defecto)
cultivos_panama = cargar_cultivos_desde_csv()


def obtener_cultivo(nombre_cultivo):
    """
    Obtiene información de un cultivo específico
    """
    nombre_cultivo = nombre_cultivo.lower()
    if nombre_cultivo in cultivos_panama:
        return cultivos_panama[nombre_cultivo]
    else:
        return None


def listar_cultivos():
    """
    Lista todos los cultivos disponibles
    """
    return list(cultivos_panama.keys())


def cultivos_por_temporada(mes):
    """
    Retorna cultivos que se pueden sembrar en un mes específico
    """
    mes = mes.lower()
    cultivos_disponibles = []
    
    for cultivo, datos in cultivos_panama.items():
        if mes in [m.lower() for m in datos['temporada_siembra']] or 'todo el año' in datos['temporada_siembra']:
            cultivos_disponibles.append(cultivo)
    
    return cultivos_disponibles


# Ejemplo de uso
if __name__ == "__main__":
    print("=== BASE DE DATOS DE CULTIVOS DE PANAMÁ ===")
    print("📄 Datos cargados desde: cultivos_panama.csv")
    print(f"📊 Total de cultivos: {len(cultivos_panama)}")
    print("="*50 + "\n")
    
    # Listar todos los cultivos
    print("Cultivos disponibles:")
    for cultivo in listar_cultivos():
        print(f"  - {cultivo.capitalize()}")
    
    print("\n" + "="*50 + "\n")
    
    # Ejemplo: información del maíz
    maiz = obtener_cultivo('maiz')
    if maiz:
        print(f"Información del {maiz['nombre']}:")
        print(f"  Duración: {maiz['duracion_dias']} días")
        print(f"  Temporada: {', '.join(maiz['temporada_siembra'])}")
        print(f"  Temperatura óptima: {maiz['temp_optima']}°C")
        print(f"  Precipitación óptima: {maiz['precipitacion_optima']} mm")
    
    print("\n" + "="*50 + "\n")
    
    # Cultivos para sembrar en mayo
    print("Cultivos recomendados para sembrar en Mayo:")
    for cultivo in cultivos_por_temporada('mayo'):
        datos = obtener_cultivo(cultivo)
        print(f"  - {datos['nombre']}")