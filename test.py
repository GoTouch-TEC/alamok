import os, sys, inspect #to import files from relative path.
import random # to create random numbers
from random import randint# to create random integer
import time # to get the time
import os # to get os operations like keyboard typings
cmd_subfolder_mqtt = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"mqtt_publisher")))
cmd_subfolder_sql = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"sql_lite_logger")))
if cmd_subfolder_mqtt not in sys.path:
    sys.path.insert(0, cmd_subfolder_mqtt)
if cmd_subfolder_sql not in sys.path:
    sys.path.insert(0, cmd_subfolder_sql)
import publisher
import SQL_Lite_Logger
import utils

def main():
	conneted_broker = False
	running = True
	sqllogger = SQL_Lite_Logger.SQL_Lite_Logger()
	#init the publisher object
	try:
		MQTT_publisher = publisher.Publisher()#init the object	
		conneted_broker = MQTT_publisher.isConnected# it is connected?
	except Exception as error:
		print( '\033[91mCannot create the publisher \033[0m')
		print(error)
	if conneted_broker:
		print('\033[94mPublisher connected \033[0m')
		MQTT_publisher.start()#start the thread
	else:
		print('\033[91mPublisher not connected \033[0m')
	try:
		while running:
			time.sleep(2)
			latitude = 93 + random.random()/88855 # closing to CR
			longitude = -86 + random.random()/88855 # closing to CR
			status = randint(1, 2) ## values {1 or 2}
			speed =random.uniform(1, 180) ## km/h
			altitude =random.uniform(3100, 3600) ##meters
			diction = {'date': utils.getTime(),'latitude':latitude, 'longitude': longitude, 'status': status,'speed': speed, 'altitude': altitude}
			sqllogger.backUpData(diction)
			if (conneted_broker):
				MQTT_publisher.publish_data(str(diction))
	except(KeyboardInterrupt, SystemExit): 
		if(conneted_broker):
			MQTT_publisher.stopPublishing()
		running = False
		print("bye")
main()