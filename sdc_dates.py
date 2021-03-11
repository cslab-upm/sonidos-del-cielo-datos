import csv

sdc_meteor_per_day = dict() #fecha -> nº detecciones

# Guardar fechas de cada detección en un csv temporal
with open('data\sdc_data1.csv', 'r') as sdc_data:
    csv_reader = csv.DictReader(sdc_data)

    with open('results\sdc_data_mod.csv', 'w') as sdc_tmp:
        for line in csv_reader:
            sdc_tmp.write("%s\n" % line['DATE'][:10])
        
        # Re-abrir sdc_tmp para lectura
        with open('results\sdc_data_mod.csv', 'r') as sdc_tmp:
            # Almacenar conteo de apariciones de cada fecha en el diccionario
            for line in sdc_tmp:
                sdc_meteor_per_day[line.rstrip('\n')] = sdc_meteor_per_day.get(line.rstrip('\n'), 0) + 1
            
            # Guardar diccionario en forma de csv
            with open('results\sdc_meteorspd.csv', 'w') as sdc_pd:
                sdc_pd.write("Date,Meteors")
                for key in sdc_meteor_per_day.keys():
                    sdc_pd.write("\n%s,%s"%(key, sdc_meteor_per_day[key]))