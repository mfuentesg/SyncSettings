import os, time

class Logger:
	FILE_NAME = '.sync-settings.log'
	MESSAGE_INFO_TYPE = 1
	MESSAGE_ERROR_TYPE = 2

	@staticmethod
	def log (message, type):
		if type == Logger.MESSAGE_ERROR_TYPE:
			message = 'ERROR: ' + message
		elif type == Logger.MESSAGE_INFO_TYPE:
			message = 'INFO: ' + message
		Logger.write(message)

	@staticmethod
	def getPath ():
		return os.path.join(os.path.expanduser('~'), Logger.FILE_NAME)

	@staticmethod
	def write (message):
		fullTime = time.strftime("[%d/%m/%Y - %H:%M:%S] ")
		message = fullTime + message
		path = Logger.getPath()
		action = 'a+' if os.path.exists(path) else 'w+'

		try:
			with open(path, action) as f:
				f.write(message + '\n')
				f.close()
		except Exception as e:
			print(e)