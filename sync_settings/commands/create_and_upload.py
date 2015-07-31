# -*- coding: utf-8 -*-

import sublime, json
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager
from ..gistapi import Gist

class SyncSettingsCreateAndUploadCommand (WindowCommand):
	def run (self):
		if SyncSettingsManager.settings('access_token'):
			return sublime.set_timeout(self.showInputPanel, 10)
		else:
			sublime.status_message('Sync Settings: You need set your access token')

	def showInputPanel (self):
		self.window.show_input_panel(
			'Sync Settings: Input Gist description',
			'',
			self.onDone,
			self.onChange,
			self.onCancel
		)

	def onDone (self, description):
		d = description if description != "" else ""
		data = {
			'files': SyncSettingsManager.getContentFiles()
		}
		if d != "": data.update({"description": d})

		try:
			result = Gist(SyncSettingsManager.settings('access_token')).create(data)
			sublime.status_message('Sync Settings: Gist created, id = ' + result.get('id'))
			if sublime.yes_no_cancel_dialog('Sync Settings: \nYour gist was created successfully\nDo you want update the gist_id property in the config file?') == sublime.DIALOG_YES:
				SyncSettingsManager.settings('gist_id', result.get('id'))
				sublime.save_settings(SyncSettingsManager.getSettingsFilename())
				sublime.status_message('Sync Settings: Gist id updated successfully!')
		except Exception as e:
			sublime.status_message(str(e))

	def onChange (self, text):
		pass

	def onCancel (self):
		pass
