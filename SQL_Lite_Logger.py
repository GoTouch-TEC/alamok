
import sqlite3
from string import Template
class SQL_Lite_Logger:

	def __init__(self):
		#set the db connection
		self.connection = sqlite3.connect('gpslog.db')
		self.cursor = self.connection.cursor()# gets a sql lite cursor.
		self.gps_logs ="gpslogs"#data base for send messages that are successful
		self.fail_gps_logs="fail_gps_logs"# data base for messages that are not successfully sent
		#tries to create a table
		try:
			#creates a database for successfully sent messages
			self.cursor.execute('''CREATE TABLE gpslogs (datestamp text, latitude real, longitude real, speed real, altitude real)''')
			#creates a database for fault sent messages
			self.cursor.execute('''CREATE TABLE fail_gps_logs (datestamp text, latitude real, longitude real, speed real, altitude real)''')
		except sqlite3.OperationalError:
			print("Table already exists so table will not be created") 
	

	#{ 'date': 'datasamp'
	#  'latitude': 'double number'
	#  'longitue': 'double number'
	#  'altitude': 'double number'
	#  'speed'   : 'double number'    
	#  'status': 1:success during mqtt export or 2:fault sending the logs  }	
	def backUpData (self,data):
		#verify the data is not null.
		if (not(data is None)):
			print("Saving gps data log")
			try:
				#init string query
				string_query = ""
				#creates a template of the command
				query = Template("INSERT INTO $dbName VALUES ('$date',$latitude,$longitude,$speed,$altitude)")
				#checks the status of the gps log
				if(data['status'] == 1):
					#makes a substitution of data: Success Log
					string_query = query.substitute(dbName=self.gps_logs, date=data['date'] , latitude=data['latitude'], longitude=data['longitude'], speed=data['speed'],altitude=data['altitude'] )	
				elif (data['status']==2):
					#makes a substitution of data:  Failed Log
					string_query = query.substitute(dbName=self.fail_gps_logs, date=data['date'] , latitude=data['latitude'], longitude=data['longitude'], speed=data['speed'],altitude=data['altitude'])	
				else:
					#makes a substitution of data: Not defined Log
					string_query = query.substitute(dbName=self.fail_gps_logs, date=data['date'] , latitude=data['latitude'], longitude=data['longitude'], speed=data['speed'],altitude=data['altitude'])	
				try: #tries to insert into gpslogs table 
					#debug print
					print("Trying to exec: ",string_query)
					self.cursor.execute(string_query)#executes the query built from template
					self.connection.commit()#saves changes to local db.
				except RuntimeError:#catch a runtime error	
					print('Fail during insertion of gpslogs')
			except RuntimeError:#catch a runtime error
				print("Error creating the command")
		else:#param data is null
			print("Param data is not null")

	#This function closes the data base connection.		
	def closeBackUp (self):
		print("Close BackUp Data Base")
		try:#tries to close the data base
			self.connection.close()
		except RuntimeError:#catch an error during the last command
			print("Error while closing data base connection")	


	def fetchFailedData (self):
		print("\n")
		data_Failed = self.cursor.execute("SELECT * FROM fail_gps_logs ")
		data_item = data_Failed.fetchone()
		while (not(data_item is None)):
			print(str(data_item))
			data_item = data_Failed.fetchone()

	def fetchSuccededData (self):
		print("\n")
		data_succeded = self.cursor.execute("SELECT * FROM gpslogs ")
		data_item = data_data_succeded.fetchone()
		counter = 0
		while (not(data_item is None)):
			print(str(data_item))
			data_item = data_data_succeded.fetchone()
			counter = counter + 1

	