# analisis_simple.py
"""
Sistema de análisis y recomendaciones simplificado
Version sin emojis y mas directa
"""

from base_datos_cultivos import cultivos_panama, cultivos_por_temporada
from conexion_clima import ClimaAPI
from datetime import datetime


class AnalizadorAgricola:
    """
    Analiza condiciones climaticas y genera recomendaciones para agricultores
    Version simplificada
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
        Evalua si las condiciones actuales son adecuadas para un cultivo
        
        Returns:
            dict: Evaluacion con puntaje y alertas
        """
        datos_cultivo = cultivos_panama[cultivo]
        
        # Extraer valores climaticos
        temp_actual = clima_actual['temperatura']
        humedad_actual = clima_actual['humedad']
        
        # Inicializar evaluacion
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
            evaluacion['alertas'].append(f"Temperatura BAJA ({temp_actual}C). Minimo requerido: {datos_cultivo['temp_minima']}C")
            evaluacion['recomendaciones'].append("Considerar proteccion termica o esperar temperaturas mas calidas")
        
        elif temp_actual > datos_cultivo['temp_maxima']:
            exceso = temp_actual - datos_cultivo['temp_maxima']
            evaluacion['puntaje'] -= exceso * 3
            evaluacion['alertas'].append(f"Temperatura ALTA ({temp_actual}C). Maximo tolerable: {datos_cultivo['temp_maxima']}C")
            evaluacion['recomendaciones'].append("Implementar sistemas de sombra o riego adicional")
        
        else:
            evaluacion['recomendaciones'].append(f"Temperatura ideal ({temp_actual}C)")
        
        # Evaluar humedad
        dif_humedad = abs(humedad_actual - datos_cultivo['humedad_optima'])
        if dif_humedad > 20:
            evaluacion['puntaje'] -= dif_humedad * 0.5
            if humedad_actual < datos_cultivo['humedad_optima']:
                evaluacion['alertas'].append(f"Humedad BAJA ({humedad_actual}%). Optimo: {datos_cultivo['humedad_optima']}%")
                evaluacion['recomendaciones'].append("Aumentar frecuencia de riego")
            else:
                evaluacion['alertas'].append(f"Humedad ALTA ({humedad_actual}%). Optimo: {datos_cultivo['humedad_optima']}%")
                evaluacion['recomendaciones'].append("Mejorar drenaje, riesgo de hongos")
        
        # Evaluar temporada de siembra
        if self.mes_actual in [m.lower() for m in datos_cultivo['temporada_siembra']] or 'todo el año' in datos_cultivo['temporada_siembra']:
            evaluacion['recomendaciones'].append(f"Mes ideal para siembra ({self.mes_actual.capitalize()})")
        else:
            evaluacion['puntaje'] -= 15
            meses = ', '.join(datos_cultivo['temporada_siembra'])
            evaluacion['alertas'].append(f"Fuera de temporada. Mejor sembrar en: {meses}")
        
        # Determinar nivel segun puntaje
        if evaluacion['puntaje'] >= 80:
            evaluacion['nivel'] = 'EXCELENTE'
        elif evaluacion['puntaje'] >= 60:
            evaluacion['nivel'] = 'BUENO'
        elif evaluacion['puntaje'] >= 40:
            evaluacion['nivel'] = 'REGULAR'
        else:
            evaluacion['nivel'] = 'MALO'
        
        # Asegurar que el puntaje no sea negativo
        evaluacion['puntaje'] = max(0, evaluacion['puntaje'])
        
        return evaluacion
    
    def recomendar_cultivos(self, ciudad):
        """
        Genera recomendaciones de cultivos basadas en el clima actual
        
        Args:
            ciudad (str): Nombre de la ciudad
            
        Returns:
            dict: Recomendaciones ordenadas por puntaje
        """
        # Obtener clima actual
        clima = self.clima_api.obtener_clima_actual(ciudad)
        
        if not clima:
            return None
        
        # Evaluar todos los cultivos
        evaluaciones = []
        
        for cultivo_key in cultivos_panama.keys():
            evaluacion = self.evaluar_condiciones_cultivo(cultivo_key, clima)
            evaluaciones.append(evaluacion)
        
        # Ordenar por puntaje (mejor primero)
        evaluaciones.sort(key=lambda x: x['puntaje'], reverse=True)
        
        return {
            'clima_actual': clima,
            'evaluaciones': evaluaciones,
            'fecha_analisis': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
    
    def generar_reporte_completo(self, ciudad, cultivo):
        """
        Genera un reporte completo para un cultivo especifico
        
        Args:
            ciudad (str): Nombre de la ciudad
            cultivo (str): Clave del cultivo
            
        Returns:
            dict: Reporte completo del cultivo
        """
        if cultivo not in cultivos_panama:
            return None
        
        # Obtener clima actual
        clima = self.clima_api.obtener_clima_actual(ciudad)
        
        if not clima:
            return None
        
        # Evaluar cultivo
        evaluacion = self.evaluar_condiciones_cultivo(cultivo, clima)
        
        # Obtener datos del cultivo
        datos_cultivo = cultivos_panama[cultivo]
        
        # Construir reporte
        reporte = {
            'cultivo': datos_cultivo,
            'clima_actual': clima,
            'evaluacion': evaluacion,
            'fecha_reporte': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'ciudad': ciudad
        }
        
        return reporte
    
    def obtener_cultivos_por_temporada(self):
        """
        Obtiene cultivos organizados por temporada
        
        Returns:
            dict: Cultivos agrupados por mes de siembra
        """
        return cultivos_por_temporada()


def mostrar_reporte_simple(reporte):
    """
    Muestra un reporte de cultivo de forma simple
    
    Args:
        reporte (dict): Reporte generado por generar_reporte_completo
    """
    print("="*60)
    print(f"REPORTE: {reporte['cultivo']['nombre'].upper()}")
    print("="*60)
    
    # Informacion basica
    info = reporte['cultivo']
    print(f"\nInformacion basica:")
    print(f"- Tiempo de cosecha: {info['tiempo_cosecha']}")
    print(f"- Temporada: {', '.join(info['temporada_siembra'])}")
    print(f"- Temperatura ideal: {info['temp_minima']}-{info['temp_maxima']} grados C")
    print(f"- Humedad ideal: {info['humedad_optima']}%")
    
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
    
    # Informacion adicional del cultivo
    print(f"\nInformacion adicional:")
    if 'plagas_comunes' in info:
        print(f"- Plagas comunes: {info['plagas_comunes']}")
    if 'fertilizante' in info:
        print(f"- Fertilizantes: {info['fertilizante']}")
    if 'suelo_ideal' in info:
        print(f"- Suelo ideal: {info['suelo_ideal']}")