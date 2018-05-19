# import logger
# import publisher
import utils
import random
from random import randint
import SQL_Lite_Logger

#init the publisher object
#publisher = publisher.Publisher()
#publisher.start()
#publisher.join()
#init the sql lite logger
sqllogger = SQL_Lite_Logger.SQL_Lite_Logger('test.db')
for x in range(1,20):
	latitude = 93 + random.random()/88855 # closing to CR
	longitude = -86 + random.random()/88855 # closing to CR
	status = randint(1, 2) ## values {1 or 2}
	speed =random.uniform(1, 180) ## km/h
	altitude =random.uniform(3100, 3600) ##meters
	sqllogger.backup({'date': utils.getTime(),'latitude':latitude, 'longitude': longitude, 'status': status,'speed': speed, 'altitude': altitude}, message_id=x)
for x in range(1,20):
	data = sqllogger.move_to_successful(x)

ip_data = sqllogger.fetch_in_progress()
print("in_progress",len(ip_data))
success_data = sqllogger.fetch_successful()
print("successful",len(success_data))
# fail_data = sqllogger.fetchFailedData()
# for entry in fail_data:
# 	print("entry: ",entry[0])
# print(len(fail_data))

# sqllogger.clean_successful()
# sqllogger.clean_in_progress()
sqllogger.closeLogger()
