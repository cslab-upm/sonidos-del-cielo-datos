"""Software tool to analyze data from Sonidos del Cielo / Contadores de Estrellas"""

import os
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import pandas as pd
import numpy as np

def get_user_input():
    """Asks the user for the necessesary information and returns it"""
    year = input('Year >>>')
    results_dir = input('Results path >>>')
    sdc_data_path = input('Daily path >>>')
    imo_data_path = input('IMO data path >>>')
    cal_path = input('Shower calendar path %s >>>' %year)
    return year, results_dir, sdc_data_path, imo_data_path, cal_path

def folder_structure(results_dir, year):
    """Changes working directory and creates the whole folders structure where the files are going to be saved"""
    os.chdir(results_dir)
    data_dir = results_dir + '\informe_' + year + '\datos'
    temp_dir = results_dir + '\informe_' + year + '\\temp'
    results_dir = results_dir + '\informe_' + year + '\\resultados'
    imo_res_path = results_dir + '\IMO'
    diario_path = results_dir + '\diario'
    lluvias_path = results_dir + '\lluvias'
    curvas_horarias_path = results_dir + '\curvas_horarias'
    os.makedirs(data_dir)
    os.makedirs(temp_dir)
    os.makedirs(imo_res_path)
    os.makedirs(diario_path)
    os.makedirs(lluvias_path)
    os.makedirs(curvas_horarias_path)
    return results_dir, data_dir, imo_res_path, diario_path, lluvias_path, curvas_horarias_path, temp_dir

def mod_sdc_daily(daily_path, results_dir, sh_cal = None):
    """Cleans the daily file and creates modified daily and temp files"""
    # Read csv and create dataframe
    df = pd.read_csv(daily_path, sep=';')
    # Datetime format and delete empty rows
    df['date'] = df['Date']
    for ind in df.index:
        date = df['date'][ind]
        # Skip empty rows
        if len(date) < 3:
            df.drop(ind, inplace=True)
            continue
        if date[8] == 't': #september exception
            day = date[11:13]
        else:
            day = date[10:12]
        # Modify date
        if day[1] == ' ':
            aux = day[0]
            day = '0' + aux
        month = date[5:8].lower()
        if month == 'ene':
            month = '01'
        elif month == 'feb':
            month = '02'
        elif month == 'mar':
            month = '03'
        elif month == 'abr':
            month = '04'
        elif month == 'may':
            month = '05'
        elif month == 'jun':
            month = '06'
        elif month == 'jul':
            month = '07'
        elif month == 'ago':
            month = '08'
        elif month == 'sep':
            month = '09'
        elif month == 'oct':
            month = '10'
        elif month == 'nov':
            month = '11'
        elif month == 'dic':
            month = '12'
        year = date[-4:]
        df['date'][ind] = ("%s-%s-%s" %(day, month, year))
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    # Modified dataframe
    columns = ['date','00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','total']
    df_mod = pd.DataFrame(columns=columns)
    df_mod['date'] = df['date'] # formato año-mes-día
    df_mod['00'] = df['Total'] - df['fakes']
    df_mod['01'] = df['Total.1'] - df['fakes.1']
    df_mod['02'] = df['Total.2'] - df['fakes.2']
    df_mod['03'] = df['Total.3'] - df['fakes.3']
    df_mod['04'] = df['Total.4'] - df['fakes.4']
    df_mod['05'] = df['Total.5'] - df['fakes.5']
    df_mod['06'] = df['Total.6'] - df['fakes.6']
    df_mod['07'] = df['Total.7'] - df['fakes.7']
    df_mod['08'] = df['Total.8'] - df['fakes.8']
    df_mod['09'] = df['Total.9'] - df['fakes.9']
    df_mod['10'] = df['Total.10'] - df['fakes.10']
    df_mod['11'] = df['Total.11'] - df['fakes.11']
    df_mod['12'] = df['Total.12'] - df['fakes.12']
    df_mod['13'] = df['Total.13'] - df['fakes.13']
    df_mod['14'] = df['Total.14'] - df['fakes.14']
    df_mod['15'] = df['Total.15'] - df['fakes.15']
    df_mod['16'] = df['Total.16'] - df['fakes.16']
    df_mod['17'] = df['Total.17'] - df['fakes.17']
    df_mod['18'] = df['Total.18'] - df['fakes.18']
    df_mod['19'] = df['Total.19'] - df['fakes.19']
    df_mod['20'] = df['Total.20'] - df['fakes.20']
    df_mod['21'] = df['Total.21'] - df['fakes.21']
    df_mod['22'] = df['Total.22'] - df['fakes.22']
    df_mod['23'] = df['Total.23'] - df['fakes.23']
    df_mod['total'] = df['Total.24'] - df['fakes.24']
    # Delete empty rows
    df_mod = df_mod.replace(0, np.NaN)
    # Monthly results
    df_month = df_mod
    df_month.index = pd.to_datetime(df_month['date'])
    df_month = df_month.groupby(pd.Grouper(freq='M')).mean()
    df_month.index = df_month.index.strftime('%m/%Y')
    df_month.to_csv(results_dir + '\..\\temp\sdc_mod_monthly.csv', sep=';')
    # Replace NaN with 0s
    df_mod = df_mod.fillna(0)
    # Export
    df_mod.to_csv(results_dir + '\sdc_mod_daily.csv', index=False, sep=';')
    # Showers
    # Read file
    cal = pd.read_csv(sh_cal, sep=';')
    cal = cal[['Maximo']]
    cal = pd.to_datetime(cal['Maximo'], format='%d/%m/%Y')
    # Create a list of showers
    showers = list()
    for date in cal:
        showers.append(date)
    # Filter daily to leave rows with shower max date
    filt = df_mod['date'].isin(showers)
    df_mod = df_mod.loc[filt]
    # Export
    df_mod.to_csv(results_dir + '\..\\temp\sdc_showers_daily.csv', index=False)

