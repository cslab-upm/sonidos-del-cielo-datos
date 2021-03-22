import pandas as pd

# Lectura de datos con pandas
data = pd.read_csv('data\imo_data1.csv', sep=';')

# Renombrar la columna "Start Date" para evitar errores
data['date'] = data['Start Date']

# Eliminar la hora
data['date'] = pd.DatetimeIndex(data.date).normalize()

# Ordena los datos por fecha
data.sort_values('date', inplace=True)

# Suma Number para cada fecha y deja una sola fila por fecha
data['meteors'] = data.groupby('date')['Number'].transform('sum')
data.drop_duplicates(subset=['date'], inplace=True)

# Elimina columnas innecesarias del dataframe
data = data[['date','meteors']]

# Elimina duplicados
data.drop_duplicates(subset ='date', inplace = True)

# Guarda como csv
data.to_csv('results\csvs\imo_meteorspd.csv', index=False)