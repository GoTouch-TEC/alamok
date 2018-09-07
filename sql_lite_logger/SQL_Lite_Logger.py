import sqlite3
from string import Template
import threading #MultiThreading


# 1: successful
# 2: in_progress
# 3: failed


class SQL_Lite_Logger:

	def __init__(self, filename):
		self.connection = sqlite3.connect(filename, check_same_thread = False)
		self.cursor = self.connection.cursor()
		self.db_locations = "locations"
		self.lock = threading.Lock()

		try:
			self.cursor.execute('''CREATE TABLE {db} (datestamp text, latitude real, longitude real, speed real, altitude real, message_id int, status int) PRIMARY KEY(datestamp) '''.format(db=self.db_locations))

		except sqlite3.OperationalError:
			print("Table already exists so table will not be created")
			self.move_to_failed()

	#{ 'date': 'datasamp'
	#  'latitude': 'double number'
	#  'longitue': 'double number'
	#  'altitude': 'double number'
	#  'speed'   : 'double number'}
	def backup(self, data, message_id=0):
		if (data is not None):
			sql = 		''' INSERT INTO projects(datestamp, latitude, longitue, speed, altitude, message_id, status)
						VALUES(?, ?, ?, ?, ?, ?, ?) '''
			self.lock.acquire()
			self.cursor.execute(sql, (data['date'], data['latitude'], data['longitude'], data['speed'], data['altitude'], message_id, 2) )
			self.connection.commit()
			self.lock.release()
		else:
			self.debug("Param data is null")

	def move_to_successful(self,message_id):
		sql = ''' UPDATE tasks SET status = ? WHERE message_id = ?'''
		self.lock.acquire()
		self.cursor.execute(sql, (1, message_id))
		self.connection.commit()
		self.lock.release()

	def move_to_failed(self, elapsed_time=0):
		sql = ''' UPDATE tasks SET status = ? WHERE status = ?'''
		self.lock.acquire()
		self.cursor.execute(sql, (0, 3))
		self.connection.commit()
		self.lock.release()


	def close(self):
		print("Close BackUp Data Base")
		try:
			self.connection.close()
		except RuntimeError:
			print"Error while closing data base connection")

	def fetch_in_progress(self):
		return self.fetch(2)

	def fetch_successful(self):
		return self.fetch(1)

	def fetch_failed(self):
		return self.fetch(3)

	def fetch(self, status):
		self.lock.acquire()
		self.cursor.execute('''SELECT * FROM locations WHERE status=?''', (status,))
		data = self.cursor.fetchall()
		self.lock.release()
		data_item = data_succeded.fetchone()
		while (data_item is not None):
			result.append(data_item)
			data_item = data_succeded.fetchone()
		return result


	# def fetch_by_elapsed_time(self, db_name,elapsed_time=0):
	# 	result = [ ]
	# 	self.lock.acquire()
	#
	# 	data_succeded = self.cursor.execute('''SELECT * FROM {db} WHERE datestamp < datetime('now', '-{seconds} seconds')'''.format(db=db_name, seconds=elapsed_time))
	#
	# 	self.lock.release()
	# 	data_item = data_succeded.fetchone()
	# 	while (data_item is not None):
	# 		result.append(data_item)
	# 		data_item = data_succeded.fetchone()
	# 	return result

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
			print("Error during deletion of data base")

	def clean_by_elapsed_time(self, db_name, elapsed_time=0):
		try:
			self.lock.acquire()
			self.cursor.execute('''DELETE FROM {db} WHERE datestamp < datetime('now', '-{seconds} seconds') '''.format(db=db_name, seconds=elapsed_time))
			self.connection.commit()
			self.lock.release()
		except RuntimeError:
			print("Error during deletion of data base")

	def close_logger(self):
		try:
			self.connection.close()
		except RuntimeError:
			print("Failed to close the database")