def graph_sdc_daily(results_dir, diario_path, year):
    """Creates the yearly graph with daily detections, comparing to prev year and with showers"""
    # Read data with Pandas
    data = pd.read_csv(results_dir + '\sdc_mod_daily.csv', sep=';')
    data['date'] = pd.to_datetime(data['date'])
    # Filter dates
    start_date = year + '-01-01'
    end_date = year + '-12-31'
    after_start_date = data['date'] >= start_date
    before_end_date = data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    data = data.loc[between_two_dates]
    dates = data['date']
    meteors = data['total']
    # Style plot
    plt.style.use('seaborn-deep')
    plt.plot_date(dates, meteors, linestyle='solid', marker='None')
    plt.gcf().set_size_inches(17, 8)
    plt.gcf().autofmt_xdate() #rotates dates
    date_format = mpl_dates.DateFormatter('%d/%m/%Y') #date format DD/MM/YYYY
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator(interval=1)) #1 day/month
    plt.xlabel('Fechas')
    plt.ylabel('Nº meteoros')
    plt.title('Detecciones diarias - Sonidos del Cielo - ' + year)
    plt.savefig(diario_path + '\SdC_' + year + '.png', dpi=75)
    # vs previous year
    # Read data
    data_prev = pd.read_csv(results_dir + '\sdc_mod_daily.csv', sep=';')
    data_prev['date'] = pd.to_datetime(data_prev['date'])
    data_prev.sort_values(by='date', inplace=True)
    # Filter dates
    yr = str(int(year) - 1)
    start_date = yr + '-01-01'
    end_date = yr + '-12-31'
    after_start_date = data_prev['date'] >= start_date
    before_end_date = data_prev["date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    data_prev = data_prev.loc[between_two_dates]
    # Plot
    dates_prev = pd.to_datetime(data_prev['date'])
    dates_prev.sort_values(inplace=True)
    dates_prev = dates_prev.dt.strftime('%d/%m')
    meteors_prev = data_prev['total']
    dates_yr = data['date'].dt.strftime('%d/%m')
    plt.clf()
    plt.style.use('seaborn-deep')
    plt.gcf().set_size_inches(17, 8)
    plt.gcf().autofmt_xdate() #rotates dates
    date_format = mpl_dates.DateFormatter('%d/%m') #date format DD/MM
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator(interval=1)) #1 day/month
    plt.xlabel('Fechas')
    plt.ylabel('Nº meteoros')
    plt.title('Detecciones diarias - Sonidos del Cielo - ' + year + ' vs ' + yr)
    plt.plot_date(dates_yr, meteors, linestyle='solid', marker='None')
    plt.plot_date(dates_prev, meteors_prev, linestyle='solid', marker='None')
    plt.savefig(diario_path + '\SdC_' + year + '_vs_' + yr + '.png', dpi=75)
    # Showers
    plt.clf()
    showers = pd.read_csv(results_dir + '\..\\temp\sdc_showers_daily.csv')
    showers['date'] = pd.to_datetime(showers['date'])
    dates_sh = showers['date']
    meteors_sh = showers['total']
    plt.style.use('seaborn-deep')
    plt.plot_date(dates, meteors, linestyle='solid', marker= 'None', label='')
    plt.plot_date(dates_sh, meteors_sh, linestyle='', marker= 'o', label='Max day of showers', color='r')
    plt.gcf().set_size_inches(17, 8)
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%d/%m/%Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator(interval=1))
    plt.xlabel("Fechas")
    plt.ylabel("Nº meteoros")
    plt.title("Detecciones diarias y lluvias - Sonidos del Cielo - " + year)
    plt.legend()
    plt.savefig(diario_path + '\SdC_' + year + '_lluvias.png', dpi=75)

