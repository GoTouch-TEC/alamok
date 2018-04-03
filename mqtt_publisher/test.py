
import publisher
import random
from random import randint
import time 
import os
#init the publisher object

try:
	MQTT_publisher = publisher.Publisher()#init the object	
	connected = MQTT_publisher.isConnected# it is connected?
	if(connected):
		print("MQTT publisher is connected")
	else:
		print("MQTT publisher is not connected")
	MQTT_publisher.start()#start the thread
except Exception:
	print("MQTT creating the publisher")
try:
	while connected:
		time.sleep(2)
		diction = {'id' : counter}
		publisher.publish_data(str(diction))
		counter = counter +1	
except(KeyboardInterrupt, SystemExit,Exception): 
	publisher.stopPublishing()
	print("bye")
