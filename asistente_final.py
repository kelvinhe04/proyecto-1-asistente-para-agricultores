# asistente_final.py
"""
SISTEMA ASISTENTE AGRICOLA - VERSION FINAL
Sistema completo con todas las funcionalidades integradas
Sin emojis, estructura clara y modular
"""

import os
import sys
from datetime import datetime

# Importar módulos del proyecto
from base_datos_cultivos import cultivos_panama, listar_cultivos
from conexion_clima import ClimaAPI
from analisis_simple import AnalizadorAgricola, mostrar_reporte_simple
from visualizaciones import VisualizadorAgricola
from historial import HistorialConsultas
from config import ConfiguracionSistema, ValidadorSistema


class AsistenteAgricola:
    """
    Sistema completo de asistente agricola para Panama
    Version final con historial y todas las funcionalidades
    """
    
    def __init__(self):
        print(ConfiguracionSistema.MENSAJES['inicio'])
        
        # Verificar sistema antes de iniciar
        diagnostico = ValidadorSistema.diagnostico_completo()
        if not diagnostico['sistema_funcionando']:
            print("ERROR: Sistema no esta configurado correctamente")
            print("Ejecute: python config.py para ver detalles")
            sys.exit(1)
        
        print("Cargando modulos...")
        
        self.clima_api = ClimaAPI()
        self.analizador = AnalizadorAgricola()
        self.visualizador = VisualizadorAgricola()
        self.historial = HistorialConsultas(ConfiguracionSistema.ARCHIVO_HISTORIAL)
        self.ciudad_actual = "Panama City"
        
        print(ConfiguracionSistema.MENSAJES['carga_exitosa'] + "\n")
    
    def limpiar_pantalla(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_header(self):
        """Muestra el encabezado del sistema"""
        info = ConfiguracionSistema.obtener_info_sistema()
        print("="*65)
        print(f"     {info['nombre']} v{info['version']}")
        print("="*65)
        print(f"Ciudad actual: {self.ciudad_actual}")
        print(f"Fecha y hora: {info['fecha_actual']}")
        print("="*65)
    
    def mostrar_menu_principal(self):
        """Muestra el menu principal del sistema"""
        print("\nMENU PRINCIPAL")
        print("-" * 35)
        print("1. Consultar clima actual")
        print("2. Ver recomendaciones de cultivos")
        print("3. Analizar cultivo especifico")
        print("4. Ver calendario de siembra")
        print("5. Generar graficas y reportes")
        print("6. Ver historial de consultas")
        print("7. Configuracion del sistema")
        print("8. Salir del sistema")
        print("-" * 35)
    
    def consultar_clima_actual(self):
        """Consulta y muestra informacion del clima actual"""
        print("\n" + "="*55)
        print("CONSULTA DE CLIMA ACTUAL")
        print("="*55)
        
        print(f"Obteniendo datos meteorologicos de {self.ciudad_actual}...")
        clima = self.clima_api.obtener_clima_actual(self.ciudad_actual)
        
        if clima:
            print(f"\nUbicacion: {clima['ciudad']}, {clima['pais']}")
            print(f"Actualizado: {clima['fecha_hora']}")
            print("-" * 45)
            print(f"Temperatura: {clima['temperatura']} grados Celsius")
            print(f"Sensacion termica: {clima['sensacion_termica']} grados Celsius")
            print(f"Humedad relativa: {clima['humedad']}%")
            print(f"Condicion climatica: {clima['descripcion'].title()}")
            print(f"Precipitacion (ultima hora): {clima['lluvia_1h']} mm")
            print(f"Velocidad del viento: {clima['velocidad_viento']} m/s")
            
            # Guardar consulta en historial
            self.historial.guardar_consulta(
                ciudad=self.ciudad_actual,
                temperatura=clima['temperatura'],
                humedad=clima['humedad'],
                tipo_consulta="consulta_clima"
            )
            
        else:
            print("\nError: No se pudo obtener informacion meteorologica")
            print("Verifique:")
            print("- Conexion a internet")
            print("- Nombre de la ciudad")
            print("- Configuracion de API key")
        
        self.pausar()
    
    def mostrar_recomendaciones_cultivos(self):
        """Genera y muestra recomendaciones de cultivos"""
        print("\n" + "="*55)
        print("RECOMENDACIONES DE CULTIVOS")
        print("="*55)
        
        print("Analizando condiciones climaticas actuales...")
        print("Evaluando cultivos disponibles...")
        
        recomendaciones = self.analizador.recomendar_cultivos(self.ciudad_actual)
        
        if recomendaciones:
            clima = recomendaciones['clima_actual']
            
            print(f"\nAnalisis completado para: {clima['ciudad']}")
            print(f"Condiciones actuales: {clima['temperatura']}C, {clima['humedad']}% humedad")
            print(f"Estado del tiempo: {clima['descripcion']}")
            
            print("\n" + "-"*55)
            print("RANKING DE CULTIVOS RECOMENDADOS")
            print("-"*55)
            
            # Mostrar top 5 cultivos
            for i, cultivo in enumerate(recomendaciones['evaluaciones'][:5], 1):
                print(f"\n{i}. {cultivo['cultivo'].upper()}")
                print(f"   Evaluacion: {cultivo['nivel']} ({cultivo['puntaje']}/100 puntos)")
                
                # Mostrar recomendaciones principales
                if cultivo['recomendaciones']:
                    print("   Recomendaciones:")
                    for rec in cultivo['recomendaciones'][:2]:
                        print(f"     - {rec}")
                
                # Mostrar alertas si las hay
                if cultivo['alertas']:
                    print(f"   ALERTAS ({len(cultivo['alertas'])}):")
                    for alerta in cultivo['alertas'][:2]:
                        print(f"     ! {alerta}")
            
            # Guardar consulta en historial
            mejor_cultivo = recomendaciones['evaluaciones'][0]
            self.historial.guardar_consulta(
                ciudad=self.ciudad_actual,
                cultivo=mejor_cultivo['cultivo'],
                temperatura=clima['temperatura'],
                humedad=clima['humedad'],
                puntaje=mejor_cultivo['puntaje'],
                nivel=mejor_cultivo['nivel'],
                tipo_consulta="recomendaciones_cultivos"
            )
            
        else:
            print("\nError al generar recomendaciones")
            print("Verifique la conexion y configuracion del sistema")
        
        self.pausar()
    
    def analizar_cultivo_especifico(self):
        """Realiza analisis detallado de un cultivo especifico"""
        print("\n" + "="*55)
        print("ANALISIS DETALLADO DE CULTIVO")
        print("="*55)
        
        # Mostrar cultivos disponibles
        print("\nCultivos disponibles en la base de datos:")
        cultivos = listar_cultivos()
        
        for i, cultivo in enumerate(cultivos, 1):
            nombre = cultivos_panama[cultivo]['nombre']
            temporada = ', '.join(cultivos_panama[cultivo]['temporada_siembra'])
            print(f"  {i}. {nombre} - Siembra: {temporada}")
        
        # Solicitar seleccion de cultivo
        print(f"\nCodigos de cultivos: {', '.join(cultivos)}")
        cultivo_elegido = input("\nIngrese el codigo del cultivo a analizar: ").lower().strip()
        
        if cultivo_elegido not in cultivos_panama:
            print(f"\nError: El cultivo '{cultivo_elegido}' no existe en la base de datos")
            print("Verifique el codigo ingresado")
            self.pausar()
            return
        
        nombre_cultivo = cultivos_panama[cultivo_elegido]['nombre']
        print(f"\nGenerando reporte completo para: {nombre_cultivo}")
        print("Analizando condiciones climaticas...")
        
        # Generar reporte detallado
        reporte = self.analizador.generar_reporte_completo(self.ciudad_actual, cultivo_elegido)
        
        if reporte:
            mostrar_reporte_simple(reporte)
            
            # Guardar en historial
            evaluacion = reporte['evaluacion']
            clima = reporte['clima_actual']
            
            self.historial.guardar_consulta(
                ciudad=self.ciudad_actual,
                cultivo=nombre_cultivo,
                temperatura=clima['temperatura'],
                humedad=clima['humedad'],
                puntaje=evaluacion['puntaje'],
                nivel=evaluacion['nivel'],
                tipo_consulta="analisis_cultivo_especifico"
            )
            
            # Ofrecer visualizaciones
            print("\n" + "="*55)
            print("OPCIONES DE VISUALIZACION")
            print("="*55)
            print("1. Grafica de temperatura vs requisitos del cultivo")
            print("2. Grafica de precipitacion")
            print("3. Ambas graficas")
            print("4. No generar graficas")
            
            opcion = input("\nSeleccione opcion de visualizacion (1-4): ").strip()
            
            if opcion == '1':
                print("\nGenerando grafica de temperatura...")
                self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo_elegido)
            elif opcion == '2':
                print("\nGenerando grafica de precipitacion...")
                self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo_elegido)
            elif opcion == '3':
                print("\nGenerando ambas graficas...")
                self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo_elegido)
                self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo_elegido)
            
        else:
            print("\nError al generar el reporte detallado")
            print("Verifique la conexion y configuracion")
        
        self.pausar()
    
    def mostrar_calendario_siembra(self):
        """Muestra el calendario anual de siembra"""
        print("\n" + "="*55)
        print("CALENDARIO ANUAL DE SIEMBRA")
        print("="*55)
        
        print("Generando calendario con todos los cultivos...")
        
        # Mostrar informacion textual primero
        print("\nRESUMEN POR TEMPORADAS:")
        print("-" * 30)
        
        temporadas = {
            'Seca (Dic-Mar)': [],
            'Lluviosa (May-Nov)': [],
            'Todo el año': []
        }
        
        for cultivo_key, datos in cultivos_panama.items():
            nombre = datos['nombre']
            temp_siembra = datos['temporada_siembra']
            
            if 'todo el año' in temp_siembra or len(temp_siembra) >= 6:
                temporadas['Todo el año'].append(nombre)
            elif any(mes in ['diciembre', 'enero', 'febrero', 'marzo'] for mes in temp_siembra):
                temporadas['Seca (Dic-Mar)'].append(nombre)
            else:
                temporadas['Lluviosa (May-Nov)'].append(nombre)
        
        for temporada, cultivos_temp in temporadas.items():
            if cultivos_temp:
                print(f"\n{temporada}:")
                for cultivo in cultivos_temp:
                    print(f"  - {cultivo}")
        
        # Generar grafica visual
        print(f"\nGenerando calendario visual...")
        self.visualizador.calendario_siembra()
        
        self.pausar()
    
    def menu_graficas_reportes(self):
        """Menu para generar diferentes tipos de graficas y reportes"""
        while True:
            print("\n" + "="*55)
            print("GRAFICAS Y REPORTES")
            print("="*55)
            
            print("\nOpciones disponibles:")
            print("1. Comparacion general de cultivos")
            print("2. Grafica temperatura vs cultivo especifico")
            print("3. Grafica de precipitacion para cultivo")
            print("4. Calendario visual de siembra")
            print("5. Dashboard completo para cultivo")
            print("6. Volver al menu principal")
            
            opcion = input("\nSeleccione una opcion (1-6): ").strip()
            
            if opcion == '1':
                print("\nGenerando comparacion de todos los cultivos...")
                self.visualizador.comparacion_cultivos(self.ciudad_actual)
                
            elif opcion == '2':
                cultivos = listar_cultivos()
                print(f"\nCultivos disponibles: {', '.join(cultivos)}")
                cultivo = input("Ingrese codigo del cultivo: ").lower().strip()
                
                if cultivo in cultivos_panama:
                    print(f"\nGenerando grafica de temperatura para {cultivo}...")
                    self.visualizador.grafica_temperatura_vs_cultivo(self.ciudad_actual, cultivo)
                else:
                    print("Codigo de cultivo no valido")
                
            elif opcion == '3':
                cultivos = listar_cultivos()
                print(f"\nCultivos disponibles: {', '.join(cultivos)}")
                cultivo = input("Ingrese codigo del cultivo: ").lower().strip()
                
                if cultivo in cultivos_panama:
                    print(f"\nGenerando grafica de precipitacion para {cultivo}...")
                    self.visualizador.grafica_precipitacion(self.ciudad_actual, cultivo)
                else:
                    print("Codigo de cultivo no valido")
                
            elif opcion == '4':
                print("\nGenerando calendario visual de siembra...")
                self.visualizador.calendario_siembra()
                
            elif opcion == '5':
                cultivos = listar_cultivos()
                print(f"\nCultivos disponibles: {', '.join(cultivos)}")
                cultivo = input("Ingrese codigo del cultivo para dashboard: ").lower().strip()
                
                if cultivo in cultivos_panama:
                    print(f"\nGenerando dashboard completo para {cultivo}...")
                    self.visualizador.dashboard_completo(self.ciudad_actual, cultivo)
                else:
                    print("Codigo de cultivo no valido")
                
            elif opcion == '6':
                break
                
            else:
                print("Opcion no valida")
            
            if opcion in ['1', '2', '3', '4', '5']:
                self.pausar()
    
    def menu_historial(self):
        """Menu para gestionar el historial de consultas"""
        while True:
            print("\n" + "="*55)
            print("HISTORIAL DE CONSULTAS")
            print("="*55)
            
            print("\nOpciones disponibles:")
            print("1. Ver ultimas consultas")
            print("2. Ver estadisticas del historial")
            print("3. Buscar consultas por cultivo")
            print("4. Limpiar historial completo")
            print("5. Volver al menu principal")
            
            opcion = input("\nSeleccione una opcion (1-5): ").strip()
            
            if opcion == '1':
                print("\n" + "-"*50)
                cantidad = input("Cuantas consultas mostrar (default 10): ").strip()
                try:
                    cantidad = int(cantidad) if cantidad else 10
                except ValueError:
                    cantidad = 10
                
                self.historial.mostrar_historial_simple(cantidad)
                
            elif opcion == '2':
                self.historial.mostrar_estadisticas()
                
            elif opcion == '3':
                cultivo_buscar = input("\nIngrese nombre o codigo del cultivo: ").lower().strip()
                consultas = self.historial.obtener_historial(100)  # Buscar en ultimas 100
                
                consultas_filtradas = [
                    c for c in consultas 
                    if cultivo_buscar in c.get('cultivo', '').lower()
                ]
                
                if consultas_filtradas:
                    print(f"\nEncontradas {len(consultas_filtradas)} consultas para '{cultivo_buscar}':")
                    for i, consulta in enumerate(consultas_filtradas, 1):
                        print(f"{i}. {consulta['fecha_hora']} - {consulta['cultivo']}")
                        if consulta['puntaje'] and consulta['puntaje'] != '0':
                            print(f"   Evaluacion: {consulta['puntaje']}/100")
                else:
                    print(f"No se encontraron consultas para '{cultivo_buscar}'")
                
            elif opcion == '4':
                print("\nADVERTENCIA: Esta accion eliminara todo el historial")
                self.historial.limpiar_historial()
                
            elif opcion == '5':
                break
                
            else:
                print("Opcion no valida")
            
            if opcion != '5':
                self.pausar()
    
    def menu_configuracion(self):
        """Menu de configuracion del sistema"""
        while True:
            print("\n" + "="*55)
            print("CONFIGURACION DEL SISTEMA")
            print("="*55)
            
            print(f"\nConfiguracion actual:")
            print(f"  Ciudad: {self.ciudad_actual}")
            
            print(f"\nOpciones:")
            print("1. Cambiar ciudad")
            print("2. Verificar conexion API clima")
            print("3. Ver informacion del sistema")
            print("4. Volver al menu principal")
            
            opcion = input("\nSeleccione una opcion (1-4): ").strip()
            
            if opcion == '1':
                self.cambiar_ciudad_sistema()
                
            elif opcion == '2':
                self.verificar_conexion_api()
                
            elif opcion == '3':
                self.mostrar_info_sistema()
                
            elif opcion == '4':
                break
                
            else:
                print("Opcion no valida")
            
            if opcion != '4':
                self.pausar()
    
    def cambiar_ciudad_sistema(self):
        """Permite cambiar la ciudad del sistema"""
        print("\n" + "-"*45)
        print("CAMBIO DE CIUDAD")
        print("-"*45)
        
        print(f"\nCiudad actual: {self.ciudad_actual}")
        
        print(f"\nCiudades principales de Panama:")
        ciudades_sugeridas = [
            "Panama City", "San Miguelito", "David", "Chitre", 
            "Santiago", "Colon", "Las Tablas", "Arraijan"
        ]
        
        for i, ciudad in enumerate(ciudades_sugeridas, 1):
            print(f"  {i}. {ciudad}")
        
        nueva_ciudad = input(f"\nIngrese nueva ciudad: ").strip()
        
        if nueva_ciudad:
            print(f"Verificando disponibilidad de datos para {nueva_ciudad}...")
            
            # Probar conexion con la nueva ciudad
            clima = self.clima_api.obtener_clima_actual(nueva_ciudad)
            
            if clima:
                self.ciudad_actual = nueva_ciudad
                print(f"\nCiudad actualizada exitosamente")
                print(f"Nueva ubicacion: {clima['ciudad']}, {clima['pais']}")
                print(f"Temperatura actual: {clima['temperatura']}C")
                print(f"Condiciones: {clima['descripcion']}")
            else:
                print(f"\nError: No se encontraron datos meteorologicos para '{nueva_ciudad}'")
                print("Verifique el nombre de la ciudad e intente nuevamente")
                print("La ciudad actual se mantiene sin cambios")
        else:
            print("Operacion cancelada")
    
    def verificar_conexion_api(self):
        """Verifica la conexion con la API del clima"""
        print("\n" + "-"*45)
        print("VERIFICACION DE CONEXION API")
        print("-"*45)
        
        print("Verificando conexion con OpenWeatherMap API...")
        
        # Probar con ciudad conocida
        clima = self.clima_api.obtener_clima_actual("Panama City")
        
        if clima:
            print("CONEXION EXITOSA")
            print(f"- API Key: Configurada correctamente")
            print(f"- Servidor: Respondiendo normalmente")
            print(f"- Datos obtenidos: {clima['ciudad']}, {clima['pais']}")
            print(f"- Temperatura: {clima['temperatura']}C")
        else:
            print("ERROR DE CONEXION")
            print("- Verifique su conexion a internet")
            print("- Verifique la API Key en el archivo .env")
            print("- Contacte soporte si el problema persiste")
    
    def mostrar_info_sistema(self):
        """Muestra informacion general del sistema"""
        print("\n" + "-"*45)
        print("INFORMACION DEL SISTEMA")
        print("-"*45)
        
        info = ConfiguracionSistema.obtener_info_sistema()
        
        print(f"\n{info['nombre']} v{info['version']}")
        print(f"Desarrollado para agricultores de Panama")
        print(f"Fecha version: {info['fecha_version']}")
        print(f"")
        print(f"Modulos cargados:")
        print(f"  - Base de datos: {len(cultivos_panama)} cultivos")
        print(f"  - API Climatica: OpenWeatherMap")
        print(f"  - Visualizaciones: matplotlib")
        print(f"  - Historial: CSV local")
        print(f"")
        print(f"Configuracion actual:")
        print(f"  - Ciudad: {self.ciudad_actual}")
        print(f"  - Fecha: {info['fecha_actual']}")
        print(f"  - Mes actual: {info['mes']}")
        print(f"  - Ciudades disponibles: {info['ciudades_disponibles']}")
        
        # Estadisticas del historial
        stats = self.historial.obtener_estadisticas()
        print(f"  - Total consultas: {stats['total_consultas']}")
        
        # Mostrar diagnostico rapido
        print(f"\nDiagnostico del sistema:")
        diagnostico = ValidadorSistema.diagnostico_completo()
        if diagnostico['sistema_funcionando']:
            print("  - Estado: FUNCIONANDO CORRECTAMENTE")
        else:
            print("  - Estado: PROBLEMAS DETECTADOS")
    
    def pausar(self):
        """Pausa la ejecucion esperando input del usuario"""
        input("\nPresione ENTER para continuar...")
    
    def ejecutar_sistema(self):
        """Ejecuta el bucle principal del sistema"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_header()
            self.mostrar_menu_principal()
            
            opcion = input("\nSeleccione una opcion (1-8): ").strip()
            
            if opcion == '1':
                self.consultar_clima_actual()
                
            elif opcion == '2':
                self.mostrar_recomendaciones_cultivos()
                
            elif opcion == '3':
                self.analizar_cultivo_especifico()
                
            elif opcion == '4':
                self.mostrar_calendario_siembra()
                
            elif opcion == '5':
                self.menu_graficas_reportes()
                
            elif opcion == '6':
                self.menu_historial()
                
            elif opcion == '7':
                self.menu_configuracion()
                
            elif opcion == '8':
                self.salir_del_sistema()
                
            else:
                print("\nOpcion no valida. Seleccione un numero del 1 al 8")
                self.pausar()
    
    def salir_del_sistema(self):
        """Sale del sistema de forma controlada"""
        print("\n" + "="*55)
        print("CERRANDO SISTEMA ASISTENTE AGRICOLA")
        print("="*55)
        
        # Mostrar estadisticas finales
        stats = self.historial.obtener_estadisticas()
        print(f"\nEstadisticas de la sesion:")
        print(f"- Total de consultas realizadas: {stats['total_consultas']}")
        
        if stats['cultivos_mas_consultados']:
            cultivo_top = stats['cultivos_mas_consultados'][0]
            print(f"- Cultivo mas consultado: {cultivo_top[0]} ({cultivo_top[1]} veces)")
        
        print(f"\nGracias por usar el Sistema Asistente Agricola")
        print(f"Desarrollado para apoyar la agricultura en Panama")
        print("\n" + "="*55)
        
        sys.exit(0)


def main():
    """Funcion principal del programa"""
    try:
        print("Cargando Sistema Asistente Agricola...")
        print("Por favor espere...")
        
        # Crear e inicializar el sistema
        asistente = AsistenteAgricola()
        
        # Ejecutar sistema principal
        asistente.ejecutar_sistema()
        
    except KeyboardInterrupt:
        print("\n\nSistema interrumpido por el usuario")
        print("Guardando datos...")
        print("Cerrando aplicacion de forma segura...")
        sys.exit(0)
        
    except Exception as error:
        print(f"\nError critico del sistema: {error}")
        print("\nPosibles soluciones:")
        print("1. Verifique su conexion a internet")
        print("2. Verifique el archivo .env con la API key")
        print("3. Reinstale las dependencias: pip install -r requirements.txt")
        print("4. Contacte soporte tecnico")
        
        input("\nPresione ENTER para cerrar...")
        sys.exit(1)


if __name__ == "__main__":
    main()