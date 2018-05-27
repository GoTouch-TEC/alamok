import gps_logger

mqtt_config = {"broker_address":"iot.eclipse","broker_port":1883,"out_topic":"Alamok_TEST","in_topic":"","user":"","password":"","device_id":"AlamokTest"}
gps_log= gps_logger.GpsLogger(mqtt_config=mqtt_config,db_filename="test.db",device_id="Alamok",refresh_time=2)

gps_log.start()
try:
    while (True):
        pass

except(KeyboardInterrupt, SystemExit,Exception ) as error:
	if(connected):
		gps_log.stop()
	print(error)
	print("bye")
