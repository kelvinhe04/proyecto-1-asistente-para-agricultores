# conexion_clima.py
"""
Módulo para conectarse a OpenWeatherMap API y obtener datos climáticos
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# Cargar variables de entorno
load_dotenv()

# Obtener API key
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# URLs base de la API
BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"


class ClimaAPI:
    """
    Clase para manejar las consultas a OpenWeatherMap API
    """
    
    def __init__(self, api_key=None):
        """
        Inicializa la conexión con la API
        """
        self.api_key = api_key or API_KEY
        
        if not self.api_key:
            raise ValueError("API key no encontrada. Verifica tu archivo .env")
    
    
    def obtener_clima_actual(self, ciudad, pais="PA"):
        """
        Obtiene el clima actual de una ciudad
        
        Args:
            ciudad (str): Nombre de la ciudad
            pais (str): Código del país (PA = Panamá)
            
        Returns:
            dict: Datos del clima actual
        """
        try:
            # Parámetros de la consulta
            params = {
                'q': f"{ciudad},{pais}",
                'appid': self.api_key,
                'units': 'metric',  # Celsius
                'lang': 'es'
            }
            
            # Realizar petición
            response = requests.get(BASE_URL_CURRENT, params=params)
            response.raise_for_status()  # Lanza error si falla
            
            data = response.json()
            
            # Extraer información relevante
            clima_actual = {
                'ciudad': data['name'],
                'pais': data['sys']['country'],
                'temperatura': data['main']['temp'],
                'sensacion_termica': data['main']['feels_like'],
                'temp_minima': data['main']['temp_min'],
                'temp_maxima': data['main']['temp_max'],
                'humedad': data['main']['humidity'],
                'presion': data['main']['pressure'],
                'descripcion': data['weather'][0]['description'],
                'velocidad_viento': data['wind']['speed'],
                'nubosidad': data['clouds']['all'],
                'fecha_hora': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Agregar lluvia si existe
            if 'rain' in data:
                clima_actual['lluvia_1h'] = data['rain'].get('1h', 0)
            else:
                clima_actual['lluvia_1h'] = 0
            
            return clima_actual
            
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return None
        except KeyError as e:
            print(f"Error al procesar datos: {e}")
            return None
    
    
    def obtener_pronostico_5dias(self, ciudad, pais="PA"):
        """
        Obtiene el pronóstico del clima para los próximos 5 días
        
        Args:
            ciudad (str): Nombre de la ciudad
            pais (str): Código del país
            
        Returns:
            pandas.DataFrame: Pronóstico organizado en tabla
        """
        try:
            # Parámetros de la consulta
            params = {
                'q': f"{ciudad},{pais}",
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'es'
            }
            
            # Realizar petición
            response = requests.get(BASE_URL_FORECAST, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Procesar pronósticos
            pronosticos = []
            
            for item in data['list']:
                pronostico = {
                    'fecha_hora': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                    'fecha': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    'hora': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
                    'temperatura': item['main']['temp'],
                    'temp_minima': item['main']['temp_min'],
                    'temp_maxima': item['main']['temp_max'],
                    'humedad': item['main']['humidity'],
                    'descripcion': item['weather'][0]['description'],
                    'velocidad_viento': item['wind']['speed'],
                    'probabilidad_lluvia': item.get('pop', 0) * 100,  # Convertir a porcentaje
                    'lluvia_3h': item.get('rain', {}).get('3h', 0)
                }
                pronosticos.append(pronostico)
            
            # Convertir a DataFrame
            df_pronostico = pd.DataFrame(pronosticos)
            
            return df_pronostico
            
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return None
        except KeyError as e:
            print(f"Error al procesar datos: {e}")
            return None
    
    
    def obtener_resumen_diario(self, ciudad, pais="PA"):
        """
        Obtiene un resumen diario del pronóstico (promedios por día)
        
        Args:
            ciudad (str): Nombre de la ciudad
            pais (str): Código del país
            
        Returns:
            pandas.DataFrame: Resumen por día
        """
        df_pronostico = self.obtener_pronostico_5dias(ciudad, pais)
        
        if df_pronostico is None:
            return None
        
        # Agrupar por fecha y calcular promedios
        resumen = df_pronostico.groupby('fecha').agg({
            'temperatura': 'mean',
            'temp_minima': 'min',
            'temp_maxima': 'max',
            'humedad': 'mean',
            'probabilidad_lluvia': 'max',
            'lluvia_3h': 'sum'
        }).round(2)
        
        resumen.columns = ['temp_promedio', 'temp_min', 'temp_max', 
                          'humedad_promedio', 'prob_lluvia_max', 'lluvia_total']
        
        return resumen


# Función auxiliar para uso rápido
def obtener_clima(ciudad):
    """
    Función rápida para obtener clima actual
    """
    clima_api = ClimaAPI()
    return clima_api.obtener_clima_actual(ciudad)


def obtener_pronostico(ciudad):
    """
    Función rápida para obtener pronóstico
    """
    clima_api = ClimaAPI()
    return clima_api.obtener_pronostico_5dias(ciudad)


# Ejemplo de uso
if __name__ == "__main__":
    print("=== PRUEBA DE CONEXIÓN CON API DEL CLIMA ===\n")
    
    # Crear instancia de la API
    clima = ClimaAPI()
    
    # Probar con Ciudad de Panamá
    ciudad = "Panama City"
    
    print(f"Obteniendo clima actual de {ciudad}...\n")
    clima_actual = clima.obtener_clima_actual(ciudad)
    
    if clima_actual:
        print("✓ CLIMA ACTUAL:")
        print(f"  Ciudad: {clima_actual['ciudad']}, {clima_actual['pais']}")
        print(f"  Temperatura: {clima_actual['temperatura']}°C")
        print(f"  Sensación térmica: {clima_actual['sensacion_termica']}°C")
        print(f"  Humedad: {clima_actual['humedad']}%")
        print(f"  Descripción: {clima_actual['descripcion']}")
        print(f"  Lluvia última hora: {clima_actual['lluvia_1h']} mm")
        print(f"  Fecha: {clima_actual['fecha_hora']}")
    else:
        print("✗ Error al obtener clima actual")
    
    print("\n" + "="*60 + "\n")
    
    print(f"Obteniendo pronóstico para {ciudad}...\n")
    pronostico = clima.obtener_pronostico_5dias(ciudad)
    
    if pronostico is not None:
        print("✓ PRONÓSTICO 5 DÍAS:")
        print(pronostico[['fecha', 'hora', 'temperatura', 'descripcion', 
                         'probabilidad_lluvia']].head(10))
        
        print("\n" + "="*60 + "\n")
        
        print("✓ RESUMEN DIARIO:")
        resumen = clima.obtener_resumen_diario(ciudad)
        print(resumen)
    else:
        print("✗ Error al obtener pronóstico")