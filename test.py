import logger
import publisher
import utils
import random
import SQL_Lite_Logger

#init the publisher object
#publisher = publisher.Publisher()
#init the sql lite logger
sqllogger = SQL_Lite_Logger.SQL_Lite_Logger()


# sets a random values to get the 
#latitude, longitude, speed, altitude, and the status

for x in xrange(1,10):
	latitude = 93 + random.random()/88855 # closing to CR
	longitude = -86 + random.random()/88855 # closing to CR
	status = random.uniform(1, 2) ## values {1 or 2}
	speed =random.uniform(1, 180) ## km/h
	altitude =random.uniform(3100, 3600) ##meters
	sqllogger.backUpData({'date': utils.getTime(),'latitude':latitude, 'longitude': longitude, 'status': status,'speed': speed, 'altitude': altitude})
	#publisher.publish_data("test")

