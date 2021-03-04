import csv

imo_meteor_per_day = dict() #fecha -> nº detecciones

# Guardar todas las fechas de sesiones y las detecciones de la sesión en un csv temp
with open('data\imo_data1.csv', 'r') as imo_data:
    csv_reader = csv.DictReader(imo_data, delimiter=';')

    with open('results\imo_data_mod.csv', 'w', newline='') as imo_tmp:
        fieldnames = ['date', 'meteors']
        csv_writer = csv.DictWriter(imo_tmp, fieldnames=fieldnames, delimiter=',')

        csv_writer.writeheader()

        for line in csv_reader:
            csv_writer.writerow({'date': line['Start Date'][:10], 'meteors': line['Number']})
        
        # Re-abrir imo_tmp para lectura
        with open('results\imo_data_mod.csv', 'r') as imo_tmp:
            csv_reader = csv.DictReader(imo_tmp, delimiter=',')

            # Almacenar diccionario día - detecciones/día
            for line in csv_reader:
                # += detecciones
                imo_meteor_per_day[line['date']] = imo_meteor_per_day.get(line['date'], 0) + int(line['meteors'])
            
            # Almacena resultados en csv final
            with open('results\imo_meteorspd.csv', 'w') as imo_pd:
                imo_pd.write("Date,Meteors")
                for key in imo_meteor_per_day.keys():
                    imo_pd.write("\n%s,%s"%(key, imo_meteor_per_day[key]))
