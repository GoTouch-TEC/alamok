# import logger
# import publisher
import random
from random import randint
import SQL_Lite_Logger
import datetime
#init the publisher object
#publisher = publisher.Publisher()
#publisher.start()
#publisher.join()
#init the sql lite logger
def getTime():
	#get the current time.
	new_date_key = str(datetime.datetime.now())
	new_date_key = new_date_key.replace(' ','T')#Setting ISO name fiel
	new_date_key += 'Z' # append to the end
	return new_date_key

sqllogger = SQL_Lite_Logger.SQL_Lite_Logger('test.db')
in_progress = {}
completed = []
for x in range(1,20):
	latitude = 93 + random.random()/88855 # closing to CR
	longitude = -86 + random.random()/88855 # closing to CR
	status =  2## values {1 or 2}
	speed =random.uniform(1, 180) ## km/h
	altitude =random.uniform(3100, 3600) ##meters
	datestamp =  getTime()
	sqllogger.backup({'date':datestamp,'latitude':latitude, 'longitude': longitude, 'status': status,'speed': speed, 'altitude': altitude})
	completed.append(datestamp)


# for x in :
data = sqllogger.mark_as_successful(completed)

ip_data = sqllogger.fetch_in_progress()
print("in_progress:",len(ip_data))
success_data = sqllogger.fetch_successful()
print("successful:",len(success_data))
print(success_data)

sqllogger.clear()
sqllogger.close_logger()
