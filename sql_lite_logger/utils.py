import datetime
def getTime():
	#get the current time.
	new_date_key = str(datetime.datetime.now())
	new_date_key = new_date_key.replace(' ','T')#Setting ISO name fiel
	new_date_key += 'Z' # append to the end
	return new_date_key
