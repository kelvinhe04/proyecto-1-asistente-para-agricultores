# main.py
"""
ASISTENTE PARA AGRICULTORES
Aplicación principal que integra análisis climático, recomendaciones y visualizaciones
"""

import os
import sys
from datetime import datetime

# Importar módulos del proyecto
from base_datos_cultivos import cultivos_panama, listar_cultivos
from conexion_clima import ClimaAPI
from analisis_recomendaciones import AnalizadorAgricola, imprimir_reporte
from visualizaciones import VisualizadorAgricola


class AsistenteAgricola:
    """
    Aplicación principal del asistente para agricultores
    """
    
    def __init__(self):
        self.clima_api = ClimaAPI()
        self.analizador = AnalizadorAgricola()
        self.visualizador = VisualizadorAgricola()
        self.ciudad_actual = "Panama City"
    
    
    def limpiar_pantalla(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    
    def mostrar_banner(self):
        """Muestra el banner de inicio"""
        print("\n" + "="*70)
        print(" 🌾  ASISTENTE PARA AGRICULTORES DE PANAMÁ  🌾 ")
        print("="*70)
        print(f"📍 Ciudad actual: {self.ciudad_actual}")
        print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("="*70 + "\n")
    
    
    def menu_principal(self):
        """Menú principal de la aplicación"""
        print("MENÚ PRINCIPAL")
        print("-" * 70)
        print("1. 🌤️  Ver clima actual")
        print("2. 📊 Recomendaciones de cultivos (qué sembrar ahora)")
        print("3. 🔍 Analizar cultivo específico (reporte completo)")
        print("4. 📈 Ver gráficas y visualizaciones")
        print("5. 📅 Calendario de siembra anual")
        print("6. ⚙️  Cambiar ciudad")
        print("7. ❌ Salir")
        print("-" * 70)
    
    
    def ver_clima_actual(self):
        """Muestra el clima actual"""
        print("\n" + "="*70)
        print("🌤️  CLIMA ACTUAL")
        print("="*70 + "\n")
        
        clima = self.clima_api.obtener_clima_actual(self.ciudad_actual)
        
        if clima:
            print(f"📍 {clima['ciudad']}, {clima['pais']}")
            print(f"📅 {clima['fecha_hora']}")
            print(f"\n🌡️  Temperatura: {clima['temperatura']}°C")
            print(f"🤔 Sensación térmica: {clima['sensacion_termica']}°C")
            print(f"💧 Humedad: {clima['humedad']}%")
            print(f"☁️  Descripción: {clima['descripcion'].capitalize()}")
            print(f"🌧️  Lluvia última hora: {clima['lluvia_1h']} mm")
            print(f"💨 Viento: {clima['velocidad_viento']} m/s")
        else:
            print("❌ Error al obtener información del clima")
        
        input("\nPresiona ENTER para continuar...")
    
    
    def ver_recomendaciones(self):
        """Muestra recomendaciones de cultivos"""
        print("\n" + "="*70)
        print("📊 RECOMENDACIONES DE CULTIVOS")
        print("="*70 + "\n")
        
        print("Analizando condiciones climáticas actuales...")
        recomendaciones = self.analizador.recomendar_cultivos(self.ciudad_actual)
        
        if recomendaciones:
            clima = recomendaciones['clima_actual']
            print(f"\n📍 {clima['ciudad']} - {clima['fecha_hora']}")
            print(f"🌡️  {clima['temperatura']}°C | 💧 {clima['humedad']}% | ☁️  {clima['descripcion']}")
            
            print("\n" + "-"*70)
            print("RANKING DE CULTIVOS (Mejores condiciones actuales)")
            print("-"*70 + "\n")
            
            for i, eval in enumerate(recomendaciones['evaluaciones'], 1):
                print(f"{i}. {eval['color']} {eval['cultivo']} - {eval['nivel']} ({eval['puntaje']}/100)")
                
                if eval['alertas']:
                    print(f"   ⚠️  Alertas: {len(eval['alertas'])}")
                
                if i <= 3:  # Mostrar detalles de los top 3
                    for rec in eval['recomendaciones'][:2]:
                        print(f"      • {rec}")
                
                print()
            
            # Mostrar gráfica de comparación
            print("-"*70)
            respuesta = input("\n¿Deseas ver la gráfica de comparación? (s/n): ").lower()
            if respuesta == 's':
                self.visualizador.comparacion_cultivos(self.ciudad_actual)
        else:
            print("❌ Error al obtener recomendaciones")
        
        input("\nPresiona ENTER para continuar...")
    
    
    def analizar_cultivo_especifico(self):
        """Analiza un cultivo específico en detalle"""
        print("\n" + "="*70)
        print("🔍 ANÁLISIS DE CULTIVO ESPECÍFICO")
        print("="*70 + "\n")
        
        # Mostrar cultivos disponibles
        print("Cultivos disponibles:")
        cultivos = listar_cultivos()
        for i, cultivo in enumerate(cultivos, 1):
            nombre = cultivos_panama[cultivo]['nombre']
            print(f"  {i}. {nombre} ({cultivo})")
        
        print()
        cultivo_elegido = input("Escribe el nombre del cultivo (ej: maiz): ").lower().strip()
        
        if cultivo_elegido not in cultivos_panama:
            print("\n❌ Cultivo no encontrado")
            input("\nPresiona ENTER para continuar...")
            return
        
        print(f"\n⏳ Generando reporte completo para {cultivos_panama[cultivo_elegido]['nombre']}...\n")
        
        # Generar reporte
        reporte = self.analizador.generar_reporte_completo(self.ciudad_actual, cultivo_elegido)
        
        if reporte:
            imprimir_reporte(reporte)
            
            # Ofrecer visualizaciones
            print("\n" + "="*70)
            print("📈 VISUALIZACIONES DISPONIBLES")
            print("="*70)
            print("1. Gráfica de temperatura vs requisitos")
            print("2. Gráfica de precipitación")
            print("3. Ambas gráficas")
            print("4. No ver gráficas")
            
            opcion = input("\nSelecciona una opción (1-4): ").strip()
            
            if opcion == '1':
                self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo_elegido)
            elif opcion == '2':
                self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo_elegido)
            elif opcion == '3':
                self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo_elegido)
                self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo_elegido)
        else:
            print("❌ Error al generar el reporte")
        
        input("\nPresiona ENTER para continuar...")
    
    
    def menu_visualizaciones(self):
        """Menú de visualizaciones"""
        while True:
            print("\n" + "="*70)
            print("📈 GRÁFICAS Y VISUALIZACIONES")
            print("="*70 + "\n")
            
            print("1. 📊 Comparación de todos los cultivos")
            print("2. 🌡️  Temperatura vs cultivo específico")
            print("3. 🌧️  Precipitación para cultivo específico")
            print("4. 📅 Calendario de siembra anual")
            print("5. 🎯 Dashboard completo (todas las gráficas)")
            print("6. ⬅️  Volver al menú principal")
            
            opcion = input("\nSelecciona una opción (1-6): ").strip()
            
            if opcion == '1':
                print("\n⏳ Generando gráfica...")
                self.visualizador.comparacion_cultivos(self.ciudad_actual)
            
            elif opcion == '2':
                cultivo = input("\nCultivo (maiz/arroz/tomate/yuca/frijol/platano/cebolla/sandia): ").lower().strip()
                if cultivo in cultivos_panama:
                    print("\n⏳ Generando gráfica...")
                    self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo)
                else:
                    print("❌ Cultivo no válido")
                    input("\nPresiona ENTER para continuar...")
            
            elif opcion == '3':
                cultivo = input("\nCultivo (maiz/arroz/tomate/yuca/frijol/platano/cebolla/sandia): ").lower().strip()
                if cultivo in cultivos_panama:
                    print("\n⏳ Generando gráfica...")
                    self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo)
                else:
                    print("❌ Cultivo no válido")
                    input("\nPresiona ENTER para continuar...")
            
            elif opcion == '4':
                print("\n⏳ Generando calendario...")
                self.visualizador.calendario_siembra()
            
            elif opcion == '5':
                cultivo = input("\nCultivo para dashboard (maiz/arroz/tomate/yuca/frijol/platano/cebolla/sandia): ").lower().strip()
                if cultivo in cultivos_panama:
                    self.visualizador.dashboard_completo(self.ciudad_actual, cultivo)
                else:
                    print("❌ Cultivo no válido")
                    input("\nPresiona ENTER para continuar...")
            
            elif opcion == '6':
                break
            
            else:
                print("❌ Opción no válida")
                input("\nPresiona ENTER para continuar...")
    
    
    def ver_calendario(self):
        """Muestra el calendario de siembra"""
        print("\n⏳ Generando calendario de siembra...")
        self.visualizador.calendario_siembra()
        input("\nPresiona ENTER para continuar...")
    
    
    def cambiar_ciudad(self):
        """Cambia la ciudad actual"""
        print("\n" + "="*70)
        print("⚙️  CAMBIAR CIUDAD")
        print("="*70 + "\n")
        
        print("Ciudades comunes en Panamá:")
        print("  • Panama City")
        print("  • David")
        print("  • Chitré")
        print("  • Santiago")
        print("  • Colón")
        
        nueva_ciudad = input("\nEscribe el nombre de la ciudad: ").strip()
        
        if nueva_ciudad:
            # Verificar si la ciudad existe
            print(f"\n⏳ Verificando {nueva_ciudad}...")
            clima = self.clima_api.obtener_clima_actual(nueva_ciudad)
            
            if clima:
                self.ciudad_actual = nueva_ciudad
                print(f"\n✅ Ciudad cambiada a: {clima['ciudad']}, {clima['pais']}")
            else:
                print(f"\n❌ No se pudo encontrar la ciudad '{nueva_ciudad}'")
                print("Manteniendo ciudad actual...")
        
        input("\nPresiona ENTER para continuar...")
    
    
    def ejecutar(self):
        """Ejecuta la aplicación principal"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_banner()
            self.menu_principal()
            
            opcion = input("\nSelecciona una opción (1-7): ").strip()
            
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
                print("\n" + "="*70)
                print("👋 ¡Gracias por usar el Asistente Agrícola!")
                print("="*70 + "\n")
                sys.exit(0)
            
            else:
                print("\n❌ Opción no válida")
                input("\nPresiona ENTER para continuar...")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    try:
        app = AsistenteAgricola()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Aplicación cerrada por el usuario")
        print("="*70 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, verifica tu conexión a internet y tu API key")
        sys.exit(1)