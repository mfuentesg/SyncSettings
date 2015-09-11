# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist
from ..thread_progress import ThreadProgress

class SyncSettingsCreateAndUploadCommand(WindowCommand):
  def run(self):
    if Manager.settings('access_token'):
      return sublime.set_timeout(self.show_input_panel, 10)
    else:
      Manager.show_message_and_log('You need set the access token', False)

  def show_input_panel(self):
    self.window.show_input_panel(
      'Sync Settings: Input Gist description', '', self.on_done, None, None
    )

  def on_done(self, description):
    def create_and_upload_request():
      d = description if description != "" else ""
      files = Manager.get_files_content()

      if len(files) > 0:
        data = {'files': files}
        if d != "": data.update({"description": d})

        try:
          result = Gist(Manager.settings('access_token')).create(data)
          Manager.show_message_and_log('Gist created, id = ' + result.get('id'), False)
          dialog_message = ''.join([
            'Sync Settings: \n',
            'Your gist was created successfully\n',
            'Do you want update the gist_id property in the configuration file?'
          ])

          if sublime.yes_no_cancel_dialog(dialog_message) == sublime.DIALOG_YES:
            Manager.settings('gist_id', result.get('id'))
            sublime.save_settings(Manager.get_settings_filename())
            Manager.show_message_and_log('Gist id updated successfully!', False)
        except Exception as e:
          Manager.show_message_and_log(e)
      else:
        Manager.show_message_and_log('There are not enough files to create the gist', False)

    ThreadProgress(lambda: create_and_upload_request(),'Creating and uploading files')
