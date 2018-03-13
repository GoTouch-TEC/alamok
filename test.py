import logger
mylogger = logger.Logger()
for x in xrange(1,10):
	mylogger.backUp("data\n")
mylogger.closeBackUp()