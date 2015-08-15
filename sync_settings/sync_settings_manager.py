# -*- coding: utf-8 -*-

import sublime, os
from .logger import Logger

class SyncSettingsManager:
	settingsFilename = 'SyncSettings.sublime-settings'
	files = [
		"Package Control.merged-ca-bundle",
		"Package Control.system-ca-bundle",
		"Package Control.user-ca-bundle",
		"Package Control.sublime-settings",
		"Preferences.sublime-settings",
		"Package Control.last-run",
		"Default (OSX).sublime-keymap",
		"Default (Windows).sublime-keymap",
		"Default (Linux).sublime-keymap"
	]

	@staticmethod
	def settings (key = None, newValue = None):
		settings =  sublime.load_settings(SyncSettingsManager.settingsFilename)
		if not key is None and not newValue is None:
			settings.set(key, newValue)
		elif not key is None and newValue is None:
			return settings.get(key)
		else:
			return settings

	@staticmethod
	def getFiles ():
		excludedFiles = SyncSettingsManager.settings('excluded_files')
		return SyncSettingsManager.excludeValues(SyncSettingsManager.files, excludedFiles)

	@staticmethod
	def getContentFiles ():
		r = {}
		for f in SyncSettingsManager.getFiles():
			fullPath = SyncSettingsManager.getPackagesPath(f)
			if os.path.isfile(fullPath) and os.path.exists(fullPath):
				try:
					content = open(fullPath, 'r').read()
					r.update({
						f: {
							'content': content
						}
					})
				except Exception as e:
					Logger.log(str(e), Logger.MESSAGE_ERROR_TYPE)
		return r

	@staticmethod
	def getPackagesPath (filename = None):
		path = os.path.join(sublime.packages_path(), 'User')
		if not filename is None:
			return os.path.join(path, filename)
		return path

	@staticmethod
	def getSettingsFilename ():
		return SyncSettingsManager.settingsFilename

	@staticmethod
	def excludeValues (l, e):
		try:
			for el in e:
				l.remove(el)
		except Exception as e:
			Logger.log(str(e), Logger.MESSAGE_ERROR_TYPE)

		return l

	@staticmethod
	def showMessageAndLog (message, error = True):
		m = l = ''
		if isinstance(message, Exception):
			message = message.toJSON()
			m = message.get('app_message')
			l = message.get('error_description')+ ', File: ' + message.get('filename') +' - Line: ' + message.get('line')
		elif isinstance(message, str):
			m = l = message

		sublime.status_message('Sync Settings: ' + m)
		Logger.log(l, Logger.MESSAGE_ERROR_TYPE if error else Logger.MESSAGE_INFO_TYPE)
