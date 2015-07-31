# -*- coding: utf-8 -*-

from .gistapi import *
import sublime, sys

class SyncSettingsManager:
	settingsFilename = 'SyncSettings.sublime-settings'
	gistapi = None
	files = [
		"Package Control.merged-ca-bundle",
		"Package Control.system-ca-bundle",
		"Package Control.user-ca-bundle",
		"Package Control.sublime-settings",
		"Preferences.sublime-settings",
		"Package Control.last-run"
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
			content = open(fullPath, 'r').read()
			r.update({
				f: {
					'content': content
				}
			})

		return r

	@staticmethod
	def getPackagesPath (filename = None):
		separator = SyncSettingsManager.getSeparator()
		path = sublime.packages_path() + separator + 'User'
		if not filename is None:
			return path + separator + filename

		return path + separator

	@staticmethod
	def getSettingsFilename ():
		return SyncSettingsManager.settingsFilename

	@staticmethod
	def excludeValues (l, e):
		try:
			for el in e:
				 l.remove(el)
		except Exception as e:
			pass

		return l

	@staticmethod
	def getSeparator ():
		return "\\" if sys.platform.startswith('win') else "/"
