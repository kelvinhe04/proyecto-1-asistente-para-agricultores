# config.py
"""
Configuracion del Sistema Asistente Agricola
Parametros y configuraciones centralizadas
"""

import os
from datetime import datetime

class ConfiguracionSistema:
    """
    Clase para manejar toda la configuracion del sistema
    """
    
    # Informacion del sistema
    NOMBRE_SISTEMA = "Sistema Asistente Agricola de Panama"
    VERSION = "1.0"
    FECHA_VERSION = "Octubre 2025"
    
    # Configuracion de archivos
    ARCHIVO_CULTIVOS = "cultivos_panama.csv"
    ARCHIVO_DATASET = "dataset_cultivos_panama.csv"
    ARCHIVO_HISTORIAL = "historial_consultas.csv"
    ARCHIVO_ENV = ".env"
    
    # Configuracion de API
    API_TIMEOUT = 10  # segundos
    REINTENTOS_API = 3
    
    # Configuracion de historial
    MAX_CONSULTAS_HISTORIAL = 1000
    CONSULTAS_MOSTRAR_DEFAULT = 10
    
    # Configuracion de visualizaciones
    TAMAÑO_FIGURA_DEFAULT = (10, 6)
    DPI_GRAFICAS = 100
    COLORES_GRAFICAS = ['#2E8B57', '#4169E1', '#DC143C', '#FF8C00', '#9932CC']
    
    # Ciudades predefinidas de Panama
    CIUDADES_PANAMA = [
        "Panama City",
        "San Miguelito", 
        "David",
        "Chitre",
        "Santiago",
        "Colon",
        "Las Tablas",
        "Arraijan",
        "La Chorrera",
        "Pacora"
    ]
    
    # Parametros de evaluacion de cultivos
    PUNTAJE_MAXIMO = 100
    PUNTAJE_EXCELENTE = 80
    PUNTAJE_BUENO = 60
    PUNTAJE_REGULAR = 40
    
    # Factores de penalizacion
    PENALIZACION_TEMPERATURA = 5
    PENALIZACION_HUMEDAD = 0.5
    PENALIZACION_TEMPORADA = 15
    
    # Mensajes del sistema
    MENSAJES = {
        'inicio': 'Iniciando Sistema Asistente Agricola...',
        'carga_exitosa': 'Sistema cargado correctamente',
        'error_conexion': 'Error de conexion. Verifique internet y API key',
        'cultivo_no_encontrado': 'Cultivo no encontrado en la base de datos',
        'ciudad_no_encontrada': 'Ciudad no encontrada. Verifique el nombre',
        'generando_reporte': 'Generando reporte completo...',
        'generando_grafica': 'Generando grafica...',
        'guardando_historial': 'Guardando consulta en historial...',
        'despedida': 'Gracias por usar el Sistema Asistente Agricola'
    }
    
    @classmethod
    def obtener_fecha_actual(cls):
        """Retorna la fecha actual formateada"""
        return datetime.now().strftime('%d/%m/%Y %H:%M')
    
    @classmethod
    def obtener_año_actual(cls):
        """Retorna el año actual"""
        return datetime.now().year
    
    @classmethod
    def obtener_mes_actual(cls):
        """Retorna el mes actual en español"""
        meses = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
            5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
            9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        return meses[datetime.now().month]
    
    @classmethod
    def validar_archivos_requeridos(cls):
        """
        Valida que todos los archivos necesarios existan
        
        Returns:
            dict: Estado de validacion de archivos
        """
        archivos_requeridos = [
            cls.ARCHIVO_CULTIVOS,
            cls.ARCHIVO_ENV
        ]
        
        archivos_opcionales = [
            cls.ARCHIVO_DATASET,
            cls.ARCHIVO_HISTORIAL
        ]
        
        estado = {
            'requeridos_ok': True,
            'archivos_faltantes': [],
            'archivos_opcionales_faltantes': []
        }
        
        # Verificar archivos requeridos
        for archivo in archivos_requeridos:
            if not os.path.exists(archivo):
                estado['requeridos_ok'] = False
                estado['archivos_faltantes'].append(archivo)
        
        # Verificar archivos opcionales
        for archivo in archivos_opcionales:
            if not os.path.exists(archivo):
                estado['archivos_opcionales_faltantes'].append(archivo)
        
        return estado
    
    @classmethod
    def obtener_info_sistema(cls):
        """
        Retorna informacion completa del sistema
        
        Returns:
            dict: Informacion del sistema
        """
        return {
            'nombre': cls.NOMBRE_SISTEMA,
            'version': cls.VERSION,
            'fecha_version': cls.FECHA_VERSION,
            'fecha_actual': cls.obtener_fecha_actual(),
            'año': cls.obtener_año_actual(),
            'mes': cls.obtener_mes_actual(),
            'ciudades_disponibles': len(cls.CIUDADES_PANAMA),
            'timeout_api': cls.API_TIMEOUT
        }


