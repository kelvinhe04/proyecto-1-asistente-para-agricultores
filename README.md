# Sistema Asistente Agricola de Panama

Sistema simplificado para ayudar a agricultores panameños con recomendaciones de cultivos basadas en condiciones climaticas actuales.

## Caracteristicas

- Consulta de clima en tiempo real
- Recomendaciones de cultivos segun condiciones actuales
- Analisis detallado de cultivos especificos
- Calendario de siembra anual
- Generacion de graficas y reportes
- Historial de consultas
- Interface simple sin elementos graficos complejos

## Archivos principales

### Sistema principal
- `asistente_final.py` - Sistema completo y principal (USAR ESTE)
- `sistema_agricola.py` - Version alternativa simplificada
- `main_simple.py` - Version basica del menu principal

### Modulos del sistema
- `base_datos_cultivos.py` - Base de datos de cultivos de Panama
- `conexion_clima.py` - Conexion con API de OpenWeatherMap
- `analisis_simple.py` - Analisis de condiciones climaticas (version sin emojis)
- `visualizaciones.py` - Generacion de graficas
- `historial.py` - Sistema de historial de consultas

### Datos
- `cultivos_panama.csv` - Datos basicos de cultivos
- `dataset_cultivos_panama.csv` - Dataset ampliado
- `.env` - Configuracion de API key

## Instalacion

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar API key de OpenWeatherMap en archivo .env:
```
OPENWEATHER_API_KEY=tu_api_key_aqui
```

## Uso

Ejecutar el sistema principal:
```bash
python asistente_final.py
```

### Menu principal

1. **Consultar clima actual** - Muestra temperatura, humedad, viento, etc.
2. **Ver recomendaciones de cultivos** - Ranking de mejores cultivos para condiciones actuales
3. **Analizar cultivo especifico** - Reporte detallado de un cultivo particular
4. **Ver calendario de siembra** - Calendario anual con temporadas de siembra
5. **Generar graficas y reportes** - Visualizaciones de datos
6. **Ver historial de consultas** - Historial de consultas anteriores
7. **Configuracion del sistema** - Cambiar ciudad, verificar conexiones
8. **Salir del sistema** - Cierra la aplicacion

## Cultivos incluidos

El sistema incluye informacion sobre:
- Maiz
- Arroz
- Tomate
- Yuca
- Frijol
- Platano
- Cebolla
- Sandia

Cada cultivo incluye:
- Temperatura optima
- Humedad requerida
- Temporada de siembra
- Tiempo de cosecha
- Plagas comunes
- Fertilizantes recomendados
- Tipo de suelo ideal

## Funciones principales

### Analisis climatico
- Obtiene datos meteorologicos en tiempo real
- Compara condiciones actuales con requisitos de cultivos
- Genera alertas si las condiciones no son optimas

### Sistema de recomendaciones
- Evalua todos los cultivos disponibles
- Asigna puntajes basados en condiciones actuales
- Ordena cultivos por idoneidad
- Genera recomendaciones practicas

### Historial de consultas
- Guarda todas las consultas en archivo CSV
- Permite revisar consultas anteriores
- Genera estadisticas de uso
- Identifica cultivos mas consultados

### Visualizaciones
- Graficas de temperatura vs requisitos de cultivos
- Graficas de precipitacion
- Calendario visual de siembra
- Comparacion entre cultivos
- Dashboard completo por cultivo

## Estructura de archivos

```
proyecto/
├── asistente_final.py          # Sistema principal
├── base_datos_cultivos.py      # Base de datos
├── conexion_clima.py           # API clima
├── analisis_simple.py          # Analisis (sin emojis)
├── visualizaciones.py          # Graficas
├── historial.py                # Historial consultas
├── cultivos_panama.csv         # Datos cultivos
├── dataset_cultivos_panama.csv # Dataset ampliado
├── requirements.txt            # Dependencias
├── .env                        # Configuracion API
└── README.md                   # Documentacion
```

## Dependencias

- pandas - Manejo de datos
- requests - Conexiones HTTP/API
- matplotlib - Graficas
- python-dotenv - Variables de entorno
- datetime - Manejo de fechas
- csv - Archivos CSV
- os, sys - Sistema operativo

## Notas de desarrollo

### Version simplificada
- Sin emojis en la interfaz
- Codigo modular y claro
- Funciones bien separadas
- Manejo de errores basico
- Interface de texto simple

### Mejoras futuras posibles
- Base de datos SQLite en lugar de CSV
- Mas tipos de graficas
- Predicciones meteorologicas
- Alertas automaticas
- Interface grafica con tkinter
- Integracion con mas APIs climaticas

## Solucion de problemas

### Error de conexion API
- Verificar conexion a internet
- Verificar API key en archivo .env
- Verificar nombre de ciudad

### Error al generar graficas
- Verificar instalacion de matplotlib
- Cerrar graficas anteriores antes de generar nuevas

### Archivos no encontrados
- Verificar que todos los archivos esten en el mismo directorio
- Verificar permisos de lectura/escritura

## Contacto

Sistema desarrollado para agricultores de Panama
Version 1.0 - Octubre 2025