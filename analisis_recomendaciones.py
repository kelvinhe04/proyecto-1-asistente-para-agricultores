# analisis_recomendaciones.py
"""
Sistema de análisis y recomendaciones para agricultores
Combina datos climáticos con requisitos de cultivos
"""

from base_datos_cultivos import cultivos_panama, cultivos_por_temporada
from conexion_clima import ClimaAPI
from datetime import datetime
import pandas as pd


class AnalizadorAgricola:
    """
    Analiza condiciones climáticas y genera recomendaciones para agricultores
    """
    
    def __init__(self):
        self.clima_api = ClimaAPI()
        self.mes_actual = datetime.now().strftime('%B').lower()
        
        # Traducir mes al español
        meses_es = {
            'january': 'enero', 'february': 'febrero', 'march': 'marzo',
            'april': 'abril', 'may': 'mayo', 'june': 'junio',
            'july': 'julio', 'august': 'agosto', 'september': 'septiembre',
            'october': 'octubre', 'november': 'noviembre', 'december': 'diciembre'
        }
        self.mes_actual = meses_es.get(self.mes_actual, self.mes_actual)
    
    
    def evaluar_condiciones_cultivo(self, cultivo, clima_actual):
        """
        Evalúa si las condiciones actuales son adecuadas para un cultivo
        
        Returns:
            dict: Evaluación con puntaje y alertas
        """
        datos_cultivo = cultivos_panama[cultivo]
        
        # Extraer valores climáticos
        temp_actual = clima_actual['temperatura']
        humedad_actual = clima_actual['humedad']
        
        # Inicializar evaluación
        evaluacion = {
            'cultivo': datos_cultivo['nombre'],
            'puntaje': 100,
            'nivel': 'EXCELENTE',
            'alertas': [],
            'recomendaciones': []
        }
        
        # Evaluar temperatura
        if temp_actual < datos_cultivo['temp_minima']:
            deficit = datos_cultivo['temp_minima'] - temp_actual
            evaluacion['puntaje'] -= deficit * 5
            evaluacion['alertas'].append(f"🌡️ Temperatura BAJA ({temp_actual}°C). Mínimo requerido: {datos_cultivo['temp_minima']}°C")
            evaluacion['recomendaciones'].append("Considerar protección térmica o esperar temperaturas más cálidas")
        
        elif temp_actual > datos_cultivo['temp_maxima']:
            exceso = temp_actual - datos_cultivo['temp_maxima']
            evaluacion['puntaje'] -= exceso * 3
            evaluacion['alertas'].append(f"🌡️ Temperatura ALTA ({temp_actual}°C). Máximo tolerable: {datos_cultivo['temp_maxima']}°C")
            evaluacion['recomendaciones'].append("Implementar sistemas de sombra o riego adicional")
        
        else:
            evaluacion['recomendaciones'].append(f"✓ Temperatura ideal ({temp_actual}°C)")
        
        # Evaluar humedad
        dif_humedad = abs(humedad_actual - datos_cultivo['humedad_optima'])
        if dif_humedad > 20:
            evaluacion['puntaje'] -= dif_humedad * 0.5
            if humedad_actual < datos_cultivo['humedad_optima']:
                evaluacion['alertas'].append(f"💧 Humedad BAJA ({humedad_actual}%). Óptimo: {datos_cultivo['humedad_optima']}%")
                evaluacion['recomendaciones'].append("Aumentar frecuencia de riego")
            else:
                evaluacion['alertas'].append(f"💧 Humedad ALTA ({humedad_actual}%). Óptimo: {datos_cultivo['humedad_optima']}%")
                evaluacion['recomendaciones'].append("Mejorar drenaje, riesgo de hongos")
        
        # Evaluar temporada de siembra
        if self.mes_actual in [m.lower() for m in datos_cultivo['temporada_siembra']] or 'todo el año' in datos_cultivo['temporada_siembra']:
            evaluacion['recomendaciones'].append(f"✓ Mes ideal para siembra ({self.mes_actual.capitalize()})")
        else:
            evaluacion['puntaje'] -= 15
            meses = ', '.join(datos_cultivo['temporada_siembra'])
            evaluacion['alertas'].append(f"📅 Fuera de temporada. Mejor sembrar en: {meses}")
        
        # Determinar nivel según puntaje
        if evaluacion['puntaje'] >= 80:
            evaluacion['nivel'] = 'EXCELENTE'
            evaluacion['color'] = '🟢'
        elif evaluacion['puntaje'] >= 60:
            evaluacion['nivel'] = 'BUENO'
            evaluacion['color'] = '🟡'
        elif evaluacion['puntaje'] >= 40:
            evaluacion['nivel'] = 'REGULAR'
            evaluacion['color'] = '🟠'
        else:
            evaluacion['nivel'] = 'MALO'
            evaluacion['color'] = '🔴'
        
        evaluacion['puntaje'] = max(0, round(evaluacion['puntaje'], 1))
        
        return evaluacion
    
    
    def analizar_riesgos_pronostico(self, pronostico_df, cultivo):
        """
        Analiza el pronóstico y detecta riesgos climáticos
        """
        datos_cultivo = cultivos_panama[cultivo]
        riesgos = []
        
        # Analizar lluvia excesiva
        lluvia_total = pronostico_df['lluvia_3h'].sum()
        if lluvia_total > 50:
            if datos_cultivo['tolerancia_lluvia'] == 'baja':
                riesgos.append({
                    'nivel': 'ALTO',
                    'tipo': 'Lluvia excesiva',
                    'descripcion': f'Se esperan {lluvia_total:.1f}mm de lluvia. {datos_cultivo["nombre"]} tiene baja tolerancia.',
                    'accion': 'Mejorar drenaje, posponer siembra o considerar otro cultivo'
                })
            elif datos_cultivo['tolerancia_lluvia'] == 'media':
                riesgos.append({
                    'nivel': 'MEDIO',
                    'tipo': 'Lluvia considerable',
                    'descripcion': f'Se esperan {lluvia_total:.1f}mm de lluvia.',
                    'accion': 'Monitorear drenaje y preparar medidas preventivas'
                })
        
        # Analizar sequía
        dias_sin_lluvia = (pronostico_df['lluvia_3h'] == 0).sum() / 8  # Aproximado
        if dias_sin_lluvia > 3:
            if datos_cultivo['tolerancia_sequia'] == 'baja':
                riesgos.append({
                    'nivel': 'ALTO',
                    'tipo': 'Sequía prolongada',
                    'descripcion': f'Aproximadamente {int(dias_sin_lluvia)} días sin lluvia esperados.',
                    'accion': 'Implementar sistema de riego constante'
                })
        
        # Analizar temperaturas extremas
        temp_max = pronostico_df['temp_maxima'].max()
        temp_min = pronostico_df['temp_minima'].min()
        
        if temp_max > datos_cultivo['temp_maxima']:
            riesgos.append({
                'nivel': 'MEDIO',
                'tipo': 'Calor extremo',
                'descripcion': f'Temperaturas hasta {temp_max}°C (máx tolerable: {datos_cultivo["temp_maxima"]}°C)',
                'accion': 'Aumentar riego, considerar mallas de sombra'
            })
        
        if temp_min < datos_cultivo['temp_minima']:
            riesgos.append({
                'nivel': 'MEDIO',
                'tipo': 'Temperatura baja',
                'descripcion': f'Temperaturas hasta {temp_min}°C (mín requerida: {datos_cultivo["temp_minima"]}°C)',
                'accion': 'Considerar protección o retrasar siembra'
            })
        
        return riesgos
    
    
    def recomendar_cultivos(self, ciudad):
        """
        Recomienda los mejores cultivos para sembrar ahora
        """
        clima_actual = self.clima_api.obtener_clima_actual(ciudad)
        
        if not clima_actual:
            return None
        
        # Evaluar todos los cultivos
        evaluaciones = []
        
        for cultivo in cultivos_panama.keys():
            eval_cultivo = self.evaluar_condiciones_cultivo(cultivo, clima_actual)
            evaluaciones.append(eval_cultivo)
        
        # Ordenar por puntaje
        evaluaciones.sort(key=lambda x: x['puntaje'], reverse=True)
        
        return {
            'ciudad': clima_actual['ciudad'],
            'fecha': clima_actual['fecha_hora'],
            'clima_actual': clima_actual,
            'evaluaciones': evaluaciones
        }
    
    
    def generar_reporte_completo(self, ciudad, cultivo):
        """
        Genera un reporte completo para un cultivo específico
        """
        # Obtener datos
        clima_actual = self.clima_api.obtener_clima_actual(ciudad)
        pronostico = self.clima_api.obtener_pronostico_5dias(ciudad)
        
        if not clima_actual or pronostico is None:
            return None
        
        # Evaluar condiciones actuales
        evaluacion = self.evaluar_condiciones_cultivo(cultivo, clima_actual)
        
        # Analizar riesgos
        riesgos = self.analizar_riesgos_pronostico(pronostico, cultivo)
        
        # Preparar reporte
        reporte = {
            'cultivo': cultivos_panama[cultivo]['nombre'],
            'ubicacion': f"{clima_actual['ciudad']}, {clima_actual['pais']}",
            'fecha': clima_actual['fecha_hora'],
            'clima_actual': clima_actual,
            'evaluacion': evaluacion,
            'riesgos': riesgos,
            'pronostico_resumen': self.clima_api.obtener_resumen_diario(ciudad)
        }
        
        return reporte


