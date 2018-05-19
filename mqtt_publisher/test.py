
import publisher
import random
from random import randint
import time
import os
import datetime
#init the publisher object
connected = False
MQTT_publisher = None
try:
	# "198.41.30.241" cloudmqtt
	# 198.41.30.241 iot.eclipse.org
	MQTT_publisher = publisher.Publisher( "198.41.30.241", 1883, "fonagotouch")#init the object
	connected = MQTT_publisher.isConnected# it is connected?
	if(connected):
		print("MQTT publisher is connected")
	else:
		print("MQTT publisher is not connected")
	MQTT_publisher.start()#start the thread

except Exception:
	print(" Error MQTT creating the publisher")

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
		MQTT_publisher.stopPublishing()
	print(error)
	print("bye")
