# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist

class SyncSettingsCreateAndUploadCommand (WindowCommand):
	def run (self):
		if Manager.settings('access_token'):
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
		files = Manager.getContentFiles()

		if len(files) > 0:
			data = { 'files': files}
			if d != "": data.update({"description": d})

			try:
				result = Gist(Manager.settings('access_token')).create(data)
				sublime.status_message('Sync Settings: Gist created, id = ' + result.get('id'))
				if sublime.yes_no_cancel_dialog('Sync Settings: \nYour gist was created successfully\nDo you want update the gist_id property in the config file?') == sublime.DIALOG_YES:
					Manager.settings('gist_id', result.get('id'))
					sublime.save_settings(Manager.getSettingsFilename())
					sublime.status_message('Sync Settings: Gist id updated successfully!')
			except Exception as e:
				sublime.status_message(str(e))
		else:
			sublime.status_message('Sync Settings: There are not enough files to create the gist')

	def onChange (self, text):
		pass

	def onCancel (self):
		pass
