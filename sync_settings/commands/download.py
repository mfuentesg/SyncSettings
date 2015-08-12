# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist

class SyncSettingsDownloadCommand (WindowCommand):
	def run (self):
		gistId = Manager.settings('gist_id')
		if gistId:
			try:
				api = Gist(Manager.settings('access_token'))
				remoteFiles = api.get(gistId).get('files')
				files = Manager.getFiles()

				if len(files) > 0:
					for f in files:
						fileJSON = remoteFiles.get(f)
						if not fileJSON is None:
						 	fileOpened = open(Manager.getPackagesPath(f), 'w+')
						 	fileOpened.write(fileJSON.get('content'))
						 	fileOpened.close()
					sublime.message_dialog('Sync Settings: Files Downloaded Successfully\nNow you need restart Sublime Text for Package Control installs all dependencies!')
					sublime.status_message('Sync Settings: Files Downloaded Successfully')
				else:
					sublime.status_message('Sync Settings: There are not enough files to create the gist')
			except Exception as e:
				sublime.status_message('Sync Settings: ' + str(e))
		else:
			sublime.status_message('Sync Settings: Set the gist_id in the configuration file')
