# historial.py
"""
Sistema de historial de consultas simplificado
Guarda y recupera consultas de usuarios
"""

import csv
import os
from datetime import datetime


class HistorialConsultas:
    """
    Maneja el historial de consultas del sistema agricola
    Version simplificada usando CSV
    """
    
    def __init__(self, archivo_csv="historial_consultas.csv"):
        self.archivo_csv = archivo_csv
        self.crear_archivo_si_no_existe()
    
    def crear_archivo_si_no_existe(self):
        """Crea el archivo CSV si no existe"""
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow([
                    'fecha_hora', 'ciudad', 'cultivo', 'temperatura', 
                    'humedad', 'puntaje', 'nivel', 'tipo_consulta'
                ])
            print(f"Archivo de historial creado: {self.archivo_csv}")
    
    def guardar_consulta(self, ciudad, cultivo="", temperatura=0, humedad=0, 
                        puntaje=0, nivel="", tipo_consulta="consulta_general"):
        """
        Guarda una consulta en el historial
        
        Args:
            ciudad (str): Ciudad consultada
            cultivo (str): Cultivo consultado (opcional)
            temperatura (float): Temperatura al momento de la consulta
            humedad (float): Humedad al momento de la consulta
            puntaje (int): Puntaje obtenido (para cultivos)
            nivel (str): Nivel de recomendacion
            tipo_consulta (str): Tipo de consulta realizada
        """
        try:
            fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(self.archivo_csv, 'a', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow([
                    fecha_hora, ciudad, cultivo, temperatura, 
                    humedad, puntaje, nivel, tipo_consulta
                ])
            
            return True
            
        except Exception as error:
            print(f"Error al guardar consulta: {error}")
            return False
    
    def obtener_historial(self, limite=10):
        """
        Obtiene las ultimas consultas del historial
        
        Args:
            limite (int): Numero maximo de consultas a retornar
            
        Returns:
            list: Lista de consultas
        """
        try:
            consultas = []
            
            with open(self.archivo_csv, 'r', encoding='utf-8') as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    consultas.append(fila)
            
            # Retornar las ultimas consultas (mas recientes primero)
            return consultas[-limite:][::-1] if consultas else []
            
        except Exception as error:
            print(f"Error al leer historial: {error}")
            return []
    
    def mostrar_historial_simple(self, limite=5):
        """
        Muestra el historial de forma simple en consola
        
        Args:
            limite (int): Numero de consultas a mostrar
        """
        consultas = self.obtener_historial(limite)
        
        if not consultas:
            print("No hay consultas en el historial")
            return
        
        print(f"\nULTIMAS {len(consultas)} CONSULTAS")
        print("-" * 50)
        
        for i, consulta in enumerate(consultas, 1):
            print(f"{i}. {consulta['fecha_hora']}")
            print(f"   Ciudad: {consulta['ciudad']}")
            
            if consulta['cultivo']:
                print(f"   Cultivo: {consulta['cultivo']}")
                print(f"   Condiciones: {consulta['temperatura']}C, {consulta['humedad']}% humedad")
                
                if consulta['puntaje'] and consulta['puntaje'] != '0':
                    print(f"   Evaluacion: {consulta['puntaje']}/100 - {consulta['nivel']}")
            
            print(f"   Tipo: {consulta['tipo_consulta']}")
            print()
    
    def obtener_estadisticas(self):
        """
        Obtiene estadisticas basicas del historial
        
        Returns:
            dict: Estadisticas del historial
        """
        consultas = self.obtener_historial(limite=1000)  # Todas las consultas
        
        if not consultas:
            return {
                'total_consultas': 0,
                'cultivos_mas_consultados': [],
                'ciudades_mas_consultadas': []
            }
        
        # Contar cultivos
        cultivos_count = {}
        ciudades_count = {}
        
        for consulta in consultas:
            # Contar cultivos
            if consulta['cultivo']:
                cultivo = consulta['cultivo']
                cultivos_count[cultivo] = cultivos_count.get(cultivo, 0) + 1
            
            # Contar ciudades
            ciudad = consulta['ciudad']
            ciudades_count[ciudad] = ciudades_count.get(ciudad, 0) + 1
        
        # Ordenar por frecuencia
        cultivos_mas_consultados = sorted(cultivos_count.items(), 
                                        key=lambda x: x[1], reverse=True)[:5]
        ciudades_mas_consultadas = sorted(ciudades_count.items(), 
                                        key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_consultas': len(consultas),
            'cultivos_mas_consultados': cultivos_mas_consultados,
            'ciudades_mas_consultadas': ciudades_mas_consultadas
        }
    
    def mostrar_estadisticas(self):
        """Muestra estadisticas del historial"""
        stats = self.obtener_estadisticas()
        
        print("\nESTADISTICAS DEL HISTORIAL")
        print("="*40)
        print(f"Total de consultas: {stats['total_consultas']}")
        
        if stats['cultivos_mas_consultados']:
            print(f"\nCultivos mas consultados:")
            for cultivo, count in stats['cultivos_mas_consultados']:
                print(f"  - {cultivo}: {count} consultas")
        
        if stats['ciudades_mas_consultadas']:
            print(f"\nCiudades mas consultadas:")
            for ciudad, count in stats['ciudades_mas_consultadas']:
                print(f"  - {ciudad}: {count} consultas")
    
    def limpiar_historial(self):
        """Limpia completamente el historial"""
        respuesta = input("Esta seguro de limpiar todo el historial? (si/no): ").lower()
        
        if respuesta == 'si':
            self.crear_archivo_si_no_existe()  # Esto recrea el archivo vacio
            print("Historial limpiado correctamente")
        else:
            print("Operacion cancelada")


# Funcion para probar el sistema de historial
def test_historial():
    """Funcion de prueba para el sistema de historial"""
    historial = HistorialConsultas()
    
    # Guardar algunas consultas de prueba
    historial.guardar_consulta(
        ciudad="Panama City",
        cultivo="maiz",
        temperatura=28,
        humedad=75,
        puntaje=85,
        nivel="BUENO",
        tipo_consulta="analisis_cultivo"
    )
    
    historial.guardar_consulta(
        ciudad="David",
        temperatura=26,
        humedad=80,
        tipo_consulta="consulta_clima"
    )
    
    # Mostrar historial
    historial.mostrar_historial_simple()
    
    # Mostrar estadisticas
    historial.mostrar_estadisticas()


if __name__ == "__main__":
    test_historial()