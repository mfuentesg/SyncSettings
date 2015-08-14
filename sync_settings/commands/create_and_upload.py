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
			Manager.showMessageAndLog('You need set the access token', False)

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
				Manager.showMessageAndLog('Gist created, id = ' + result.get('id'), False)
				if sublime.yes_no_cancel_dialog('Sync Settings: \nYour gist was created successfully\nDo you want update the gist_id property in the config file?') == sublime.DIALOG_YES:
					Manager.settings('gist_id', result.get('id'))
					sublime.save_settings(Manager.getSettingsFilename())
					Manager.showMessageAndLog('Gist id updated successfully!', False)
			except Exception as e:
				Manager.showMessageAndLog(e)
		else:
			Manager.showMessageAndLog('There are not enough files to create the gist', False)

	def onChange (self, text):
		pass

	def onCancel (self):
		pass
