import gps_logger

mqtt_config = {"broker_address":"13.59.16.98","broker_port":1884,"out_topic":"fonagotouch","in_topic":"","user":"","password":"","device_id":"5b00d2360a9eaf3f661c81f8"}
gps_log= gps_logger.GpsLogger(mqtt_config=mqtt_config,db_filename="test.db",device_id="5b00d2360a9eaf3f661c81f8",refresh_time=2)

gps_log.start()
try:
    while (True):
        pass

except(KeyboardInterrupt, SystemExit,Exception ) as error:
	gps_log.stop()
	print(error)
	print("bye")