def imprimir_reporte(reporte):
    """
    Imprime un reporte de forma legible
    """
    if not reporte:
        print("Error: No se pudo generar el reporte")
        return
    
    print("="*70)
    print(f"REPORTE AGRÍCOLA - {reporte['cultivo'].upper()}")
    print("="*70)
    print(f"Ubicación: {reporte['ubicacion']}")
    print(f"Fecha: {reporte['fecha']}")
    print()
    
    # Clima actual
    print("📊 CLIMA ACTUAL:")
    clima = reporte['clima_actual']
    print(f"  Temperatura: {clima['temperatura']}°C (sensación: {clima['sensacion_termica']}°C)")
    print(f"  Humedad: {clima['humedad']}%")
    print(f"  Descripción: {clima['descripcion']}")
    print()
    
    # Evaluación
    eval = reporte['evaluacion']
    print(f"📈 EVALUACIÓN: {eval['color']} {eval['nivel']} (Puntaje: {eval['puntaje']}/100)")
    print()
    
    if eval['alertas']:
        print("⚠️  ALERTAS:")
        for alerta in eval['alertas']:
            print(f"  • {alerta}")
        print()
    
    print("💡 RECOMENDACIONES:")
    for rec in eval['recomendaciones']:
        print(f"  • {rec}")
    print()
    
    # Riesgos
    if reporte['riesgos']:
        print("🚨 RIESGOS IDENTIFICADOS:")
        for riesgo in reporte['riesgos']:
            print(f"  [{riesgo['nivel']}] {riesgo['tipo']}")
            print(f"      {riesgo['descripcion']}")
            print(f"      → {riesgo['accion']}")
        print()
    
    # Pronóstico
    print("📅 PRONÓSTICO 5 DÍAS:")
    print(reporte['pronostico_resumen'])
    print()
    print("="*70)


# Ejemplo de uso
if __name__ == "__main__":
    analizador = AnalizadorAgricola()
    
    # Ejemplo 1: Reporte completo para maíz
    print("Generando reporte para MAÍZ en Ciudad de Panamá...\n")
    reporte = analizador.generar_reporte_completo("Panama City", "maiz")
    imprimir_reporte(reporte)
    
    print("\n\n")
    
    # Ejemplo 2: Recomendar mejores cultivos
    print("="*70)
    print("MEJORES CULTIVOS PARA SEMBRAR AHORA")
    print("="*70)
    recomendaciones = analizador.recomendar_cultivos("Panama City")
    
    if recomendaciones:
        print(f"Ubicación: {recomendaciones['ciudad']}")
        print(f"Fecha: {recomendaciones['fecha']}\n")
        
        print("TOP 5 CULTIVOS RECOMENDADOS:\n")
        for i, eval in enumerate(recomendaciones['evaluaciones'][:5], 1):
            print(f"{i}. {eval['color']} {eval['cultivo']} - {eval['nivel']} ({eval['puntaje']}/100)")
            if eval['alertas']:
                print(f"   Alertas: {len(eval['alertas'])}")