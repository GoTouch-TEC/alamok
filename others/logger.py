import datetime
class Logger:

	def __init__(self):
		#get the current time.
		self.new_name_file = str(datetime.datetime.now())
		self.new_name_file = self.new_name_file.replace(' ','T')#Setting ISO name fiel
		self.new_name_file += 'Z' # append to the end
		# try to create and open a new file.
		self.log_file = open(self.new_name_file,'w')# open a new file to store the data.
		
	def backUp (self,data):	
		self.log_file.write(data)

	def closeBackUp (self):
		self.log_file.close()