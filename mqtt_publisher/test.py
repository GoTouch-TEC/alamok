
import publisher
import random
from random import randint
import time
import os
import datetime
#init the publisher object
connected = False
MQTT_publisher = None
# try:
# "198.41.30.241" cloudmqtt
# 198.41.30.241 iot.eclipse.org
# MQTT_publisher = publisher.Publisher( "198.41.30.241", 1883, "fonagotouch")#init the object
MQTT_publisher = publisher.Publisher( "localhost", 1883, "fonagotouch",device_id="publisher")#init the object
MQTT_publisher.start()
connected = MQTT_publisher.initial_connection# it is connected?
if(connected):
	print("MQTT publisher is connected")
else:
	print("MQTT publisher is not connected")

# except Exception:
# 	print(" Error MQTT creating the publisher")

try:
	counter = 0
	while connected:
		time.sleep(2)
		diction = {
			'trip_id' : " Coronado - TEC ",
			'lat' : 9.8569,
			'lng' :-83.9130,
			'speed': 100,
			'alitute': 1420,
			'dtime': str(datetime.datetime.now())
		}
		MQTT_publisher.publish_data(str(diction))
		counter = counter +1
except(KeyboardInterrupt, SystemExit,Exception ) as error:
	if(connected):
		MQTT_publisher.stop()
	print(error)
	print("bye")
