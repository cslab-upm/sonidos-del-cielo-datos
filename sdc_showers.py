# Csv con las filas que coinciden con máximos de lluvias

import datetime
import pandas as pd

def showers_csv(cal_path, daily_path, year):
    # Open files
    cal = pd.read_csv(cal_path, sep=';')
    cal = cal[['Maximo']]
    cal = pd.to_datetime(cal['Maximo'], format='%d/%m/%Y')
    df = pd.read_csv(daily_path)
    df['date'] = pd.to_datetime(df['date'])

    # Create a list of the showers max date
    showers = list()
    for date in cal:
        showers.append(date)

    # Filter daily to leave rows with shower max date
    filt = df['date'].isin(showers)
    df = df.loc[filt]

    # Export
    df.to_csv('results\csvs\sdc_showers_' + year + '.csv', index=False)


showers_csv('data\cal2019.csv', 'results\csvs\sdc_clear_daily.csv', '2019')
showers_csv('data\cal2020.csv', 'results\csvs\sdc_clear_daily.csv', '2020')