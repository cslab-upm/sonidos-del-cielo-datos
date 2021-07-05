# Csv con las filas que coinciden con máximos de lluvias

import datetime
import pandas as pd

def only_showers_csv(year):
    # Rutas
    cal_path = 'data\cal_' + year + '.txt'
    results_path = 'results\csvs\sdc_showers_' + year + '.csv'

    # Abrir y leer calendario de lluvias y detecciones diarias
    cal = pd.read_csv(cal_path, squeeze=True)
    cal = pd.to_datetime(cal, format='%d/%m/%Y')
    df = pd.read_csv('results\csvs\sdc_clear_daily.csv')
    df['date'] = pd.to_datetime(df['date'])

    # Convertir el txt con las lluvias a lista
    showers = list()
    for ind in cal.index:
        showers.append(cal[ind])

    # Filtrar
    filt = df['date'].isin(showers)
    df = df.loc[filt]

    # Exportar
    df.to_csv(results_path, index=False)

only_showers_csv('2019')