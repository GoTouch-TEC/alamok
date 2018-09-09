import sqlite3
from string import Template
import threading #MultiThreading


# 1: successful
# 2: in_progress
# 3: failed


class SQL_Lite_Logger:

	def __init__(self, filename):
		self.connection = sqlite3.connect(filename, check_same_thread = False)
		self.connection.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)]) # return every roy as a dictionaty
		self.cursor = self.connection.cursor()
		self.locations_table = "locations"
		self.lock = threading.Lock()

		try:
			sql = '''CREATE TABLE locations (datestamp text, latitude real, longitude real, speed real, altitude real, message_id int, status int, PRIMARY KEY(datestamp)) '''
			self.cursor.execute(sql)

		except sqlite3.OperationalError:
			print("Table already exists so table will not be created")
			self.move_to_failed()

	#{ 'datestamp': 'string'
	#  'latitude': 'double number'
	#  'longitude': 'double number'
	#  'altitude': 'double number'
	#  'speed'   : 'double number'}
	def backup(self, data, message_id=0):
		if (data is not None):
			data["status"]=2
			data["message_id"]=message_id
			sql = 		''' INSERT INTO locations (datestamp, latitude, longitude, speed, altitude, message_id, status)
						VALUES(:datestamp, :latitude, :longitude, :speed, :altitude, :message_id, :status) '''
			self.lock.acquire()
			self.cursor.execute(sql,data)
			self.connection.commit()
			self.lock.release()
		else:
			self.debug("Param data is null")

	def move_to_successful(self,message_id):
		sql = ''' UPDATE locations SET status = ? WHERE message_id = ?'''
		self.lock.acquire()
		self.cursor.execute(sql, (1, message_id))
		self.connection.commit()
		self.lock.release()

	def move_to_failed(self):
		sql = ''' UPDATE locations SET status = ? WHERE status = ?'''
		self.lock.acquire()
		self.cursor.execute(sql, (2, 3))
		self.connection.commit()
		self.lock.release()

	def close(self):
		print("Close BackUp Data Base")
		try:
			self.connection.close()
		except RuntimeError:
			print("Error while closing data base connection")

	def fetch_in_progress(self):
		return self.fetch(2)

	def fetch_successful(self):
		return self.fetch(1)

	def fetch_failed(self):
		return self.fetch(3)

	def fetch(self, status):
		result = []
		self.lock.acquire()
		self.cursor.execute('''SELECT * FROM locations WHERE status=?''', (status,))
		data = self.cursor.fetchall()
		self.lock.release()
		return data

	def clear(self):
			sql = "DROP TABLE locations"
			try:
				self.lock.acquire()
				self.cursor.execute(sql)
				self.connection.commit()
				self.lock.release()
			except RuntimeError:
				print("Error during deletion of data base")
	def close_logger(self):
		try:
			self.connection.close()
		except RuntimeError:
			print("Failed to close the database")
