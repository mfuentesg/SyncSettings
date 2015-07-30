# -*- coding: utf-8 -*-

from .gistapi import Gist
from .utils import *
import sublime

class SyncSettingsManager:
	settingsFilename = 'SyncSettings.sublime-settings'
	gistapi = None
	files = [
		"Package Control.merged-ca-bundle",
		"Package Control.sublime-settings",
		"Package Control.system-ca-bundle",
		"Package Control.user-ca-bundle",
		"Preferences.sublime-settings",
		"Package Control.last-run"
	]

	@staticmethod
	def settings(key = None, newValue = None):
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
		return excludeValues(SyncSettingsManager.files, excludedFiles)

	@staticmethod
	def getPackagesPath (filename = None):
		path = sublime.packages_path() + getSeparator() + 'User'
		if not filename is None:
			return path + getSeparator() + filename

		return path + getSeparator()

	@staticmethod
	def getSettingsFilename ():
		return SyncSettingsManager.settingsFilename

	@staticmethod
	def gistapi ():
		try:
			SyncSettingsManager.gistapi = Gist(SyncSettingsManager.settings('access_token'))
			sublime.status_message('Sync Settings: Token Accepted')
			return SyncSettingsManager.gistapi
		except Exception as e:
			sublime.status_message('Sync Settings: ' + str(e))
