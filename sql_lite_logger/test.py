import logger
import publisher
import utils
import random
from random import randint
import SQL_Lite_Logger

#init the publisher object
#publisher = publisher.Publisher()
#publisher.start()
#publisher.join() 
#init the sql lite logger
sqllogger = SQL_Lite_Logger.SQL_Lite_Logger()
for x in xrange(1,100):
	latitude = 93 + random.random()/88855 # closing to CR
	longitude = -86 + random.random()/88855 # closing to CR
	status = randint(1, 2) ## values {1 or 2}
	speed =random.uniform(1, 180) ## km/h
	altitude =random.uniform(3100, 3600) ##meters
	sqllogger.backUpData({'date': utils.getTime(),'latitude':latitude, 'longitude': longitude, 'status': status,'speed': speed, 'altitude': altitude})


success_data = sqllogger.fetchSuccededData()
print(len(success_data))
fail_data = sqllogger.fetchFailedData()
print(len(fail_data))

sqllogger.cleanGPS_FAILED_LOG()
sqllogger.cleanGPS_LOG()
sqllogger.closeLogger()