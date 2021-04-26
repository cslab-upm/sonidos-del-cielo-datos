import mylibrary as ml

# Create pandas dataframes from daily meteors csv file
sdc = ml.Metspd_csv(name='sdc_clear_daily')
imo = ml.Metspd_csv(name='imo_meteors_average', mets_col_name='avg mets per station')

ml.top_x_percent(sdc, 5)
ml.top_x_percent(imo, 5)