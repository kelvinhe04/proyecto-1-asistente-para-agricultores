# visualizaciones.py
"""
Sistema de visualizaciones para datos agrícolas
Genera gráficas informativas para agricultores
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from base_datos_cultivos import cultivos_panama
from conexion_clima import ClimaAPI
from analisis_recomendaciones import AnalizadorAgricola

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class VisualizadorAgricola:
    """
    Crea visualizaciones para análisis agrícola
    """
    
    def __init__(self):
        self.clima_api = ClimaAPI()
        self.analizador = AnalizadorAgricola()
        self.colores = {
            'temp': '#FF6B6B',
            'temp_optima': '#4ECDC4',
            'lluvia': '#45B7D1',
            'humedad': '#96CEB4'
        }
    
    
    def grafica_temperatura_vs_cultivo(self, ciudad, cultivo):
        """
        Gráfica que compara temperatura del pronóstico vs requisitos del cultivo
        """
        # Obtener datos
        pronostico = self.clima_api.obtener_pronostico_5dias(ciudad)
        datos_cultivo = cultivos_panama[cultivo]
        
        if pronostico is None:
            print("Error al obtener pronóstico")
            return
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Preparar datos
        fechas = pd.to_datetime(pronostico['fecha_hora'])
        temperaturas = pronostico['temperatura']
        
        # Graficar temperatura pronóstico
        ax.plot(fechas, temperaturas, 
                color=self.colores['temp'], 
                linewidth=2.5, 
                marker='o', 
                label='Temperatura Pronosticada',
                markersize=4)
        
        # Líneas de referencia del cultivo
        ax.axhline(y=datos_cultivo['temp_optima'], 
                   color=self.colores['temp_optima'], 
                   linestyle='--', 
                   linewidth=2,
                   label=f'Temperatura Óptima ({datos_cultivo["temp_optima"]}°C)')
        
        ax.axhline(y=datos_cultivo['temp_maxima'], 
                   color='red', 
                   linestyle=':', 
                   linewidth=1.5,
                   alpha=0.7,
                   label=f'Temperatura Máxima ({datos_cultivo["temp_maxima"]}°C)')
        
        ax.axhline(y=datos_cultivo['temp_minima'], 
                   color='blue', 
                   linestyle=':', 
                   linewidth=1.5,
                   alpha=0.7,
                   label=f'Temperatura Mínima ({datos_cultivo["temp_minima"]}°C)')
        
        # Zona óptima (área sombreada)
        ax.fill_between(fechas, 
                        datos_cultivo['temp_minima'], 
                        datos_cultivo['temp_maxima'],
                        alpha=0.2, 
                        color=self.colores['temp_optima'],
                        label='Rango Tolerable')
        
        # Formato
        ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperatura (°C)', fontsize=12, fontweight='bold')
        ax.set_title(f'Pronóstico de Temperatura vs Requisitos de {datos_cultivo["nombre"].upper()}\n{ciudad}', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    
    def grafica_precipitacion(self, ciudad, cultivo):
        """
        Gráfica de precipitación pronosticada
        """
        # Obtener datos
        pronostico = self.clima_api.obtener_pronostico_5dias(ciudad)
        datos_cultivo = cultivos_panama[cultivo]
        
        if pronostico is None:
            return
        
        # Agrupar por día
        pronostico['fecha'] = pd.to_datetime(pronostico['fecha_hora']).dt.date
        lluvia_diaria = pronostico.groupby('fecha')['lluvia_3h'].sum()
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Gráfica de barras
        fechas = range(len(lluvia_diaria))
        ax.bar(fechas, lluvia_diaria.values, 
               color=self.colores['lluvia'], 
               alpha=0.7,
               edgecolor='navy',
               label='Precipitación Diaria')
        
        # Línea de precipitación óptima mensual (dividida por 30)
        precip_optima_diaria = datos_cultivo['precipitacion_optima'] / 30
        ax.axhline(y=precip_optima_diaria, 
                   color='green', 
                   linestyle='--', 
                   linewidth=2,
                   label=f'Precipitación Óptima Diaria (~{precip_optima_diaria:.1f}mm)')
        
        # Formato
        ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
        ax.set_ylabel('Precipitación (mm)', fontsize=12, fontweight='bold')
        ax.set_title(f'Pronóstico de Precipitación para {datos_cultivo["nombre"].upper()}\n{ciudad}', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(fechas)
        ax.set_xticklabels([str(f) for f in lluvia_diaria.index], rotation=45, ha='right')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
    
    
    def calendario_siembra(self):
        """
        Calendario visual de siembras por mes
        """
        # Preparar datos
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        cultivos_lista = list(cultivos_panama.keys())
        matriz = np.zeros((len(cultivos_lista), 12))
        
        for i, cultivo in enumerate(cultivos_lista):
            temporadas = cultivos_panama[cultivo]['temporada_siembra']
            if 'todo el año' in temporadas:
                matriz[i, :] = 1
            else:
                meses_es = {
                    'enero': 0, 'febrero': 1, 'marzo': 2, 'abril': 3,
                    'mayo': 4, 'junio': 5, 'julio': 6, 'agosto': 7,
                    'septiembre': 8, 'octubre': 9, 'noviembre': 10, 'diciembre': 11
                }
                for temporada in temporadas:
                    mes_idx = meses_es.get(temporada.lower())
                    if mes_idx is not None:
                        matriz[i, mes_idx] = 1
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Mapa de calor
        im = ax.imshow(matriz, cmap='YlGn', aspect='auto', alpha=0.8)
        
        # Etiquetas
        ax.set_xticks(np.arange(12))
        ax.set_yticks(np.arange(len(cultivos_lista)))
        ax.set_xticklabels(meses, fontsize=11)
        ax.set_yticklabels([cultivos_panama[c]['nombre'] for c in cultivos_lista], 
                          fontsize=11)
        
        # Rotar etiquetas
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Agregar texto en celdas
        for i in range(len(cultivos_lista)):
            for j in range(12):
                if matriz[i, j] == 1:
                    text = ax.text(j, i, '✓', ha="center", va="center", 
                                 color="darkgreen", fontsize=16, fontweight='bold')
        
        ax.set_title('Calendario de Siembra - Panamá\n(✓ = Mes Recomendado)', 
                     fontsize=16, fontweight='bold', pad=20)
        
        # Línea vertical para mes actual
        mes_actual = datetime.now().month - 1
        ax.axvline(x=mes_actual, color='red', linestyle='--', linewidth=2, alpha=0.5)
        
        plt.tight_layout()
        plt.show()
    
    
    def comparacion_cultivos(self, ciudad):
        """
        Compara condiciones actuales con requisitos de todos los cultivos
        """
        recomendaciones = self.analizador.recomendar_cultivos(ciudad)
        
        if not recomendaciones:
            return
        
        # Preparar datos
        cultivos_nombres = [e['cultivo'] for e in recomendaciones['evaluaciones']]
        puntajes = [e['puntaje'] for e in recomendaciones['evaluaciones']]
        colores_barra = [e['color'] for e in recomendaciones['evaluaciones']]
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Gráfica de barras horizontal
        barras = ax.barh(cultivos_nombres, puntajes, color='skyblue', edgecolor='navy')
        
        # Colorear según nivel
        for i, (barra, puntaje) in enumerate(zip(barras, puntajes)):
            if puntaje >= 80:
                barra.set_color('#4CAF50')  # Verde
            elif puntaje >= 60:
                barra.set_color('#FFC107')  # Amarillo
            elif puntaje >= 40:
                barra.set_color('#FF9800')  # Naranja
            else:
                barra.set_color('#F44336')  # Rojo
        
        # Líneas de referencia
        ax.axvline(x=80, color='green', linestyle='--', alpha=0.5, linewidth=1.5, label='Excelente')
        ax.axvline(x=60, color='orange', linestyle='--', alpha=0.5, linewidth=1.5, label='Bueno')
        ax.axvline(x=40, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='Regular')
        
        # Agregar valores en barras
        for i, (nombre, puntaje) in enumerate(zip(cultivos_nombres, puntajes)):
            ax.text(puntaje + 2, i, f'{puntaje:.1f}', 
                   va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Puntaje de Idoneidad', fontsize=12, fontweight='bold')
        ax.set_title(f'Comparación de Cultivos - Condiciones Actuales\n{ciudad}', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 105)
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.show()
    
    
    def dashboard_completo(self, ciudad, cultivo):
        """
        Crea un dashboard con múltiples gráficas
        """
        print(f"\n{'='*70}")
        print(f"Generando Dashboard para {cultivo.upper()} en {ciudad}")
        print(f"{'='*70}\n")
        
        self.grafica_temperatura_vs_cultivo(ciudad, cultivo)
        self.grafica_precipitacion(ciudad, cultivo)
        self.comparacion_cultivos(ciudad)
        self.calendario_siembra()
        
        print(f"\n{'='*70}")
        print("✓ Dashboard completo generado exitosamente")
        print(f"{'='*70}\n")


# Ejemplo de uso
if __name__ == "__main__":
    visualizador = VisualizadorAgricola()
    
    # Opciones:
    print("Selecciona una opción:")
    print("1. Dashboard completo (todas las gráficas)")
    print("2. Calendario de siembra")
    print("3. Comparación de cultivos")
    print("4. Temperatura vs cultivo específico")
    
    opcion = input("\nOpción (1-4): ").strip()
    
    if opcion == "1":
        ciudad = input("Ciudad (por defecto: Panama City): ").strip() or "Panama City"
        cultivo = input("Cultivo (maiz/arroz/tomate/yuca/frijol/platano/cebolla/sandia): ").strip() or "maiz"
        visualizador.dashboard_completo(ciudad, cultivo)
    
    elif opcion == "2":
        visualizador.calendario_siembra()
    
    elif opcion == "3":
        ciudad = input("Ciudad (por defecto: Panama City): ").strip() or "Panama City"
        visualizador.comparacion_cultivos(ciudad)
    
    elif opcion == "4":
        ciudad = input("Ciudad (por defecto: Panama City): ").strip() or "Panama City"
        cultivo = input("Cultivo (maiz/arroz/tomate/yuca/frijol/platano/cebolla/sandia): ").strip() or "maiz"
        visualizador.grafica_temperatura_vs_cultivo(ciudad, cultivo)
    
    else:
        print("Opción no válida")