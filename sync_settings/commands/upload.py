# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager
from ..gistapi import Gist

class SyncSettingsUploadCommand (WindowCommand):
	def run (self):
		gistId = SyncSettingsManager.settings('gist_id')
		if gistId:
			try:
				api = Gist(SyncSettingsManager.settings('access_token'))
				data = {'files': SyncSettingsManager.getContentFiles() }
				print(data)
				api.edit(gistId, data)
				sublime.status_message('Sync Settings: Your files was uploaded successfully!')
			except Exception as e:
				sublime.status_message('Sync Settings: ' + str(e))
		else:
			sublime.status_message('Sync Settings: Set the gist_id in the configuration file')
