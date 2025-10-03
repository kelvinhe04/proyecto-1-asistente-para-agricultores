# sistema_agricola.py
"""
SISTEMA ASISTENTE AGRICOLA - VERSION SIMPLIFICADA
Sistema completo sin emojis y estructura modular clara
"""

import os
import sys
from datetime import datetime

# Importar módulos del proyecto
from base_datos_cultivos import cultivos_panama, listar_cultivos
from conexion_clima import ClimaAPI
from analisis_simple import AnalizadorAgricola, mostrar_reporte_simple
from visualizaciones import VisualizadorAgricola


class SistemaAgricola:
    """
    Sistema principal para asistente agricola
    Version simplificada y modular
    """
    
    def __init__(self):
        print("Iniciando Sistema Agricola...")
        self.clima_api = ClimaAPI()
        self.analizador = AnalizadorAgricola()
        self.visualizador = VisualizadorAgricola()
        self.ciudad_actual = "Panama City"
        print("Sistema iniciado correctamente\n")
    
    def limpiar_pantalla(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_header(self):
        """Muestra el encabezado del sistema"""
        print("="*60)
        print("    SISTEMA ASISTENTE AGRICOLA DE PANAMA")
        print("="*60)
        print(f"Ciudad: {self.ciudad_actual}")
        print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("="*60)
    
    def mostrar_menu(self):
        """Muestra el menu principal"""
        print("\nMENU PRINCIPAL")
        print("-" * 30)
        print("1. Consultar clima actual")
        print("2. Ver recomendaciones de cultivos")
        print("3. Analizar cultivo especifico")
        print("4. Ver calendario de siembra")
        print("5. Generar graficas")
        print("6. Cambiar ciudad")
        print("7. Salir del sistema")
        print("-" * 30)
    
    def consultar_clima(self):
        """Consulta y muestra el clima actual"""
        print("\n" + "="*50)
        print("CONSULTA DE CLIMA ACTUAL")
        print("="*50)
        
        clima = self.clima_api.obtener_clima_actual(self.ciudad_actual)
        
        if clima:
            print(f"\nUbicacion: {clima['ciudad']}, {clima['pais']}")
            print(f"Fecha y hora: {clima['fecha_hora']}")
            print("-" * 40)
            print(f"Temperatura: {clima['temperatura']} grados Celsius")
            print(f"Sensacion termica: {clima['sensacion_termica']} grados Celsius")
            print(f"Humedad: {clima['humedad']}%")
            print(f"Condicion: {clima['descripcion'].title()}")
            print(f"Precipitacion (1h): {clima['lluvia_1h']} mm")
            print(f"Velocidad del viento: {clima['velocidad_viento']} m/s")
        else:
            print("\nError: No se pudo obtener la informacion del clima")
            print("Verifique su conexion a internet o la ciudad ingresada")
        
        self.pausar()
    
    def ver_recomendaciones(self):
        """Muestra recomendaciones de cultivos"""
        print("\n" + "="*50)
        print("RECOMENDACIONES DE CULTIVOS")
        print("="*50)
        
        print("Analizando condiciones climaticas...")
        recomendaciones = self.analizador.recomendar_cultivos(self.ciudad_actual)
        
        if recomendaciones:
            clima = recomendaciones['clima_actual']
            print(f"\nAnalisis para: {clima['ciudad']}")
            print(f"Condiciones: {clima['temperatura']}C, {clima['humedad']}% humedad")
            print(f"Estado: {clima['descripcion']}")
            
            print("\n" + "-"*50)
            print("RANKING DE CULTIVOS RECOMENDADOS")
            print("-"*50)
            
            for i, cultivo in enumerate(recomendaciones['evaluaciones'][:5], 1):
                print(f"\n{i}. {cultivo['cultivo']} - {cultivo['nivel']}")
                print(f"   Puntaje: {cultivo['puntaje']}/100")
                
                # Mostrar 2 recomendaciones principales
                if cultivo['recomendaciones']:
                    for rec in cultivo['recomendaciones'][:2]:
                        print(f"   - {rec}")
                
                # Mostrar alertas si existen
                if cultivo['alertas']:
                    print(f"   ALERTAS: {len(cultivo['alertas'])}")
                    for alerta in cultivo['alertas'][:1]:
                        print(f"   ! {alerta}")
        else:
            print("\nError al obtener recomendaciones")
        
        self.pausar()
    
    def analizar_cultivo(self):
        """Analiza un cultivo especifico"""
        print("\n" + "="*50)
        print("ANALISIS DE CULTIVO ESPECIFICO")
        print("="*50)
        
        # Mostrar cultivos disponibles
        print("\nCultivos disponibles:")
        cultivos = listar_cultivos()
        for i, cultivo in enumerate(cultivos, 1):
            nombre = cultivos_panama[cultivo]['nombre']
            print(f"  {i}. {nombre}")
        
        # Solicitar cultivo
        print(f"\nCultivos: {', '.join(cultivos)}")
        cultivo_elegido = input("\nIngrese el cultivo a analizar: ").lower().strip()
        
        if cultivo_elegido not in cultivos_panama:
            print(f"\nError: Cultivo '{cultivo_elegido}' no encontrado")
            self.pausar()
            return
        
        print(f"\nGenerando reporte para {cultivos_panama[cultivo_elegido]['nombre']}...")
        
        # Generar reporte
        reporte = self.analizador.generar_reporte_completo(self.ciudad_actual, cultivo_elegido)
        
        if reporte:
            mostrar_reporte_simple(reporte)
            
            # Ofrecer grafica
            print("\n" + "="*50)
            respuesta = input("\nDesea ver grafica de temperatura? (s/n): ").lower()
            if respuesta == 's':
                self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo_elegido)
        else:
            print("Error al generar el reporte")
        
        self.pausar()
    
    def ver_calendario(self):
        """Muestra el calendario de siembra"""
        print("\n" + "="*50)
        print("CALENDARIO DE SIEMBRA ANUAL")
        print("="*50)
        
        print("\nGenerando calendario...")
        self.visualizador.calendario_siembra()
        self.pausar()
    
    def generar_graficas(self):
        """Menu para generar diferentes graficas"""
        while True:
            print("\n" + "="*50)
            print("GENERADOR DE GRAFICAS")
            print("="*50)
            
            print("\nOpciones disponibles:")
            print("1. Comparacion de todos los cultivos")
            print("2. Temperatura vs cultivo especifico")
            print("3. Precipitacion para cultivo")
            print("4. Calendario de siembra")
            print("5. Volver al menu principal")
            
            opcion = input("\nSeleccione una opcion (1-5): ").strip()
            
            if opcion == '1':
                print("\nGenerando comparacion de cultivos...")
                self.visualizador.comparacion_cultivos(self.ciudad_actual)
                
            elif opcion == '2':
                cultivos = listar_cultivos()
                print(f"\nCultivos disponibles: {', '.join(cultivos)}")
                cultivo = input("Ingrese el cultivo: ").lower().strip()
                
                if cultivo in cultivos_panama:
                    print(f"\nGenerando grafica de temperatura para {cultivo}...")
                    self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo)
                else:
                    print("Cultivo no valido")
                
            elif opcion == '3':
                cultivos = listar_cultivos()
                print(f"\nCultivos disponibles: {', '.join(cultivos)}")
                cultivo = input("Ingrese el cultivo: ").lower().strip()
                
                if cultivo in cultivos_panama:
                    print(f"\nGenerando grafica de precipitacion para {cultivo}...")
                    self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo)
                else:
                    print("Cultivo no valido")
                
            elif opcion == '4':
                print("\nGenerando calendario de siembra...")
                self.visualizador.calendario_siembra()
                
            elif opcion == '5':
                break
                
            else:
                print("Opcion no valida")
            
            if opcion in ['1', '2', '3', '4']:
                self.pausar()
    
    def cambiar_ciudad(self):
        """Permite cambiar la ciudad actual"""
        print("\n" + "="*50)
        print("CAMBIO DE CIUDAD")
        print("="*50)
        
        print(f"\nCiudad actual: {self.ciudad_actual}")
        print("\nCiudades sugeridas en Panama:")
        ciudades = ["Panama City", "David", "Chitre", "Santiago", "Colon", "Las Tablas"]
        
        for i, ciudad in enumerate(ciudades, 1):
            print(f"  {i}. {ciudad}")
        
        nueva_ciudad = input(f"\nIngrese nueva ciudad: ").strip()
        
        if nueva_ciudad:
            print(f"Verificando disponibilidad de {nueva_ciudad}...")
            
            # Probar conexion con la nueva ciudad
            clima = self.clima_api.obtener_clima_actual(nueva_ciudad)
            
            if clima:
                self.ciudad_actual = nueva_ciudad
                print(f"\nCiudad actualizada a: {clima['ciudad']}, {clima['pais']}")
                print(f"Temperatura actual: {clima['temperatura']}C")
            else:
                print(f"\nError: No se encontro informacion para '{nueva_ciudad}'")
                print("Manteniendo ciudad actual")
        
        self.pausar()
    
    def pausar(self):
        """Pausa el sistema esperando input del usuario"""
        input("\nPresione ENTER para continuar...")
    
    def ejecutar(self):
        """Ejecuta el bucle principal del sistema"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            self.mostrar_menu()
            
            opcion = input("\nSeleccione una opcion (1-7): ").strip()
            
            if opcion == '1':
                self.consultar_clima()
                
            elif opcion == '2':
                self.ver_recomendaciones()
                
            elif opcion == '3':
                self.analizar_cultivo()
                
            elif opcion == '4':
                self.ver_calendario()
                
            elif opcion == '5':
                self.generar_graficas()
                
            elif opcion == '6':
                self.cambiar_ciudad()
                
            elif opcion == '7':
                self.salir_sistema()
                
            else:
                print("\nOpcion no valida. Intente nuevamente.")
                self.pausar()
    
    def salir_sistema(self):
        """Sale del sistema de forma controlada"""
        print("\n" + "="*50)
        print("CERRANDO SISTEMA AGRICOLA")
        print("="*50)
        print("\nGracias por usar el Sistema Asistente Agricola")
        print("Desarrollado para agricultores de Panama")
        print("\n" + "="*50)
        sys.exit(0)


def main():
    """Funcion principal del sistema"""
    try:
        # Crear e iniciar el sistema
        sistema = SistemaAgricola()
        sistema.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\nSistema interrumpido por el usuario")
        print("Cerrando aplicacion...")
        sys.exit(0)
        
    except Exception as error:
        print(f"\nError inesperado: {error}")
        print("Verifique su conexion a internet y configuracion")
        print("Contacte soporte tecnico si el problema persiste")
        sys.exit(1)


if __name__ == "__main__":
    main()