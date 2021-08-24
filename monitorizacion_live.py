"""Software tool to monitor data from Sonidos del Cielo / Contadores de Estrellas"""

import os
from datetime import datetime
import paho.mqtt.client as mqtt
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Welcome
print("\n\t ********* ANÁLISIS DE DATOS DE CONTADORES DE ESTRELLAS - MONITORIZACIÓN EN VIVO *********")
print("\nEsperando meteoros...")

# Connect to MQTT server
MQTT_HOST = 'vps190.cesvima.upm.es'
MQTT_PORT = 1883

MQTT_TOPIC_STATIONS = "station/echoes/#"
MQTT_TOPIC_SERVER_UP = "server/status/up"

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="Sonidos_del_Cielo"
    )
mycursor = db.cursor()

# Define functions        
def on_message(client, userdata, message):
	print("\nMETEORO DETECTADO\n")
	# Import mysql data to pandas dataframe
	df = pd.read_sql("SELECT * from daily", db, index_col = 'date')
	# Get current datetime
	date = datetime.now().date()
	time = datetime.now().time()
	# Modify row if date has already been added
	if str(date) in df.index.values:
		if len(str(time.hour)) == 1:
			df.loc[str(date), '0' + str(time.hour) + 'H'] = df.loc[str(date), '0' + str(time.hour) + 'H'] + 1
		else:
			df.loc[str(date), str(time.hour) + 'H'] = df.loc[str(date), str(time.hour) + 'H'] + 1
		df.loc[str(date), 'total'] = df.loc[str(date), 'total'] + 1
		df = df.reset_index()
		print('\nBase de datos actualizada:\n', df)
	# Add new row with date
	else:
		# reset index on data
		df = df.reset_index()
		# create new row
		new_row = {'date':str(date), '00H':0, '01H':0, '02H':0, '03H':0, '04H':0, '05H':0, '06H':0, '07H':0, '08H':0, '09H':0, '10H':0, '11H':0,
			'12H':0, '13H':0, '14H':0, '15H':0, '16H':0, '17H':0, '18H':0, '19H':0, '20H':0, '21H':0, '22H':0, '23H':0, 'total':1}
		if len(str(time.hour)) == 1:
			new_row['0' + str(time.hour) + 'H'] = 1
		else:
			new_row[str(time.hour) + 'H'] = 1
		# append new row to df
		df = df.append(new_row, ignore_index=True)
		print('\nBase de datos actualizada:\n', df)
	# Empty old table
	mycursor.execute("TRUNCATE daily")
	# Export dataframe to table
	engine = create_engine("mysql://root:1234@localhost/Sonidos_del_Cielo")
	con = engine.connect()
	df.to_sql('daily', con, if_exists='replace', index=False)
	print("\nEsperando meteoros...")

# Start MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC_STATIONS)

mqtt_client.loop_forever()