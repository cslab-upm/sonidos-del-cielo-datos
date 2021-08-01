import os
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import pandas as pd

MQTT_HOST = 'vps190.cesvima.upm.es'
MQTT_PORT = 1883

MQTT_TOPIC_STATIONS = "station/echoes/#"
MQTT_TOPIC_SERVER_UP = "server/status/up"

def on_station_message(client, userdata, msg):
	mensaje = json.loads(str(msg.payload.decode("utf-8")))
        
def on_message(client, userdata, message):
	msg = str(message.payload.decode("utf-8"))
	pos = msg.rfind("event_id")
	date = msg[pos + 12 : pos + 16] + '-' + msg[pos + 16 : pos + 18] + '-' + msg[pos + 18 : pos + 20]
	time = msg[pos + 20 : pos + 22] + ':' + msg[pos + 22 : pos + 24]
	print('\n\nDate: %s\nTime: %s\n\n' % (date, time))
	hour = msg[pos + 20 : pos + 22]
	df = pd.read_csv('mqtt_daily.csv', sep=';', index_col='date')
	print(df)
	if date in df.index.values:
		print ('date exists')
		df.index = pd.to_datetime(df.index)
		date = pd.to_datetime(date, format='%Y-%m-%d')
		df.loc[date, hour] = df.loc[date, hour] + 1
		df.loc[date, 'total'] = df.loc[date, 'total'] + 1
		print(df)
		df.to_csv('mqtt_daily.csv', index=True, sep=';')
	else:
		print('new date')
		# reset index on data
		df = df.reset_index()
		# create new row
		new_row = {'date':date, '00':0, '01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0,
					'13':0, '14':0, '15':0, '16':0, '17':0, '18':0, '19':0, '20':0, '21':0, '22':0, '23':0, 'total':1}
		new_row[hour] = 1
		# append new row to df
		df = df.append(new_row, ignore_index=True)
		# print out final dataframe
		print(df)
		df.to_csv('mqtt_daily.csv', index=False, sep=';')

def serverUp():
	mqtt_client = mqtt.Client()
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.loop_start()
	mqtt_client.publish(MQTT_TOPIC_SERVER_UP, True)
	mqtt_client.loop_stop()

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC_STATIONS)

mqtt_client.loop_forever()