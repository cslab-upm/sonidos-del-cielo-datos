# Changelog
Los cambios que se produzcan en el proyecto se documentarán aquí.

## 2021-03-04
### Added
- Carpeta data con los datos originales del IMO
- Carpeta results con los resultados de ejecutar los scripts de Python
- imo_dates.py: genera un csv con todas las fechas y detecciones en esa fecha
- imo_graph.py: a partir del csv con las detecciones diarias del IMO genera un gráfico y lo guarda en png

## 2021-03-11
### Added
- sdc_dates.py: genera un csv con todas las fechas y detecciones en esa fecha de Sonidos del Cielo
- sdc_graph.py: igual que imo_graph.py pero para Sonidos del Cielo
- comparativa.py: genera un gráfico comparando resultados del IMO y SdC

## 2021-03-22
### Modified
- sdc_dates.py: utiliza el csv daily
- imo_dates.py: mejora en eficiencia mediante uso de la librería pandas

## 2021-04-11
### Added
- imo_dates_average.py: genera un csv con la media de meteoros detectados por estación cada día

## 2021-04-12
### Removed
- imo_graph.py
- sdc_graph.py
- comparativa.py
### Added
- graphs.py: funcionalidad de los programas que generaban gráficos condensada en un solo programa + implementación de POO y funciones

## 2021-04-24
### Modified
- Ahora los csvs con las detecciones diarias incluyen las fechas sin detecciones con un valor de 0.
- Representación por años