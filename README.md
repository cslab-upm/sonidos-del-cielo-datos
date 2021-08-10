# ANÁLISIS DE DATOS DE SONIDOS DEL CIELO
Contiene dos programas para analizar los datos del proyecto Sonidos del Cielo, uno para monitorización en directo de las detecciones de meteoros y otro para la elaboración anual de informes.

## Requisitos previos
* Python
* Módulo Matplotlib
* ...

## generador_informes.py
Herramienta diseñada con el objetivo de ser ejecutada periódicamente y obtener informes anuales sobre las detecciones de meteoros realizadas en el último año.
### Uso
1. Ejecutar analisis_datos.py
2. Introducir los datos requeridos:
* Año del informe
* Ruta en la que se desea que se guarde el informe
* Ruta del archivo daily de Sonidos del Cielo
* Ruta del archivo con los datos del IMO
* Ruta del archivo con el calendario de lluvias del año correspondiente
3. El informe obtenido es una estructura de carpetas con las imágenes resultantes de graficar los datos aportados.

## monitorizacion_live.py
Herramienta para la monitorización de las detecciones de meteoros realizadas en directo mientras el programa está en marcha.
El programa se conecta a una base de datos MySQL que se actualiza cada vez que se escucha un meteoro mediante un cliente MQTT.
Los resultados de esta monitorización se pueden observar en un dashboard dinámico hecho con Grafana en localhost:3000
Para poner en marcha el programa ejecutarlo y dejarlo en segundo plano.