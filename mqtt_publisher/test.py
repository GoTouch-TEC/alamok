
import publisher
import random
from random import randint
import time 
import os
#init the publisher object
publisher = publisher.Publisher()
publisher.start()#start the thread
counter = 0
try:
	while True:
		time.sleep(2)
		diction = {'id' : counter}
		publisher.publish_data(str(diction))
		counter = counter +1	
except(KeyboardInterrupt, SystemExit): 
	publisher.stopPublishing()
	print("bye")
