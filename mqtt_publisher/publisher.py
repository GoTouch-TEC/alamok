import os
import paho.mqtt.client as mqtt #import the client1
import json # to load the config file.

class Publisher ():

	def __init__(self, broker_address, broker_port=1883, out_topic="", in_topic="", user="", password="", on_publish=None, device_id="" ):
		self.running = True #setting the thread running to true
		self.broker_address = broker_address
		self.broker_port = broker_port
		self.user = user
		self.password = password
		self.isConnected = False
		self.out_topic=out_topic
		self.in_topic=in_topic
		# init the user
		if(device_id): #
			self.client = mqtt.Client(device_id) #create new instance
		else:
			self.client = mqtt.Client()
		if(user): # ask if auth is required
			self.client.username_pw_set(self.user, password=self.password)
		#attach function to callback
		self.client.on_message=self.on_message
		self.client.on_connect=self.on_connect
		if(on_publish is not None):
			self.client.on_publish=on_publish

		self.debug("connecting to broker")

		try:
			self.client.connect(self.broker_address, port=self.broker_port)
			self.client.loop_start() #start the loop
			self.isConnected = True

		except Exception as error:
			self.debug("Fail during connection")
			self.debug (error)
			self.isConnected = False


	#callback on recieved message
	def on_message(self, client, userdata, message):
		self.debug('\n')
		self.debug("message received " ,str(message.payload.decode("utf-8")))
		self.debug("message topic=",message.topic)
		self.debug("message qos=",message.qos)
		self.debug("message retain flag=",message.retain)

	#callback on recieved message
	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			self.debug("Connected to broker")
			self.isConnected = True                #Signal connection
			if(self.in_topic):
				self.debug("Subscribing to topic", self.in_topic)
				self.client.subscribe(self.in_topic)
		else:
			self.debug("Connection failed")
			self.__stopThread()


	def __stopThread(self):
		self.debug("Killing Thread...")
		self.running = False

	def publish_data(self,data):
		try:
			msg_info = self.client.publish(self.out_topic,data, qos=1)
			self.debug("Published:",data)
			return msg_info.mid
		except Exception:
			self.debug("Error publishing")





	def stopPublishing(self):
		self.running = False

	def __disconnectPublisher(self):
		self.debug("disconnect...mqtt")
		try:
			self.client.disconnect()
			self.debug('disconnected...mqtt')
		except Exception:
			self.debug("Error disconnecting client")

	def debug(self, *params):
		if(__debug__):
			for param in params:
				print(param, end=' ')
			print("")
