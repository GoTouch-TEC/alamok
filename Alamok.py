#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
import sys
import os
from gps import *
from time import *
import time
import threading
import json
sys.path.append("mqtt_publisher/")
import publisher
sys.path.append("sql_lite_logger/")
import logger


gpsd = None #seting the global variable
#init the publisher object
connected = False
MQTT_publisher = None
os.system('clear') #clear the terminal (optional)

class GpsPoller(threading.Thread):
  #self.data = {}


  def __init__(self):
    self.data={}
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
    self.data['coordinates'] = [] # init array in
    MQTT_publisher = publisher.Publisher()#init the object
	connected = MQTT_publisher.isConnected# it is connected?
	if(connected):
		print("MQTT publisher is connected")
	else:
		print("MQTT publisher is not connected")
	MQTT_publisher.start()#start the thread

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  #set backup file, a new one each time that this file is set to run
  ## init the logger
  logger = logger.Logger();

  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

      os.system('clear')

      print
      print ' GPS reading'
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'eps         ' , gpsd.fix.eps
      print 'epx         ' , gpsd.fix.epx
      print 'epv         ' , gpsd.fix.epv
      print 'ept         ' , gpsd.fix.ept
      print 'speed (m/s) ' , gpsd.fix.speed
      print 'climb       ' , gpsd.fix.climb
      print 'track       ' , gpsd.fix.track
      print 'mode        ' , gpsd.fix.mode
      print
      print 'sats        ' , gpsd.satellites

      gpsp.data['coordinates'].append({
        'latitude': gpsd.fix.latitude,
        'longitude': gpsd.fix.longitude,
        'time utc': gpsd.utc
      })

      logger.backUp({
        'latitude': gpsd.fix.latitude,
        'longitude': gpsd.fix.longitude,
        'time utc': gpsd.utc
      })
      if(connected):
        MQTT_publisher.publish_data(str({
            'latitude': gpsd.fix.latitude,
            'longitude': gpsd.fix.longitude,
            'time utc': gpsd.utc
        }))
      time.sleep(3) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing

  logger.closeBackUp()
  print "\nDone"