class ValidadorSistema:
    """
    Clase para validar el estado del sistema
    """
    
    @staticmethod
    def verificar_dependencias():
        """
        Verifica que todas las dependencias esten instaladas
        
        Returns:
            dict: Estado de las dependencias
        """
        dependencias = {
            'pandas': False,
            'requests': False,
            'matplotlib': False,
            'dotenv': False
        }
        
        try:
            import pandas
            dependencias['pandas'] = True
        except ImportError:
            pass
        
        try:
            import requests
            dependencias['requests'] = True
        except ImportError:
            pass
        
        try:
            import matplotlib
            dependencias['matplotlib'] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencias['dotenv'] = True
        except ImportError:
            pass
        
        return dependencias
    
    @staticmethod
    def verificar_api_key():
        """
        Verifica si la API key esta configurada
        
        Returns:
            bool: True si la API key existe
        """
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv('OPENWEATHER_API_KEY')
            return api_key is not None and len(api_key) > 0
        except:
            return False
    
    @staticmethod
    def diagnostico_completo():
        """
        Realiza un diagnostico completo del sistema
        
        Returns:
            dict: Resultado del diagnostico
        """
        # Verificar archivos
        estado_archivos = ConfiguracionSistema.validar_archivos_requeridos()
        
        # Verificar dependencias
        dependencias = ValidadorSistema.verificar_dependencias()
        
        # Verificar API key
        api_key_ok = ValidadorSistema.verificar_api_key()
        
        # Calcular estado general
        archivos_ok = estado_archivos['requeridos_ok']
        todas_dependencias = all(dependencias.values())
        
        sistema_ok = archivos_ok and todas_dependencias and api_key_ok
        
        return {
            'sistema_funcionando': sistema_ok,
            'archivos': estado_archivos,
            'dependencias': dependencias,
            'api_key_configurada': api_key_ok,
            'fecha_diagnostico': ConfiguracionSistema.obtener_fecha_actual()
        }


def mostrar_diagnostico():
    """Muestra el diagnostico del sistema"""
    print("="*60)
    print("DIAGNOSTICO DEL SISTEMA")
    print("="*60)
    
    diagnostico = ValidadorSistema.diagnostico_completo()
    
    if diagnostico['sistema_funcionando']:
        print("ESTADO: SISTEMA FUNCIONANDO CORRECTAMENTE")
    else:
        print("ESTADO: PROBLEMAS DETECTADOS")
    
    print(f"\nFecha diagnostico: {diagnostico['fecha_diagnostico']}")
    
    # Mostrar estado de archivos
    print(f"\nArchivos requeridos:")
    if diagnostico['archivos']['requeridos_ok']:
        print("  OK - Todos los archivos requeridos estan presentes")
    else:
        print("  ERROR - Archivos faltantes:")
        for archivo in diagnostico['archivos']['archivos_faltantes']:
            print(f"    - {archivo}")
    
    # Mostrar dependencias
    print(f"\nDependencias:")
    for dep, estado in diagnostico['dependencias'].items():
        estado_texto = "OK" if estado else "FALTANTE"
        print(f"  - {dep}: {estado_texto}")
    
    # Mostrar API key
    print(f"\nAPI Key:")
    if diagnostico['api_key_configurada']:
        print("  OK - API key configurada")
    else:
        print("  ERROR - API key no configurada en .env")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    # Ejecutar diagnostico si se ejecuta directamente
    mostrar_diagnostico()