def mod_imo_avg(imo_data_path, temp_path, sh_cal):
    """Gets simplified version of IMO data and gets daily meteors as the average of meteors per station"""
    # Read data with Pandas
    data = pd.read_csv(imo_data_path, sep=';')
    # Adjust dates column
    data['date'] = data['Start Date'] # rename
    data['date'] = pd.DatetimeIndex(data.date).normalize() # delete time
    data['date'] = pd.to_datetime(data['date']) # datetime format
    data.sort_values('date', inplace=True) # sort data by date
    # Count average meteor detections by station
    total_mets = data.groupby('date')['Number'].sum() # add daily meteors
    stations = data.groupby('date')['Obs Session ID'].nunique() # count number of different stations for each day
    # Reconfigure columns
    df = total_mets.to_frame().reset_index()
    df2 = stations.to_frame().reset_index()
    df['stations'] = df2['Obs Session ID']
    df['total meteors'] = df['Number']
    df['avg mets per station'] = df['total meteors'] / df['stations']
    df = df[['date','stations','total meteors','avg mets per station']]
    # Fill in missing dates with zeros
    ind = pd.date_range(min(df['date']), max(df['date']))
    df.set_index('date', inplace=True)
    df = df[~df.index.duplicated()]
    df = df.reindex(ind, fill_value=0)
    df = df.reset_index()
    df['date'] = df['index']
    df = df[['date','stations','total meteors','avg mets per station']]
    # Export
    df.to_csv(temp_path + '\imo_data_mod.csv', index=False)
    # Showers
    # Read data
    cal = pd.read_csv(sh_cal, sep=';')
    cal = cal[['Maximo']]
    cal = pd.to_datetime(cal['Maximo'], format='%d/%m/%Y')
    # Create a list of showers
    showers = list()
    for date in cal:
        showers.append(date)
    # Filter imo_mod to leave rows with shower max date
    filt = df['date'].isin(showers)
    df = df.loc[filt]
    # Export
    df.to_csv(temp_path + '\imo_showers.csv', index=False)

