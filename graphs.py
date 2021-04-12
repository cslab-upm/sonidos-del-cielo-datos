from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import pandas as pd

class Csv_file:
    """general csv file"""
    def __init__(self, name, route = ''):
        if route[-1] != '\\':
            self.path = route + '\\' + name + '.csv'
        else:
            self.path = route + name + '.csv'

class Metspd_csv(Csv_file):
    """Daily meteor detection file"""
    def __init__(self, name, route = "results\csvs\\", mets_col_name = "meteors"):
        self.mets_col_name = mets_col_name
        self.path = route + name + '.csv'

def read_mets_data(csv):
    """reads data from daily mets detections csv and returns dates and mets series"""
    data = pd.read_csv(csv.path)
    data['date'] = pd.to_datetime(data['date']) #convierte str a formato date
    data.sort_values('date', inplace=True) #ordena los datos por fecha
    dates = data['date']
    mets = data[csv.mets_col_name]
    return dates, mets


def style_date_plot(x, y, style, label='', linestyle='solid', marker='None'):
    """styles date plot"""
    plt.style.use(style)
    plt.plot_date(x, y, linestyle=linestyle, marker=marker, label=label)
    plt.gcf().set_size_inches(17, 8) #tamaño de la figura
    # Formateo de las fechas
    plt.gcf().autofmt_xdate() #rota fechas para mejor visualización
    date_format = mpl_dates.DateFormatter('%d/%m/%Y') #fechas en formato DD/MM/YYYY
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator(interval=1)) #1 fecha al mes


def create_metspd_graph(csv, style = 'seaborn-deep'):
    """creates a graph with daily meteor detections"""
     # Lectura y acondicionamiento de datos con Pandas
    dates, mets = read_mets_data(csv)

    # Características del gráfico
    style_date_plot(dates,mets,style)
    
    # Etiquetas y exportar
    plt.xlabel("Fechas")
    plt.ylabel("Nº meteoros")

    if 'imo' in csv.path:
        plt.title("Detecciones diarias - IMO")
        plt.savefig('results\graphs\imo_gráfico_deteccionesdiarias.png', dpi = 75)
    else:
        plt.title("Detecciones diarias - Sonidos del Cielo")
        plt.savefig('results\graphs\sdc_gráfico_deteccionesdiarias.png', dpi = 75)


def create_comparative_graph(csv1, csv2, style = 'seaborn-deep', title='Detecciones diarias - Sonidos del Cielo vs IMO'):
    """creates a graph comparing daily meteor detections from two sources"""
    # Leer datos
    dates1, mets1 = read_mets_data(csv1)
    dates2, mets2 = read_mets_data(csv2)

    # Formateo del gráfico
    label1 = label2 = ''
    if 'imo' in csv1.path:
        label1='IMO'
        if 'sdc' in csv2.path:
            label2='Sonidos del Cielo'
    elif 'sdc' in csv1.path:
        label1='Sonidos del Cielo'
        if 'imo' in csv2.path:
            label2='IMO'

    style_date_plot(dates1, mets1, style, label=label1)
    style_date_plot(dates2, mets2, style, label=label2)
    plt.title(title)
    plt.xlabel("Fechas")
    plt.ylabel("Nº meteoros")
    plt.legend()
    
    plt.savefig('results\graphs\comparativa_detecciones_diarias.png', dpi = 75)



# Test - Sonidos del Cielo
# sdc = Metspd_csv(name='sdc_clear_daily')
# create_metspd_graph(sdc)

# Test - IMO
# imo = Metspd_csv(name='imo_meteors_average', mets_col_name='avg mets per station')
# create_metspd_graph(imo)

# Test - Comparativa SdC vs IMO
sdc = Metspd_csv(name='sdc_clear_daily')
imo = Metspd_csv(name='imo_meteors_average', mets_col_name='avg mets per station')
create_comparative_graph(sdc,imo)