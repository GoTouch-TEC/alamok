
import sqlite3
from string import Template
import threading #MultiThreading
class SQL_Lite_Logger:

	def __init__(self, filename):
		self.connection = sqlite3.connect(filename, check_same_thread = False)
		self.cursor = self.connection.cursor()
		self.db_in_progress ="in_progress"
		self.db_successful="sended"
		self.db_failed="failed"
		self.lock = threading.Lock()
		try:
			self.cursor.execute("CREATE TABLE " + self.db_successful+ " (datestamp text, latitude real, longitude real, speed real, altitude real, message_id int)")
			self.cursor.execute("CREATE TABLE " + self.db_in_progress + " (datestamp text, latitude real, longitude real, speed real, altitude real, message_id int)")
			self.cursor.execute("CREATE TABLE " + self.db_failed + " (datestamp text, latitude real, longitude real, speed real, altitude real, message_id int)")

		except sqlite3.OperationalError:
			self.debug("Table already exists so table will not be created")
		self.move_to_failed()

	#{ 'date': 'datasamp'
	#  'latitude': 'double number'
	#  'longitue': 'double number'
	#  'altitude': 'double number'
	#  'speed'   : 'double number'}
	def backup(self, data, message_id=0):
		self.debug("Saving gps data to in_progress database")
		if (data is not None):
			try:
				string_query = ""
				query = Template("INSERT INTO $dbName VALUES ('$date',$latitude,$longitude,$speed,$altitude, $message_id)")
				if(message_id == 0):
					string_query = query.substitute(dbName=self.db_successful, date=data['date'] , latitude=data['latitude'], longitude=data['longitude'], speed=data['speed'],altitude=data['altitude'], message_id=message_id )
				else:
					string_query = query.substitute(dbName=self.db_in_progress, date=data['date'] , latitude=data['latitude'], longitude=data['longitude'], speed=data['speed'],altitude=data['altitude'], message_id=message_id )
				try:
					self.debug("Trying to exec: ",string_query)
					self.lock.acquire()
					self.cursor.execute(string_query)
					self.connection.commit()
					self.lock.release()
				except RuntimeError:
					self.debug('Fail during insertion of gpslogs')
			except RuntimeError:
				self.debug("Error creating the command")
		else:
			self.debug("Param data is null")

	def move_to_successful(self,message_id):
		result = [ ]
		self.lock.acquire()
		data = self.cursor.execute("SELECT * FROM " + self.db_in_progress + " WHERE message_id = "+str(message_id))
		self.lock.release()
		data_item = data.fetchone()
		while (data_item is not None):
			query = Template("INSERT INTO $dbName VALUES ('$date',$latitude,$longitude,$speed,$altitude, $message_id)")
			string_query = query.substitute(dbName=self.db_successful, date=data_item[0] , latitude=data_item[1] , longitude=data_item[2] , speed=data_item[3] ,altitude=data_item[4] , message_id=data_item[5]  )
			self.lock.acquire()
			self.cursor.execute(string_query)
			self.cursor.execute("DELETE FROM " + self.db_in_progress + " WHERE message_id = "+str(message_id))
			self.connection.commit()
			self.lock.release()
			data_item = data.fetchone()

	def move_to_failed(self):
		data=self.fetch_in_progress()
		print("in_progress len: ",len(data))
		self.lock.acquire()
		for data_item in data:
			query = Template("INSERT INTO $dbName VALUES ('$date',$latitude,$longitude,$speed,$altitude, $message_id)")
			string_query = query.substitute(dbName=self.db_failed, date=data_item[0] , latitude=data_item[1] , longitude=data_item[2] , speed=data_item[3] ,altitude=data_item[4] , message_id=data_item[5]  )
			self.cursor.execute(string_query)
		self.connection.commit()
		self.lock.release()
		self.clean_in_progress()

	def close(self):
		self.debug("Close BackUp Data Base")
		try:
			self.connection.close()
		except RuntimeError:
			self.debug("Error while closing data base connection")

	def fetch_in_progress(self):
		return self.fetch(self.db_in_progress)

	def fetch_successful(self):
		return self.fetch(self.db_successful)

	def fetch_failed(self):
		return self.fetch(self.db_failed)

	def fetch(self, db_name):
		result = [ ]
		self.lock.acquire()
		data_succeded = self.cursor.execute("SELECT * FROM "+db_name)
		self.lock.release()
		data_item = data_succeded.fetchone()
		while (data_item is not None):
			result.append(data_item)
			data_item = data_succeded.fetchone()
		return result

	def clean_successful(self):
		self.clean(self.db_successful)

	def clean_in_progress(self):
		self.clean(self.db_in_progress)

	def clean_failed(self):
		self.clean(self.db_failed)

	def clean(self, db_name):
		string_query = "DELETE FROM " + db_name
		try:
			self.lock.acquire()
			self.cursor.execute(string_query)
			self.connection.commit()
			self.lock.release()
		except RuntimeError:
			self.debug("Error during deletion of data base")

	def close_logger(self):
		try:
			self.connection.close()
		except RuntimeError:
			self.debug("Failed to close the database")

	def debug(self, *params):
		if(__debug__):
			for param in params:
				print(param, end=' ')
			print("")
