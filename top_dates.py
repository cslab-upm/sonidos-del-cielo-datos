import mylibrary as ml

# Create pandas dataframes from daily meteors csv file
sdc = ml.Metspd_csv(name='sdc_clear_daily')
imo = ml.Metspd_csv(name='imo_meteors_average', mets_col_name='avg mets per station')

sdc_monthly = ml.Metspd_csv('sdc_meteors_monthly')
imo_monthly = ml.Metspd_csv(name='imo_meteors_average_monthly', mets_col_name='avg mets per station')

def test_top_x_percent(percentage):
    print('\n\nTop ',percentage,'% \days with greatest meteor activity')
    print('\n\tIMO - 2019')
    ml.top_x_percent(sdc, percentage, '2019')
    print('\n\tIMO - 2020')
    ml.top_x_percent(sdc, percentage, '2020')
    print('\n\tSonidos del Cielo - 2019')
    ml.top_x_percent(imo, percentage, '2019')
    print('\n\tSonidos del Cielo - 2020')
    ml.top_x_percent(imo, percentage, '2020')

def test_top_x_months(months):
    print('\n\nTop ',months,' months with the most meteor detections in 2019')
    print('\n\tIMO - 2019')
    ml.top_x_months(sdc_monthly, months, '2019')
    print('\n\tSonidos del Cielo - 2019')
    ml.top_x_months(imo_monthly, months, '2019')

def test_top_n_days_month(days):
    print('\n\nTop ',days,' days with the most meteors in every month')
    print('\n\tIMO - 2019')
    ml.top_n_days_month(imo, days, '2019')
    print('\n\tIMO - 2020')
    ml.top_n_days_month(imo, days, '2020')
    print('\n\tSonidos del Cielo - 2019')
    ml.top_n_days_month(sdc, days, '2019')
    print('\n\tSonidos del Cielo - 2020')
    ml.top_n_days_month(sdc, days, '2020')

if __name__ == '__main__':
    test_top_x_percent(5)
    test_top_x_months(3)
    test_top_n_days_month(2)