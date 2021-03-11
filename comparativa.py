# Código que representa en un gráfico las detecciones diarias de Sonidos del Cielo y las del IMO
# Es necesario haber obtenido anteriormente imo_meteorspd.csv y sdc_meteorspd.csv

from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import pandas as pd

# Lectura de datos con Pandas
# Datos Sonidos del Cielo
data_sdc = pd.read_csv('results\sdc_meteorspd.csv')
data_sdc['date'] = pd.to_datetime(data_sdc['date'])
data_sdc.sort_values('date', inplace=True) #ordena los datos por fecha
dates_sdc = data_sdc['date']
mets_sdc = data_sdc['meteors']
# Datos IMO
data_imo = pd.read_csv('results\imo_meteorspd.csv')
data_imo['Date'] = pd.to_datetime(data_imo['Date']) #convierte str a formato date
data_imo.sort_values('Date', inplace=True) #ordena los datos por fecha
dates_imo = data_imo['Date']
mets_imo = data_imo['Meteors']

# Características del gráfico
plt.style.use('ggplot') #estilo
plt.plot_date(dates_sdc, mets_sdc, linestyle='solid', marker='None', label = 'Sonidos del Cielo')
plt.plot_date(dates_imo, mets_imo, linestyle='solid', marker='None', label = 'IMO')
plt.gcf().set_size_inches(17, 8) #tamaño de la figura

# Formateo de las fechas
plt.gcf().autofmt_xdate() #rota fechas para mejor visualización
date_format = mpl_dates.DateFormatter('%d/%m/%Y') #fechas en formato DD/MM/YYYY
plt.gca().xaxis.set_major_formatter(date_format)
plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator(interval=1)) #1 fecha al mes

# Etiquetas
plt.title("Detecciones diarias - Sonidos del Cielo vs IMO")
plt.xlabel("Fechas")
plt.ylabel("Nº meteoros")
# Leyenda
plt.legend() #Añade las labels indicadas en plot_date como leyenda

# Exportar png
plt.savefig('results\comparativa_detecciones_diarias.png', dpi = 75)