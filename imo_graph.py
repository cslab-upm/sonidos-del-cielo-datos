from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import pandas as pd

# Lectura y acondicionamiento de datos con Pandas
data = pd.read_csv('results\imo_meteorspd.csv')
data['Date'] = pd.to_datetime(data['Date']) #convierte str a formato date
data.sort_values('Date', inplace=True) #ordena los datos por fecha
dates = data['Date']
mets = data['Meteors']

# Características del gráfico
plt.style.use('seaborn-deep') #estilo
plt.plot_date(dates, mets, linestyle='solid', marker='None')
plt.gcf().set_size_inches(17, 8) #tamaño de la figura

# Formateo de las fechas
plt.gcf().autofmt_xdate() #rota fechas para mejor visualización
date_format = mpl_dates.DateFormatter('%d/%m/%Y') #fechas en formato DD/MM/YYYY
plt.gca().xaxis.set_major_formatter(date_format)
plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator(interval=1)) #1 fecha al mes

# Etiquetas
plt.title("Detecciones diarias - IMO")
plt.xlabel("Fechas")
plt.ylabel("Nº meteoros")

# Exportar png
plt.savefig('results\imo_gráfico_deteccionesdiarias.png', dpi = 75)