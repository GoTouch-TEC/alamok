import os, sys, inspect #to import files from relative path.
import random # to create random numbers
from random import randint# to create random integer
import time # to get the time
import os # to get os operations like keyboard typings
import threading #MultiThreading

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
    MQTT_publisher = publisher.Publisher('iot.eclipse.org', out_topic="fonagotouch", on_publish=on_publish)#init the object
    MQTT_publisher.start()

    try:
        MQTT_publisher.start()
    except Exception as error:
        print( '\033[91mCannot create the publisher \033[0m')
        print(error)
    if MQTT_publisher.status():
        print('\033[94mPublisher connected \033[0m')
        # MQTT_publisher.start()#start the thread
    else:
        print('\033[91mPublisher not connected \033[0m')
    try:
        cont = 0
        prom = 0
        while running:
            if(not MQTT_publisher.status()):
                MQTT_publisher.start()
            start = time.time()
            # time.sleep(0.5)
            latitude = 93 + random.random()/88855 # closing to CR
            longitude = -86 + random.random()/88855 # closing to CR
            status = randint(1, 2) ## values {1 or 2}
            speed =random.uniform(1, 180) ## km/h
            altitude =random.uniform(3100, 3600) ##meters
            diction = {'date': utils.getTime(),'latitude':latitude, 'longitude': longitude, 'status': status,'speed': speed, 'altitude': altitude}
            message_id = -1
            print("Connection status:",MQTT_publisher.status())
            print("Client status:",MQTT_publisher.client._state)
            if (MQTT_publisher.status()):
                message_id = MQTT_publisher.publish_data(str(diction))
                # print(message_id)
            sqllogger.backup(diction, message_id)
            end = time.time()
            # print("elapsed time",end - start)
            cont+=1
            prom+= (end - start)
            # print("prom time:", prom/cont)



    except(KeyboardInterrupt, SystemExit):
        if(conneted_broker):
            MQTT_publisher.stop()
        running = False
        print("bye")
main()
