import sublime, os
from sublime_plugin import WindowCommand
from ..logger import Logger

class SyncSettingsOpenLogsCommand (WindowCommand):
	def run (self):
		path = Logger.getPath()
		if not os.path.exists(path):
			Logger.createEmptyFile()
		sublime.active_window().open_file(Logger.getPath())
