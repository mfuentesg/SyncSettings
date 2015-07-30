# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager

class SyncSettingsDownloadCommand (WindowCommand):
	def run (self):
		gistId = SyncSettingsManager.settings('gist_id')
		if gistId:
			files = SyncSettingsManager.gistapi().get(gistId).get('files', {})
			print(SyncSettingsManager.gistapi())
		else:
			sublime.status_message('Sync Settings: Set the gist_id in the configuration file')
