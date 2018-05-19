
import sqlite3
from string import Template
import threading #MultiThreading
class SQL_Lite_Logger:

	def __init__(self, filename):
		#set the db connection
		self.connection = sqlite3.connect(filename, check_same_thread = False)
		self.cursor = self.connection.cursor()# gets a sql lite cursor.
		self.db_in_progress ="in_progress"#data base for send messages that are successful
		self.db_successful="sended"# data base for messages that are not successfully sent
		self.lock = threading.Lock()
		#tries to create a table
		try:
			#creates a database for successfully sent messages
			self.cursor.execute("CREATE TABLE "+self.db_successful+ " (datestamp text, latitude real, longitude real, speed real, altitude real, message_id int)")
			#creates a database for fault sent messages
			self.cursor.execute("CREATE TABLE " +self.db_in_progress + " (datestamp text, latitude real, longitude real, speed real, altitude real, message_id int)")
		except sqlite3.OperationalError:
			self.debug("Table already exists so table will not be created")


	#{ 'date': 'datasamp'
	#  'latitude': 'double number'
	#  'longitue': 'double number'
	#  'altitude': 'double number'
	#  'speed'   : 'double number'}
	def backup(self, data, message_id=0):
		self.debug("Saving gps data to in_progress database")
		if (data is not None):
			try:
				#init string query
				string_query = ""
				#creates a template of the command
				query = Template("INSERT INTO $dbName VALUES ('$date',$latitude,$longitude,$speed,$altitude, $message_id)")
				if(message_id == 0):
					string_query = query.substitute(dbName=self.db_successful, date=data['date'] , latitude=data['latitude'], longitude=data['longitude'], speed=data['speed'],altitude=data['altitude'], message_id=message_id )
				else:
					string_query = query.substitute(dbName=self.db_in_progress, date=data['date'] , latitude=data['latitude'], longitude=data['longitude'], speed=data['speed'],altitude=data['altitude'], message_id=message_id )
				try: #tries to insert into gpslogs table
					#debug print
					self.debug("Trying to exec: ",string_query)
					self.lock.acquire()
					self.cursor.execute(string_query)#executes the query built from template
					self.connection.commit()#saves changes to local db.
					self.lock.release()
				except RuntimeError:#catch a runtime error
					self.debug('Fail during insertion of gpslogs')
			except RuntimeError:#catch a runtime error
				self.debug("Error creating the command")
		else:#param data is null
			self.debug("Param data is null")


	def move_to_successful(self,message_id):
		result = [ ]
		self.lock.acquire()
		data = self.cursor.execute("SELECT * FROM " + self.db_in_progress + " WHERE message_id = "+str(message_id))
		self.lock.release()
		data_item = data.fetchone()
		while (data_item is not None):# loop while the cursor is not empty
			query = Template("INSERT INTO $dbName VALUES ('$date',$latitude,$longitude,$speed,$altitude, $message_id)")
			string_query = query.substitute(dbName=self.db_successful, date=data_item[0] , latitude=data_item[1] , longitude=data_item[2] , speed=data_item[3] ,altitude=data_item[4] , message_id=data_item[5]  )
			self.lock.acquire()
			self.cursor.execute(string_query)#executes the query built from template
			self.cursor.execute("DELETE FROM " + self.db_in_progress + " WHERE message_id = "+str(message_id))
			self.connection.commit()#saves changes to local db.
			self.lock.release()
			# result.append(data_item)
			data_item = data.fetchone()#fetch the ext chunk of data
		# return result# retun the result


	#This function closes the data base connection.
	def close(self):
		self.debug("Close BackUp Data Base")
		try:#tries to close the data base
			self.connection.close()
		except RuntimeError:#catch an error during the last command
			self.debug("Error while closing data base connection")

	#this function returns a list of tuples, each tuple is a chunk of gps data
	def fetch_in_progress(self):
		self.debug("\n")
		result = [ ]#define a list of the data chunks
		data_Failed = self.cursor.execute("SELECT * FROM "+ self.db_in_progress )#selecet just the failed data
		data_item = data_Failed.fetchone()#fetch te first chunk of data
		while (not(data_item is None)):# loop while the cursor is not empty
			data_item = data_Failed.fetchone()#fetch the ext chunk of data
			result.append(data_item)# append to the result
		return result# retun the result

	#this function returns a list of tuples, each tuple is a chunk of failed gps data
	def fetch_successful(self):
		print("\n")
		result = [ ]#define a list of the data chunks
		data_succeded = self.cursor.execute("SELECT * FROM "+self.db_successful)#selecet just the succeded data
		data_item = data_succeded.fetchone()#fetch te first chunk of data
		while (data_item is not None):# loop while the cursor is not empty
			data_item = data_succeded.fetchone()#fetch the ext chunk of data
			result.append(data_item)# append to the result
		return result# retun the result

	#this function cleans the data from GPS_LOG table
	def clean_successful (self):
		#delete string query
		string_query = "DELETE FROM " +self.db_successful
		try:
			self.cursor.execute(string_query)#executes the query built from string
			self.connection.commit()#saves changes to local db.
		except RuntimeError:
			self.debug("Error during deletion of data base")

	#this function cleans the data from GPS_FAILED_DATA
	def clean_in_progress (self):
		#delete string query
		string_query = "DELETE FROM " +self.db_in_progress
		try:
			self.cursor.execute(string_query)#executes the query built from string
			self.connection.commit()#saves changes to local db.
		except RuntimeError:
			self.debug("Error during deletion of data base")

	#close the data base
	def closeLogger(self):
		try:#tries to close the connection to the data base.
			self.connection.close()
		except RuntimeError:
			#manages the error
			self.debug("Failed to close the database")

	def debug(self, *params):
		if(__debug__):
			for param in params:
				print(param, end=' ')
			print("")
