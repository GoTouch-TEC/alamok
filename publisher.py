import os
import paho.mqtt.client as mqtt #import the client1
import threading #MultiThreading
class Publisher (threading.Thread):

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


	def __init__(self):
		#init the thread
		threading.Thread.__init__(self)
		self.running = True #setting the thread running to true
		#set the address
		self.broker_address="m11.cloudmqtt.com"
		self.serverPort = 13933
		self.user = "xelgtveu"
		self.password = "oYgQjqYbuaop"
		self.Connected = False
		print("creating new instance")
		# init the user
		self.client = mqtt.Client("GPS-GOTOUHC-MODULE") #create new instance
		# Set the password and user.
		self.client.username_pw_set(self.user, password=self.password)
		#attach function to callback
		self.client.on_message=self.on_message
		self.client.on_connect=self.on_connect   
		print("connecting to broker")
		self.client.connect(self.broker_address, port=self.serverPort)
		self.client.loop_start() #start the loop

	def run(self):
		try:
			while True:
				pass
		except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
		  print "\nKilling Thread..."
		  self.running = False
		  self.join() # wait for the thread to finish what it's doing
		


	def publish_data(self,data):
		self.client.publish("fonagotouch",data)

