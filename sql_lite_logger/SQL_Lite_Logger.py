import sqlite3
from string import Template
# import threading #MultiThreading


# 1: successful
# 2: in_progress
# 3: failed

class SQL_Lite_Logger:

	def __init__(self, filename):
		self.connection = sqlite3.connect(filename)
		self.connection.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)]) # return every roy as a dictionaty
		# self.cursor = self.connection.cursor()
		self.locations_table = "locations"

		try:
			sql = '''CREATE TABLE locations (date text, latitude real, longitude real, speed real, altitude real, status int, PRIMARY KEY(date)) '''
			cursor = self.connection.cursor()
			cursor.execute(sql)

		except sqlite3.OperationalError:
			print("Table already exists so table will not be created")
		self.connection.commit()

		self.mark_as_failed()

	#{ 'date': 'string'
	#  'latitude': 'double number'
	#  'longitude': 'double number'
	#  'altitude': 'double number'
	#  'speed'   : 'double number'}
	def backup(self, data):
		if (data is not None):
			# data["message_id"]=message_id
			sql = 		''' INSERT INTO locations (date, latitude, longitude, speed, altitude, status)
						VALUES(:date, :latitude, :longitude, :speed, :altitude, :status) '''
			cursor = self.connection.cursor()
			cursor.execute(sql,data)
			self.connection.commit()
		else:
			self.debug("Param data is null")

	def mark_as_successful(self, dates):
		task = []
		for date in dates:
			task.append(	(1,date)	)
		sql = ''' UPDATE locations SET status = ? WHERE date = ?'''
		cursor = self.connection.cursor()
		cursor.executemany(sql, task)
		self.connection.commit()

	def mark_as_failed(self):
		sql = ''' UPDATE locations SET status = ? WHERE status = ?'''
		cursor = self.connection.cursor()
		cursor.execute(sql, (3, 2))
		self.connection.commit()

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
		cursor = self.connection.cursor()
		cursor.execute('''SELECT * FROM locations WHERE status=?''', (status,))
		data = cursor.fetchall()
		return data

	def clear(self):
			sql = "DROP TABLE locations"
			try:
				cursor = self.connection.cursor()
				cursor.execute(sql)
				self.connection.commit()
			except RuntimeError:
				print("Error during deletion of data base")
	def close_logger(self):
		try:
			self.connection.close()
		except RuntimeError:
			print("Failed to close the database")
