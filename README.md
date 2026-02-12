# 5.2 Ejercicio de programación 2 y análisis estático

... como parte del ejercicio de la asignatura "Pruebas de software y aseguramiento de la calidad".

## Descripción

- `compute_sales.py`:

## Requisitos

- Python 3.7+

# Notas Importantes

- Se utiliza pylint y flake 8 para analisis de la calidad....
- 

## Uso

### Ejercicio 1. Compute sales
```bash
python source/compute_statistics.py priceCatalogue.json salesRecord.json
```

## Estructura del Proyecto
```
├── source/                                         # Código fuente de los ejercicios
│   └── compute_statistics.py                       # Ejercicio 1. Compute sales
│
├── scripts/                                        # Scripts
│   └── generate_reports.sh                         # Script para generar reportes de calidad
│
├── tests/                                          # Casos de prueba organizados por ejercicio
│   ├── P1/                                         # Primer caso de prueba
│   ├── P2/                                         # Segundo caso de prueba
│   └── P3/                                         # Tercer caso de prueba
│
├── results/                                        # Resultados generados durante la ejecución
│   │
│   ├── console/                                    # Registros de salida en consola
│   │   ├── screenshots/                            # Capturas de pantalla de ejecución
│   │   └── output.txt                              # Salida completa de consola
│   │
│   ├── reports/                                    # Reportes de cumplimiento PEP8
│   │   ├── compute_statistics_pylint_report.txt    # Reporte pylint
│   │   └── compute_statistics_flake8_report.txt    # Reporte flake8
│   │
│   └── SalesResults.txt                            # Resultados completos del Ejercicio 1
│
└── README.txt                                      # Documentación del proyecto
```

## Resultados y registros

- Resultados agregados:
  - `results/SalesResults.txt` (Ejercicio 1. Compute sales)

- Salidas de consola y screenshots de contola en `results/console/` por cada ejercicio.
- Reportes de usando Pylint y Flake8 en `results/reports/`.

## Calidad de Código

El programa ha sido analizados con PyLint y Flake8. Los reportes se encuentran en `results/reports/`.

Para generar ambos reportes de forma automatizada, en `scripts/` se generó el script generate_reports.sh para la generación de reportes automatizados usando dichas dos librerías.

## Comandos útiles

### Ejercicio 1. Compute sales

#### pylint
```bash
pylint source/compute_sales.py --output-format=text > results/reports/compute_sales_pylint_report.txt
```

#### flake8
```bash
flake8 source/compute_sales.py > results/reports/compute_sales_flake8_report.txt
```

#### Test Cases
```bash
python source/compute_sales.py tests/TC1/TC1.ProductList.json tests/TC1/TC1.Sales.json
python source/compute_sales.py tests/TC1/TC1.ProductList.json tests/TC2/TC2.Sales.json
python source/compute_sales.py tests/TC1/TC1.ProductList.json tests/TC3/TC3.Sales.json
```