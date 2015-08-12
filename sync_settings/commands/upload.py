# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist

class SyncSettingsUploadCommand (WindowCommand):
	def run (self):
		gistId = Manager.settings('gist_id')
		if gistId:
			try:
				api = Gist(Manager.settings('access_token'))
				files = Manager.getContentFiles()
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
