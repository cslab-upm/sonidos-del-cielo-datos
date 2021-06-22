# Totales por hora y día csv Fuenlabrada Daily

import pandas as pd

df = pd.read_csv('data\sdc_daily.csv', sep=';')

# Fechas en formato datetime y eliminar líneas sin datos
df['date'] = df['Date']
for ind in df.index:
    date = df['date'][ind]

    # Saltar líneas sin datos
    if len(date) < 3:
        df.drop(ind, inplace=True)
        continue
    
    day = date[10:12]

    # Añadir 0 a días <10 (ej: 1 -> 01)
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

columns = ['date','00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
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

df_mod.to_csv('results\csvs\sdc_daily_hours.csv', index=False, sep=';')

# Resultados por mes
df_month = df_mod
df_month.index = pd.to_datetime(df_month['date'])
df_month = df_month.groupby(pd.Grouper(freq='M')).mean()
df_month.index = df_month.index.strftime('%m/%Y')
df_month.to_csv('results\csvs\sdc_monthly_hours.csv', sep=';')