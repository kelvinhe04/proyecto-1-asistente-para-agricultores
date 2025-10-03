# main_simple.py
"""
ASISTENTE PARA AGRICULTORES - VERSION SIMPLIFICADA
Sistema principal sin emojis y con estructura modular
"""

import os
import sys
from datetime import datetime

# Importar módulos del proyecto
from base_datos_cultivos import cultivos_panama, listar_cultivos
from conexion_clima import ClimaAPI
from analisis_recomendaciones import AnalizadorAgricola
from visualizaciones import VisualizadorAgricola


class AsistenteAgricola:
    """
    Aplicación principal del asistente para agricultores
    Version simplificada sin emojis
    """
    
    def __init__(self):
        self.clima_api = ClimaAPI()
        self.analizador = AnalizadorAgricola()
        self.visualizador = VisualizadorAgricola()
        self.ciudad_actual = "Panama City"
        print("Sistema iniciado correctamente")
    
    def limpiar_pantalla(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_banner(self):
        """Muestra el banner de inicio"""
        print("\n" + "="*60)
        print("   ASISTENTE PARA AGRICULTORES DE PANAMA")
        print("="*60)
        print(f"Ciudad actual: {self.ciudad_actual}")
        print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("="*60 + "\n")
    
    def menu_principal(self):
        """Menú principal de la aplicación"""
        print("MENU PRINCIPAL")
        print("-" * 40)
        print("1. Ver clima actual")
        print("2. Recomendaciones de cultivos")
        print("3. Analizar cultivo especifico")
        print("4. Ver graficas")
        print("5. Calendario de siembra")
        print("6. Cambiar ciudad")
        print("7. Salir")
        print("-" * 40)
    
    def ver_clima_actual(self):
        """Muestra el clima actual"""
        print("\n" + "="*60)
        print("CLIMA ACTUAL")
        print("="*60 + "\n")
        
        clima = self.clima_api.obtener_clima_actual(self.ciudad_actual)
        
        if clima:
            print(f"Ubicacion: {clima['ciudad']}, {clima['pais']}")
            print(f"Fecha: {clima['fecha_hora']}")
            print(f"Temperatura: {clima['temperatura']} grados C")
            print(f"Sensacion termica: {clima['sensacion_termica']} grados C")
            print(f"Humedad: {clima['humedad']}%")
            print(f"Descripcion: {clima['descripcion'].capitalize()}")
            print(f"Lluvia ultima hora: {clima['lluvia_1h']} mm")
            print(f"Viento: {clima['velocidad_viento']} m/s")
        else:
            print("Error al obtener informacion del clima")
        
        input("\nPresiona ENTER para continuar...")
    
    def ver_recomendaciones(self):
        """Muestra recomendaciones de cultivos"""
        print("\n" + "="*60)
        print("RECOMENDACIONES DE CULTIVOS")
        print("="*60 + "\n")
        
        print("Analizando condiciones climaticas actuales...")
        recomendaciones = self.analizador.recomendar_cultivos(self.ciudad_actual)
        
        if recomendaciones:
            clima = recomendaciones['clima_actual']
            print(f"\nUbicacion: {clima['ciudad']} - {clima['fecha_hora']}")
            print(f"Condiciones: {clima['temperatura']}C | Humedad: {clima['humedad']}% | {clima['descripcion']}")
            
            print("\n" + "-"*60)
            print("RANKING DE CULTIVOS (Mejores condiciones actuales)")
            print("-"*60 + "\n")
            
            for i, eval in enumerate(recomendaciones['evaluaciones'], 1):
                print(f"{i}. {eval['cultivo']} - {eval['nivel']} ({eval['puntaje']}/100)")
                
                if eval['alertas']:
                    print(f"   Alertas: {len(eval['alertas'])}")
                
                if i <= 3:  # Mostrar detalles de los top 3
                    for rec in eval['recomendaciones'][:2]:
                        print(f"      - {rec}")
                print()
        else:
            print("Error al obtener recomendaciones")
        
        input("\nPresiona ENTER para continuar...")
    
    def analizar_cultivo_especifico(self):
        """Analiza un cultivo específico en detalle"""
        print("\n" + "="*60)
        print("ANALISIS DE CULTIVO ESPECIFICO")
        print("="*60 + "\n")
        
        # Mostrar cultivos disponibles
        print("Cultivos disponibles:")
        cultivos = listar_cultivos()
        for i, cultivo in enumerate(cultivos, 1):
            nombre = cultivos_panama[cultivo]['nombre']
            print(f"  {i}. {nombre} ({cultivo})")
        
        print()
        cultivo_elegido = input("Escribe el nombre del cultivo (ej: maiz): ").lower().strip()
        
        if cultivo_elegido not in cultivos_panama:
            print("\nCultivo no encontrado")
            input("\nPresiona ENTER para continuar...")
            return
        
        print(f"\nGenerando reporte completo para {cultivos_panama[cultivo_elegido]['nombre']}...\n")
        
        # Generar reporte
        reporte = self.analizador.generar_reporte_completo(self.ciudad_actual, cultivo_elegido)
        
        if reporte:
            self.mostrar_reporte_simple(reporte)
        else:
            print("Error al generar el reporte")
        
        input("\nPresiona ENTER para continuar...")
    
    def mostrar_reporte_simple(self, reporte):
        """Muestra un reporte simplificado"""
        print("="*60)
        print(f"REPORTE: {reporte['cultivo']['nombre'].upper()}")
        print("="*60)
        
        # Informacion basica
        info = reporte['cultivo']
        print(f"\nInformacion basica:")
        print(f"- Tiempo de cosecha: {info['tiempo_cosecha']}")
        print(f"- Temporada: {info['temporada_siembra']}")
        print(f"- Temperatura ideal: {info['temp_min']}-{info['temp_max']} grados C")
        print(f"- Humedad ideal: {info['humedad_min']}-{info['humedad_max']}%")
        
        # Condiciones actuales
        clima = reporte['clima_actual']
        print(f"\nCondiciones actuales en {clima['ciudad']}:")
        print(f"- Temperatura: {clima['temperatura']} grados C")
        print(f"- Humedad: {clima['humedad']}%")
        print(f"- Descripcion: {clima['descripcion']}")
        
        # Evaluacion
        eval_info = reporte['evaluacion']
        print(f"\nEvaluacion: {eval_info['puntaje']}/100 - {eval_info['nivel']}")
        
        # Recomendaciones
        if eval_info['recomendaciones']:
            print(f"\nRecomendaciones:")
            for rec in eval_info['recomendaciones']:
                print(f"- {rec}")
        
        # Alertas
        if eval_info['alertas']:
            print(f"\nAlertas:")
            for alerta in eval_info['alertas']:
                print(f"- {alerta}")
    
    def menu_visualizaciones(self):
        """Menú de visualizaciones"""
        while True:
            print("\n" + "="*60)
            print("GRAFICAS Y VISUALIZACIONES")
            print("="*60 + "\n")
            
            print("1. Comparacion de todos los cultivos")
            print("2. Temperatura vs cultivo especifico")
            print("3. Precipitacion para cultivo especifico")
            print("4. Calendario de siembra anual")
            print("5. Volver al menu principal")
            
            opcion = input("\nSelecciona una opcion (1-5): ").strip()
            
            if opcion == '1':
                print("\nGenerando grafica...")
                self.visualizador.comparacion_cultivos(self.ciudad_actual)
            
            elif opcion == '2':
                cultivo = input("\nCultivo (maiz/arroz/tomate/yuca/frijol/platano/cebolla/sandia): ").lower().strip()
                if cultivo in cultivos_panama:
                    print("\nGenerando grafica...")
                    self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo)
                else:
                    print("Cultivo no valido")
                    input("\nPresiona ENTER para continuar...")
            
            elif opcion == '3':
                cultivo = input("\nCultivo (maiz/arroz/tomate/yuca/frijol/platano/cebolla/sandia): ").lower().strip()
                if cultivo in cultivos_panama:
                    print("\nGenerando grafica...")
                    self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo)
                else:
                    print("Cultivo no valido")
                    input("\nPresiona ENTER para continuar...")
            
            elif opcion == '4':
                print("\nGenerando calendario...")
                self.visualizador.calendario_siembra()
            
            elif opcion == '5':
                break
            
            else:
                print("Opcion no valida")
                input("\nPresiona ENTER para continuar...")
    
    def ver_calendario(self):
        """Muestra el calendario de siembra"""
        print("\nGenerando calendario de siembra...")
        self.visualizador.calendario_siembra()
        input("\nPresiona ENTER para continuar...")
    
    def cambiar_ciudad(self):
        """Cambia la ciudad actual"""
        print("\n" + "="*60)
        print("CAMBIAR CIUDAD")
        print("="*60 + "\n")
        
        print("Ciudades comunes en Panama:")
        print("  - Panama City")
        print("  - David")
        print("  - Chitre")
        print("  - Santiago")
        print("  - Colon")
        
        nueva_ciudad = input("\nEscribe el nombre de la ciudad: ").strip()
        
        if nueva_ciudad:
            # Verificar si la ciudad existe
            print(f"\nVerificando {nueva_ciudad}...")
            clima = self.clima_api.obtener_clima_actual(nueva_ciudad)
            
            if clima:
                self.ciudad_actual = nueva_ciudad
                print(f"\nCiudad cambiada a: {clima['ciudad']}, {clima['pais']}")
            else:
                print(f"\nNo se pudo encontrar la ciudad '{nueva_ciudad}'")
                print("Manteniendo ciudad actual...")
        
        input("\nPresiona ENTER para continuar...")
    
    def ejecutar(self):
        """Ejecuta la aplicación principal"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_banner()
            self.menu_principal()
            
            opcion = input("\nSelecciona una opcion (1-7): ").strip()
            
            if opcion == '1':
                self.ver_clima_actual()
            
            elif opcion == '2':
                self.ver_recomendaciones()
            
            elif opcion == '3':
                self.analizar_cultivo_especifico()
            
            elif opcion == '4':
                self.menu_visualizaciones()
            
            elif opcion == '5':
                self.ver_calendario()
            
            elif opcion == '6':
                self.cambiar_ciudad()
            
            elif opcion == '7':
                print("\n" + "="*60)
                print("Gracias por usar el Asistente Agricola!")
                print("="*60 + "\n")
                sys.exit(0)
            
            else:
                print("\nOpcion no valida")
                input("\nPresiona ENTER para continuar...")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    try:
        app = AsistenteAgricola()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Aplicacion cerrada por el usuario")
        print("="*60 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("Por favor, verifica tu conexion a internet y tu API key")
        sys.exit(1)