import os
import paho.mqtt.client as mqtt #import the client1
import threading #MultiThreading
import json # to load the config file.
class Publisher (threading.Thread):

	isConnected = False	

	def __init__(self):
		#init the thread
		threading.Thread.__init__(self)
		self.running = True #setting the thread running to true
		#reading the config file:
		config = json.loads(open('mqtt-defaults.json').read())
		#set the address

		self.broker_address=str(config["broker_address"])
		self.serverPort = config["serverPort"]
		self.user = str(config["user"])
		self.password = str(config["password"])
		self.Connected = False
		print("Is creating a new instance of MQTT publisher")
		# init the user
		self.client = mqtt.Client(str(config["topic"])) #create new instance
		# Set the password and user.
		self.client.username_pw_set(self.user, password=self.password)
		#attach function to callback
		self.client.on_message=self.on_message
		self.client.on_connect=self.on_connect   
		print("connecting to broker")
		try:
			self.client.connect(self.broker_address, port=self.serverPort)
			self.client.loop_start() #start the loop
			self.isConnected = True
		except Exception as error:
			print("Fail during connection")
			print (error)
			self.isConnected = False
			self.__stopThread()#stop the thread


	#callback on recieved message
	def on_message(self, client, userdata, message):
		print('\n')
		print("message received " ,str(message.payload.decode("utf-8")))
		print("message topic=",message.topic)
		print("message qos=",message.qos)
		print("message retain flag=",message.retain)

	#callback on recieved message    
	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			print("Connected to broker")
			self.Connected = True                #Signal connection
			print("Subscribing to topic","fonagotouch")
			self.client.subscribe("fonagotouch") 
		else:
			print("Connection failed")
			self.__stopThread()
			

	def __stopThread(self):
		print ("\nKilling Thread...")
		self.running = False

	def publish_data(self,data):
		try:
			self.client.publish("fonagotouch",data)
		except Exception: 
			print("Error publishing")

	def stopPublishing(self):
		self.running = False

	def __disconnectPublisher(self):
		print("disconnect...mqtt")
		try:
			self.client.disconnect()
			print('disconnected...mqtt')
		except Exception:
			print("Error disconnecting client")		

	def run(self):
		try:
			while self.running:
				pass
			self.__disconnectPublisher()
		except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
			print "\nKilling Thread..."
		 	self.running = False
		 	self.join() # wait for the thread to finish what it's doing
		


	