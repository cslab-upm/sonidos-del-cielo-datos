import mylibrary as ml

# Create pandas dataframes from daily meteors csv file
sdc = ml.Metspd_csv(name='sdc_clear_daily')
imo = ml.Metspd_csv(name='imo_meteors_average', mets_col_name='avg mets per station')

sdc_monthly = ml.Metspd_csv('sdc_meteors_monthly')
imo_monthly = ml.Metspd_csv(name='imo_meteors_average_monthly', mets_col_name='avg mets per station')

print('Top 5%\ days with greatest meteor activity')
print('\t IMO')
ml.top_x_percent(sdc, 5, '2019')
ml.top_x_percent(sdc, 5, '2020')
print('\t Sonidos del Cielo')
ml.top_x_percent(imo, 5, '2019')
ml.top_x_percent(imo, 5, '2020')

print('Top 3 months with the most meteor detections in 2019')
print('\t IMO')
ml.top_x_months(sdc_monthly, 3, '2019')
print('\t Sonidos del Cielo')
ml.top_x_months(imo_monthly, 3, '2019')