def graph_comp_imo(results_dir, temp_dir, diario_path, imo_results_path, year):
    """Creates yearly graph comparing daily meteor detections of IMO and SdC"""
    # Read data with Pandas
    sdc_data = pd.read_csv(results_dir + '\sdc_mod_daily.csv', sep=';')
    sdc_data['date'] = pd.to_datetime(sdc_data['date'])
    imo_data = pd.read_csv(temp_dir + '\imo_data_mod.csv')
    imo_data['date'] = pd.to_datetime(imo_data['date'])
    # Filter dates
    start_date = year + '-01-01'
    end_date = year + '-12-31'
    after_start_date = sdc_data['date'] >= start_date
    before_end_date = sdc_data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    sdc_data = sdc_data.loc[between_two_dates]
    sdc_dates = sdc_data['date']
    sdc_meteors = sdc_data['total']
    after_start_date = imo_data['date'] >= start_date
    before_end_date = imo_data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    imo_data = imo_data.loc[between_two_dates]
    imo_dates = imo_data['date']
    imo_meteors = imo_data['avg mets per station']
    # Style plot
    plt.style.use('seaborn-deep')
    plt.plot_date(sdc_dates, sdc_meteors, linestyle='solid', marker='None', label='Sonidos del Cielo')
    plt.plot_date(imo_dates, imo_meteors, linestyle='solid', marker='None', label='IMO')
    plt.gcf().set_size_inches(17, 8)
    plt.gcf().autofmt_xdate() #rotates dates
    date_format = mpl_dates.DateFormatter('%d/%m/%Y') #date format DD/MM/YYYY
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_major_locator(mpl_dates.MonthLocator(interval=1)) #1 day/month
    plt.xlabel('Fechas')
    plt.ylabel('Nº meteoros')
    plt.legend()
    plt.title('Detecciones diarias - Sonidos del Cielo vs IMO - ' + year)
    plt.savefig(imo_results_path + '\SdC_vs_IMO_' + year + '.png', dpi=75)
    # Showers
    # Read data
    showers_sdc = pd.read_csv(temp_dir + '\sdc_showers_daily.csv')
    showers_sdc['date'] = pd.to_datetime(showers_sdc['date'])
    dates_sh_sdc = showers_sdc['date']
    meteors_sh_sdc = showers_sdc['total']
    showers_imo = pd.read_csv(temp_dir + '\imo_showers.csv')
    showers_imo['date'] = pd.to_datetime(showers_imo['date'])
    dates_sh_imo = showers_imo['date']
    meteors_sh_imo = showers_imo['avg mets per station']
    plt.plot_date(dates_sh_imo, meteors_sh_imo, linestyle='', marker= 'o', label='Max day of showers - IMO', color='m')
    plt.plot_date(dates_sh_sdc, meteors_sh_sdc, linestyle='', marker= 'o', label='Max day of showers - SdC', color='r')
    plt.legend()
    plt.title("Detecciones diarias y lluvias - Sonidos del Cielo vs IMO - " + year)
    plt.savefig(diario_path + '\SdC_vs_IMO_' + year + '_lluvias.png', dpi=75)

def graph_sdc_hours(curvas_horarias_path, temp_dir, year):
    """Graphs mean meteor detections for each month by hour"""
    # Import data
    data = pd.read_csv(temp_dir + '\sdc_mod_monthly.csv', sep=';')
    # Plot all columns except 'total' for each month
    data = data.set_index('date')
    data = data.loc[ : , data.columns != 'total']
    for month in data.index:
        if month[3:] == '2019':
            plt.clf()
            plt.style.use('seaborn-deep')
            plt.plot(data.columns, data.loc[month])
            plt.xlabel('Hora')
            plt.ylabel('Nº meteoros')
            plt.title('Media de detecciones por hora Sonidos del Cielo - ' + month)
            plt.savefig(curvas_horarias_path + '\SdC_CurvaHoraria_' + month[0:2] + '_' + year + '.png', dpi=75)
    # Plot comparative
    plt.style.use('seaborn-deep')
    for month in data.index:
        if month[3:] == '2019':
            plt.plot(data.columns, data.loc[month], label=month)
    plt.xlabel('Hora')
    plt.ylabel('Nº meteoros')
    plt.title("Comparativa detecciones por hora (media mensual) Sonidos del Cielo - " + year)
    plt.legend()
    plt.savefig(curvas_horarias_path + '\SdC_CurvasHorarias_' + year + '.png', dpi=75)

def run_software():
    year, results_dir, sdc_data_path, imo_data_path, cal_path = get_user_input()
    results_dir, data_dir, imo_res_path, diario_path, lluvias_path, curvas_horarias_path, temp_dir = folder_structure(results_dir, year)
    mod_sdc_daily(sdc_data_path, results_dir, cal_path)
    graph_sdc_daily(results_dir, diario_path, year)
    mod_imo_avg(imo_data_path, temp_dir, cal_path)
    graph_comp_imo(results_dir, temp_dir, diario_path, imo_res_path, year)
    graph_sdc_hours(curvas_horarias_path, temp_dir, year)

run_software()