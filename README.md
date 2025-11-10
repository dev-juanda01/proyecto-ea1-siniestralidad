# Proyecto (EA1): Ingeniería de Datos para Siniestralidad Vial

Este repositorio contiene el desarrollo del Proyecto Integrado (EA1), enfocado en la formulación de una necesidad de ingeniería de datos y su materialización en una base de datos local (SQLite).

## 1. Problema y Caso de Uso

* **Para quién:** La Oficina de Planeación de la Secretaría de Movilidad de una alcaldía o gobernación en Colombia.
* **Necesidad:** La secretaría necesita priorizar sus recursos (limitados) para la intervención de infraestructura vial (instalación de señalización, reductores de velocidad, cámaras) con el objetivo de reducir la mortalidad en las vías.
* **Por qué requiere analítica:** Se requiere una **base de datos local (SQLite)** que centralice los "Sectores Críticos" identificados. Esto permitirá a los analistas ejecutar consultas rápidas para filtrar los puntos por `Municipio` o `Departamento` y, lo más importante, **generar reportes priorizados (CSV)** de los sectores con mayor número de `Fallecidos`, justificando así la asignación de recursos basada en evidencia.

## 2. Objetivo del Proyecto

Desarrollar una solución de ingeniería de datos local, utilizando SQLite y Python, que centralice el dataset de "Sectores Críticos de Siniestralidad Vial" para facilitar la consulta, el análisis y la generación de reportes priorizados, apoyando así la toma de decisiones basada en evidencia de las entidades de movilidad.

## 3. Estructura del Repositorio

El proyecto está organizado de la siguiente manera:

```

.
├── data/
│   └── SECTORES\_CRITICOS\_DE\_SINIESTRALIDAD\_VIAL\_20251109.csv  (Dataset Original)
│
├── db/
│   ├── proyecto.db     (Base de datos SQLite generada)
│   └── export.csv      (Reporte CSV Top 20 Sectores Críticos)
│
├── docs/
│   └── (Imágenes o soportes adicionales, ej. Diagrama de Gantt)
│
├── src\_datos.py    (Script de Python para crear la BD y el CSV)
│
└── README.md           (Este archivo)

````

## 4. Flujo de Datos y Ejecución

Este proyecto demuestra un flujo de ingeniería de datos (ETL) local:

1.  **Dataset Original (CSV):** El archivo fuente (`data/SECTORES...csv`) contiene 316 registros de puntos críticos.
2.  **Base de Datos (SQLite):** El script `proceso_datos.py` lee el CSV, lo limpia y lo carga en una base de datos SQLite estructurada (`db/proyecto.db`) en la tabla `sectores_criticos`.
3.  **Producto de Datos (CSV):** El script luego consulta la base de datos (`proyecto.db`) para extraer los 20 sectores más críticos (ordenados por número de `Fallecidos`) y exporta este análisis a `db/export.csv`.

### Cómo replicar el proyecto

Si deseas regenerar los artefactos de la base de datos, puedes (después de instalar Python y Pandas):

```bash
# 1. (Opcional) Elimina los archivos generados anteriormente
rm db/proyecto.db
rm db/export.csv

# 2. Ejecuta el script de ingeniería
python proceso_datos.py
````

Esto volverá a crear los archivos `proyecto.db` y `export.csv` en el directorio `db/`.

## 5\. Fuente de Datos y Licencia

  * **Dataset:** Sectores Críticos de Siniestralidad Vial (20251109).
  * **Autor (Probable):** Agencia Nacional de Seguridad Vial (ANSV) o Ministerio de Transporte de Colombia.
  * **Fuente (Probable):** [Portal de Datos Abiertos de Colombia (datos.gov.co)](https://www.datos.gov.co/)
  * **Licencia (Datos):** Licencia Abierta de Datos del Gobierno Colombiano.

-----

### Licencia del Proyecto

Este proyecto se distribuye bajo la **Licencia MIT**.