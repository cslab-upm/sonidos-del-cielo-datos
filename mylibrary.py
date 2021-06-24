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

def read_mets_data(csv, year):
    """reads data from daily mets detections csv and returns dates and mets series of the specified year"""
    data = pd.read_csv(csv.path)
    data['date'] = pd.to_datetime(data['date']) #convierte str a formato date
    data.sort_values('date', inplace=True) #ordena los datos por fecha
    if year != 'all times':
        start_date = year + '-01-01'
        end_date = year + '-12-31'
        after_start_date = data['date'] >= start_date
        before_end_date = data["date"] <= end_date
        between_two_dates = after_start_date & before_end_date
        df = data.loc[between_two_dates]
    else:
        df = data
    dates = df['date']
    mets = df[csv.mets_col_name]
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


def create_metspd_graph(csv, style = 'seaborn-deep', year='all times'):
    """creates a graph with daily meteor detections"""
    # Lectura y acondicionamiento de datos con Pandas
    dates, mets = read_mets_data(csv, year)

    # Características del gráfico
    style_date_plot(dates,mets,style)
    
    # Etiquetas y exportar
    plt.xlabel("Fechas")
    plt.ylabel("Nº meteoros")

    if 'imo' in csv.path:
        plt.title("Detecciones diarias - IMO - " + year)
        plt.savefig('results\graphs\imo_gráfico_deteccionesdiarias_' + year + '.png', dpi=75)
    else:
        plt.title("Detecciones diarias - Sonidos del Cielo - " + year)
        plt.savefig('results\graphs\sdc_gráfico_deteccionesdiarias_' + year + '.png', dpi=75)


def create_comparative_graph(csv1, csv2, style = 'seaborn-deep', title='Detecciones diarias - Sonidos del Cielo vs IMO', year='all times'):
    """creates a graph comparing daily meteor detections from two sources"""
    # Leer datos
    dates1, mets1 = read_mets_data(csv1, year)
    dates2, mets2 = read_mets_data(csv2, year)

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
    plt.title(title + ' - ' + year)
    plt.xlabel("Fechas")
    plt.ylabel("Nº meteoros")
    plt.legend()
    
    plt.savefig('results\graphs\comparativa_detecciones_diarias_' + year + '.png', dpi = 75)

def top_x_percent(csv, percentage, year):
    data = pd.read_csv(csv.path)

    start_date = year + '-01-01'
    end_date = year + '-12-31'

    after_start_date = data['date'] >= start_date
    before_end_date = data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date

    df = data.loc[between_two_dates]

    length = len(df.index)
    if 'meteors' in df.columns:
        print(df.nlargest(round((percentage*length)/100), ['meteors'])[['date','meteors']])
    elif 'avg mets per station' in df.columns:
        print(df.nlargest(round((percentage*length)/100), ['avg mets per station'])[['date','avg mets per station']])
    else:
        print("error")

def top_x_months(csv, months, year):
    data = pd.read_csv(csv.path)
    data['date'] = pd.to_datetime(data['date']) #convierte str a formato date
    data.sort_values('date', inplace=True) #ordena los datos por fecha

    start_date = year + '-01-01'
    end_date = year + '-12-31'

    after_start_date = data['date'] >= start_date
    before_end_date = data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date

    df = data.loc[between_two_dates]

    if 'meteors' in df.columns:
        print(df.nlargest(months, ['meteors'])[['date','meteors']])
    elif 'avg mets per station' in df.columns:
        print(df.nlargest(months, ['avg mets per station'])[['date','avg mets per station']])
    else:
        print("error")

def top_n_days_month(csv, n, year):
    data = pd.read_csv(csv.path)
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values('date', inplace=True) #ordena los datos por fecha

    start_date = year + '-01-01'
    end_date = year + '-12-31'

    after_start_date = data['date'] >= start_date
    before_end_date = data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date

    df = data.loc[between_two_dates]

    if 'meteors' in df.columns:
        df = df.sort_values('meteors').groupby(df['date'].dt.strftime('%B')).tail(n)
    elif 'avg mets per station' in df.columns:
        df = df.sort_values('avg mets per station').groupby(df['date'].dt.strftime('%B')).tail(n)
        df = df[['date','avg mets per station']]
    else:
        print('error')
        exit
    
    df.sort_values('date', inplace=True)
    df['date'] = df['date'].dt.strftime('%d %B')

    print(df)


def create_monthly_graph(csv, style = 'seaborn-deep', year='all times'):
    """Creates a graph with monthly meteor detections"""
    # Lectura y acondicionamiento de datos con Pandas
    dates, mets = read_mets_data(csv, year)

    # Características del gráfico
    style_date_plot(dates,mets,style)

    # Etiquetas y exportar
    plt.xlabel("Mes")
    plt.ylabel("Nº meteoros")

    if 'imo' in csv.path:
        plt.title("Detecciones mensuales - IMO - " + year)
        plt.savefig('results\graphs\imo_gráfico_deteccionesmensuales_' + year + '.png', dpi=75)
    else:
        plt.title("Detecciones mensuales - Sonidos del Cielo - " + year)
        plt.savefig('results\graphs\sdc_gráfico_deteccionesmensuales_' + year + '.png', dpi=75)

def create_hourly_month(csv, month,style = 'seaborn-deep'):
    """Creates a graph with mean meteor detections by hour in month"""

    # Open and read through data
    data = pd.read_csv(csv.path, sep=';', index_col='date')
    
    # Plot the data
    plt.plot(data.columns, data.loc[month])
    plt.xlabel("Hora")
    plt.ylabel("Nº meteoros")
    plt.title("Media de detecciones por hora Sonidos del Cielo - " + month)
    plt.savefig('results\graphs\sdc_horario_' + month[0:2] + '_' + month[3:] + '.png', dpi=75)