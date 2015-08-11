import os, time

class Logger:
	FILE_NAME = '.sync-settings.log'
	MESSAGE_ERROR_TYPE = 1
	MESSAGE_INFO_TYPE = 1

	@staticmethod
	def log (message, type = None):
		if not type is None:
			pass

	@staticmethod
	def getPath ():
		return os.path.expanduser('~', Logger.FILE_NAME)

	@staticmethod
	def write (message):
		fullTime = time.strftime("[%d/%m/%Y - %H:%M:%S] ")
		message = fullTime + message
