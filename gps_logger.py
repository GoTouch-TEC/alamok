import sys
import os
import math
import time
import threading
import json
import datetime

from gps3.agps3threaded import AGPS3mechanism
from sql_lite_logger.SQL_Lite_Logger import SQL_Lite_Logger
from mqtt_publisher.publisher import Publisher

# TODO: Obtain the date from the gps
def getTime():
	#get the current time.
	new_date_key = str(datetime.datetime.now())
	new_date_key = new_date_key.replace(' ','T')#Setting ISO name fiel
	new_date_key += 'Z' # append to the end
	return new_date_key

class GpsdMannager():
    def __init__(self):
        self.gpsd_thread = AGPS3mechanism()
        self.gpsd_thread.stream_data()
        self.gpsd_thread.run_thread()
        # self.data = {'latitude': 0, 'longitude': 0, 'speed': 0, 'altitude': 0}

    def data(self):
        current_data = {'latitude': 0, 'longitude': 0, 'speed': 0, 'altitude': 0}
        current_data['latitude'] = self.gpsd_thread.data_stream.lat
        current_data['longitude'] = self.gpsd_thread.data_stream.lon
        current_data['speed'] = self.gpsd_thread.data_stream.speed
        current_data['altitude'] = self.gpsd_thread.data_stream.alt
        # print("CURRENT DATA:", current_data);
        return current_data


class GpsLogger(threading.Thread):
    def __init__(self, config, db_filename):
        self.gpsd = GpsdMannager()
        self.running = False
        self.refresh_time = config["refresh_time"]
        self.device_id = config["device_id"]
        threading.Thread.__init__(self)

        self.logger = SQL_Lite_Logger(db_filename)

        self.publisher = Publisher(broker_address=config["broker_address"],
                                             broker_port=config["broker_port"], out_topic=config["out_topic"],
                                             in_topic=config["in_topic"], username=config["username"],
                                             password=config["password"], device_id=config["device_id"],
                                             on_publish=self.on_publish)

    def on_publish(self, client, userdata, message_id):
        self.debug("moved to successful:", message_id)
        self.logger.move_to_successful(message_id)

    def debug(self, *params):
        if(__debug__):
            for param in params:
                print(param, end=' ')
                print("")

    def run(self):
        self.publisher.start()
        self.running = True
        while (self.running):
            try:
                if(not self.publisher.status()):
                    self.publisher.start()
                data = self.gpsd.data()
                data['deviceId'] = self.device_id
                data['date'] = getTime()
                if(data['latitude'] != "n/a"):
                    message_id = -1
                    if (self.publisher.status()):
                        message_id = self.publisher.publish_data(str(data))
                    self.logger.backup(data, message_id)
                else:
                    self.debug("GPS data error:", data)
                time.sleep(self.refresh_time)
            except Exception as error:
                print("Error:", error)

    def stop(self):
        self.running = False
