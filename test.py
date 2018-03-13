import logger
import publisher

mylogger = logger.Logger()
publisher = publisher.Publisher()
for x in xrange(1,10):
	mylogger.backUp("data\n")
	publisher.publish_data("test")
mylogger.closeBackUp()