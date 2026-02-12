# 5.2 Ejercicio de programación 2 y análisis estático

Este proyecto tiene como objetivo calcular las ventas totales a partir de un catálogo de precios y un registro de ventas. Se implementa en Python y utiliza análisis de calidad de código con herramientas como Pylint y Flake8. 

Este trabajo se realiza como parte de la actividad **5.2 Ejercicio de programación 2 y análisis estático**, de la asignatura **Pruebas de software y aseguramiento de la calidad**.

## Descripción del Proyecto

- **`compute_sales.py`**: Este script lee un catálogo de precios y un registro de ventas desde archivos JSON, calcula el costo total de todas las ventas y genera un informe detallado. Incluye manejo de errores para operaciones de archivo y validación de datos.

### Funcionalidades
  - Carga y analiza archivos JSON para el catálogo y los registros de ventas.
  - Crea un mapeo de precios a partir del catálogo.
  - Calcula el costo total de las ventas basado en los registros de ventas y el mapeo de precios.
  - Formatea el informe de salida con detalles de cada venta y el costo total.

### Ejemplo de Uso
Para ejecutar el programa desde la línea de comandos:
```bash
python source/compute_sales.py priceCatalogue.json salesRecord.json
```

## Estructura del Proyecto
```
├── source/                                         # Código fuente de los ejercicios
│   └── compute_sales.py                           # Ejercicio 1. Compute sales
│
├── scripts/                                        # Scripts
│   └── generate_reports.sh                         # Script para generar reportes de calidad
│
├── tests/                                          # Casos de prueba organizados por ejercicio
│   ├── TC1/                                        # Primer caso de prueba
│   ├── TC2/                                        # Segundo caso de prueba
│   ├── TC3/                                        # Tercer caso de prueba
│   └── Results.txt                                 # Resultados de los casos de prueba
│
├── results/                                        # Resultados generados durante la ejecución
│   ├── console/                                    # Registros de salida en consola
│   │   ├── screenshots/                            # Capturas de pantalla de ejecución
│   │   └── output.txt                              # Salida completa de consola
│   ├── reports/                                    # Reportes de cumplimiento PEP8
│   │   ├── screenshots/                            # Capturas de pantalla de ejecución de reportes 
│   │   ├── compute_sales_pylint_report.txt         # Reporte pylint
│   │   └── compute_sales_flake8_report.txt         # Reporte flake8
│   └── SalesResults.txt                            # Resultados completos del Ejercicio 1
└── README.txt                                      # Documentación del proyecto
```

## Resultados y Registros
- Resultados agregados en `results/SalesResults.txt`.
- Salidas de consola y screenshots en `results/console/`.
- Reportes generados usando Pylint y Flake8 en `results/reports/`.

## Calidad de Código
El programa ha sido analizado con Pylint y Flake8. Los reportes se encuentran en `results/reports/`.

Para generar ambos reportes de forma automatizada, se ha creado el script `generate_reports.sh` en `scripts/`.

## Comandos Útiles
### Análisis de Calidad
#### Pylint
```bash
pylint source/compute_sales.py
```
#### Flake8
```bash
flake8 source/compute_sales.py
```
### Casos de Prueba
```bash
python source/compute_sales.py tests/TC1/TC1.ProductList.json tests/TC1/TC1.Sales.json
python source/compute_sales.py tests/TC1/TC1.ProductList.json tests/TC2/TC2.Sales.json
python source/compute_sales.py tests/TC1/TC1.ProductList.json tests/TC3/TC3.Sales.json
```