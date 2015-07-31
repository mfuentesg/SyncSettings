# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager
from ..gistapi import Gist

class SyncSettingsDownloadCommand (WindowCommand):
	def run (self):
		gistId = SyncSettingsManager.settings('gist_id')
		if gistId:
			try:
				api = Gist(SyncSettingsManager.settings('access_token'))
				remoteFiles = api.get(gistId).get('files')
				files = SyncSettingsManager.getFiles()

				for f in files:
					fileJSON = remoteFiles.get(f)
					if fileJSON:
						fileOpened = open(SyncSettingsManager.getPackagesPath(f), 'w+')
						fileOpened.write(fileJSON.get('content'))
						fileOpened.close()
				sublime.status_message('Sync Settings: Files Downloaded Successfully')
			except Exception as e:
				sublime.status_message('Sync Settings: ' + str(e))
		else:
			sublime.status_message('Sync Settings: Set the gist_id in the configuration file')
