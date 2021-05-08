import pandas as pd

# CALCULA LAS DETECCIONES DIARIAS COMO LA MEDIA DE DETECCIONES POR ESTACIÓN (sum(number_fecha) / sum(estaciones_fecha))

data = pd.read_csv('data\imo_data1.csv', sep=';')

# Reconfigurar la columna de fecha
data['date'] = data['Start Date'] # Renombrar
data['date'] = pd.DatetimeIndex(data.date).normalize() # Eliminar la hora
data['date'] = pd.to_datetime(data['date']) # Formato datetime
data.sort_values('date', inplace=True) # Ordenar los datos por fecha

# Contar detecciones medias por estación
total_mets = data.groupby('date')['Number'].sum() # Sumar meteoros en cada fecha

stations = data.groupby('date')['Obs Session ID'].nunique() # Contar nº estaciones distintas en cada fecha

df = total_mets.to_frame().reset_index()
df2 = stations.to_frame().reset_index()
df['stations'] = df2['Obs Session ID']
df['total meteors'] = df['Number']

df['avg mets per station'] = df['total meteors'] / df['stations'] # Media de meteoros por estación

df = df[['date','stations','total meteors','avg mets per station']] # Reordenar

# Rellenar fechas que faltan con 0
ind = pd.date_range(min(df['date']), max(df['date'])) # serie que cubre todas las fechas en el rango disponible
df.set_index('date', inplace=True) # index = columna date
df = df[~df.index.duplicated()] # eliminar duplicados
df = df.reindex(ind, fill_value=0) # rellenar con 0 fechas sin datos
df = df.reset_index()
df['date'] = df['index']
df = df[['date','stations','total meteors','avg mets per station']]

# Exporta como csv
df.to_csv('results\csvs\imo_meteors_average.csv', index=False)

# Resultado por mes
df_month = df
df_month.index = pd.to_datetime(df_month['date'])
df_month = df_month.groupby(pd.Grouper(freq='M')).sum()
df_month.index = df_month.index.strftime('%m/%Y')
df_month.to_csv('results\csvs\imo_meteors_average_monthly.csv')