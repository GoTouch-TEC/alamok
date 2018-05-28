#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
from __future__ import print_function
import sys
import os
from gps import *
from time import *
import time
import threading
import json
sys.path.append("../mqtt_publisher/")
import publisher
sys.path.append("../sql_lite_logger/")
import SQL_Lite_Logger
import utils
import math

class GpsdMannager(threading.Thread):
    def __init__(self):
        self.gpsd=gps(mode=WATCH_ENABLE)
        self.running = False
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.running=True
        while self.running:
            self.gpsd.next()
    def fix(self):
        return self.gpsd.fix
    def utc(self):
        return self.gpsd.utc
    def satellites(self):
        return self.gpsd.satellites
    def stop(self):
        self.running=False

class GpsLogger(threading.Thread):
    def __init__(self, mqtt_config, db_filename, device_id="Alamok" ,refresh_time=3):
        self.running = False
        self.refresh_time=refresh_time
        self.device_id = device_id
        threading.Thread.__init__(self)
        self.gpsd=GpsdMannager()
        self.logger = SQL_Lite_Logger.SQL_Lite_Logger(db_filename)
        self.publisher = publisher.Publisher(broker_address=mqtt_config["broker_address"],
            broker_port=mqtt_config["broker_port"],out_topic= mqtt_config["out_topic"],
            in_topic=mqtt_config["in_topic"], user=mqtt_config["user"], password=mqtt_config["password"], device_id=mqtt_config["device_id"],on_publish=self.on_publish)

    def on_publish(self,client, userdata, mid):
        self.debug("move to successful:",mid)
        self.logger.move_to_successful(mid)

    def debug(self, *params):
		if(__debug__):
			for param in params:
				print(param, end=' ')
			print("")

    def run(self):
        self.publisher.start()
        self.running=True
        while (self.running):
            if(not self.publisher.status()):
                self.publisher.start()
            data = {'deviceId':self.device_id,'date': utils.getTime(),'latitude': self.gpsd.fix().latitude, 'longitude': self.gpsd.fix().longitude ,'speed': self.gpsd.fix().speed, 'altitude': self.gpsd.fix().altitude}
                # jalar data
            if(not math.isnan(data["speed"])):
                message_id = -1
                if (self.publisher.status()):
                    message_id = self.publisher.publish_data(str(data))
                self.logger.backup(data, message_id)
            time.sleep(self.refresh_time)
    def stop(self):
        self.gpsd.stop()
        self.running=False
