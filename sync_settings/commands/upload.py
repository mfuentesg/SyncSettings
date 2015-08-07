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
				files = SyncSettingsManager.getContentFiles()
				if len(files) > 0:
					data = { 'files': files}
					api.edit(gistId, data)
					sublime.status_message('Sync Settings: Your files was uploaded successfully!')
				else:
					sublime.status_message('Sync Settings: There are not enough files to upload')
			except Exception as e:
				sublime.status_message('Sync Settings: ' + str(e))
		else:
			sublime.status_message('Sync Settings: Set the gist_id in the configuration file')
