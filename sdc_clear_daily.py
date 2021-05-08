# Limpieza del csv Fuenlabrada Daily

import pandas as pd

# Eliminar todos los campos excepto daily totals
df = pd.read_csv('data\sdc_daily.csv', sep=';')
cols = range(1,169)
df.drop(df.columns[cols],axis=1, inplace=True)

# Renombrar columnas
df['Max S [dBm]'] = df['Max S [dBm].24']
df['Avg N [dBm]'] = df['Avg N [dBm].24']
df['Total'] = df['Total.24']
df['overdenses'] = df['overdenses.24']
df['underdenses'] = df['underdenses.24']
df['fakes'] = df['fakes.24']

# Eliminar columnas innecesarias
columns = ['Max S [dBm].24','Avg N [dBm].24','Total.24','overdenses.24','underdenses.24','fakes.24','|.24']
df.drop(columns, inplace=True, axis=1)

# Dejar fecha   Total-fakes
df['meteors'] = df['Total'] - df['fakes']
df['date'] = df['Date']
df = df[['date', 'meteors']]

# Convertir fechas a formato datetime
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

# Eliminar líneas sin datos de meteoros
df.dropna(inplace=True)

# Rellenar fechas que faltan con 0
ind = pd.date_range(min(df['date']), max(df['date'])) # serie que cubre todas las fechas en el rango disponible
df.set_index('date', inplace=True) # index = columna date
df = df[~df.index.duplicated()] # eliminar duplicados
df = df.reindex(ind, fill_value=0) # rellenar con 0 fechas sin datos
df = df.reset_index()
df['date'] = df['index']
df = df[['date','meteors']]

# Exportar
df.to_csv('results\csvs\sdc_clear_daily.csv', index=False)

# Resultado por mes
df_month = df
df_month.index = pd.to_datetime(df_month['date'])
df_month = df_month.groupby(pd.Grouper(freq='M')).sum()
df_month.index = df_month.index.strftime('%m/%Y')
df_month.to_csv('results\csvs\sdc_meteors_monthly.csv')