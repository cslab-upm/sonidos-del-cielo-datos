import mylibrary as ml

# Create pandas dataframes from daily meteors csv file
sdc = ml.Metspd_csv(name='sdc_clear_daily')
imo = ml.Metspd_csv(name='imo_meteors_average', mets_col_name='avg mets per station')
sdc_monthly = ml.Metspd_csv('sdc_meteors_monthly')
imo_monthly = ml.Metspd_csv(name='imo_meteors_average_monthly', mets_col_name='avg mets per station')

def test_sdc_alltimes():
    ml.create_metspd_graph(sdc)
    ml.plt.clf()

def test_sdc_2019():
    ml.create_metspd_graph(sdc, year='2019')
    ml.plt.clf()

def test_sdc_2020():
    ml.create_metspd_graph(sdc, year='2020')
    ml.plt.clf()

def test_imo_alltimes():
    ml.create_metspd_graph(imo)
    ml.plt.clf()

def test_imo_2019():
    ml.create_metspd_graph(imo,year='2019')
    ml.plt.clf()

def test_imo_2020():
    ml.create_metspd_graph(imo,year='2020')
    ml.plt.clf()

def test_comp_alltimes():
    ml.create_comparative_graph(sdc,imo)
    ml.plt.clf()

def test_comp_2019():
    ml.create_comparative_graph(sdc,imo,year='2019')
    ml.plt.clf()

def test_comp_2020():
    ml.create_comparative_graph(sdc,imo,year='2020')
    ml.plt.clf()

def test_imo_monthly_alltimes():
    ml.create_monthly_graph(imo_monthly)
    ml.plt.clf()

def test_sdc_monthly_alltimes():
    ml.create_monthly_graph(sdc_monthly)
    ml.plt.clf()

def test_imo_monthly_2019():
    ml.create_monthly_graph(imo_monthly,year='2019')
    ml.plt.clf()

def test_imo_monthly_2020():
    ml.create_monthly_graph(imo_monthly,year='2020')
    ml.plt.clf()

def test_sdc_monthly_2019():
    ml.create_monthly_graph(sdc_monthly,year='2019')
    ml.plt.clf()

def test_sdc_monthly_2020():
    ml.create_monthly_graph(sdc_monthly,year='2020')
    ml.plt.clf()

if __name__ == '__main__':
    test_sdc_alltimes()
    test_sdc_2019()
    test_sdc_2020()
    test_imo_alltimes()
    test_imo_2019()
    test_imo_2020()
    test_comp_alltimes()
    test_comp_2019()
    test_comp_2020()
    test_imo_monthly_alltimes()
    test_sdc_monthly_alltimes()
    test_imo_monthly_2019()
    test_imo_monthly_2020()
    test_sdc_monthly_2019()
    test_sdc_monthly_2020()