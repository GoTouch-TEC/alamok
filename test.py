import os, sys, inspect #to import files from relative path.
import random # to create random numbers
from random import randint# to create random integer
import time # to get the time
import os # to get os operations like keyboard typings

sys.path.append("mqtt_publisher/")
import publisher
sys.path.append("sql_lite_logger/")
import SQL_Lite_Logger
import utils

def main():
    def on_publish(client, userdata, mid):
        print("move to successful:",mid)
        sqllogger.move_to_successful(mid)
    conneted_broker = False
    running = True
    sqllogger = SQL_Lite_Logger.SQL_Lite_Logger("test.db")
	#init the publisher object
    try:
        MQTT_publisher = publisher.Publisher('iot.eclipse.org', out_topic="fonagotouch", on_publish=on_publish)#init the object
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
            message_id = -1
            if (conneted_broker):
            	message_id = MQTT_publisher.publish_data(str(diction))
            sqllogger.backup(diction, message_id)

    except(KeyboardInterrupt, SystemExit):
        if(conneted_broker):
            MQTT_publisher.stopPublishing()
        running = False
        print("bye")
main()
