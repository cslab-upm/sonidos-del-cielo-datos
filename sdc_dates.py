import pandas as pd

# Lectura de datos con pandas
data = pd.read_csv('data\sdc_data1.csv')

# Eliminar la hora
data['date'] = pd.DatetimeIndex(data.DATE).normalize()

# Ordena los datos por fecha
data.sort_values('date', inplace=True)

# Cuenta el nº de veces que se repite una fecha = nº detecciones
data['meteors'] = data.groupby('date')['date'].transform('count')

# Elimina columnas innecesarias del dataframe
data = data[['date','meteors']]

# Elimina duplicados
data.drop_duplicates(subset ='date', inplace = True)

# Guarda como csv
data.to_csv('results\csvs\sdc_meteorspd.csv', index=False)