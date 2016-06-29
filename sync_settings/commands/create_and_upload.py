# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..thread_progress import ThreadProgress

class SyncSettingsCreateAndUploadCommand(WindowCommand):
  def run(self):
    if SyncManager.settings('access_token'):
      return sublime.set_timeout(self.show_input_panel, 10)
    else:
      SyncManager.show_message_and_log('You need set the access token', False)

  def show_input_panel(self):
    self.window.show_input_panel(
      'Sync Settings: Input Gist description', '', self.on_done, None, None
    )

  def on_done(self, description):
    def create_and_upload_request():
      d = description if description != '' else ''
      files = SyncManager.get_files_content()

      if len(files) > 0:
        try:
          data = {'files': files}
          api = SyncManager.gist_api()

          if d != '': data.update({'description': d})
          if api is not None:
            result = api.create(data)
            dialog_message = ''.join([
              'Sync Settings: \n',
              'Your gist was created successfully\n',
              'Do you want update the gist_id property in the configuration file?'
            ])

            SyncManager.show_message_and_log('Gist created, id = ' + result.get('id'), False)
            if sublime.yes_no_cancel_dialog(dialog_message) == sublime.DIALOG_YES:
              SyncManager.settings('gist_id', result.get('id'))
              sublime.save_settings(SyncManager.get_settings_filename())
              SyncManager.show_message_and_log('Gist id updated successfully!', False)
        except Exception as e:
          SyncManager.show_message_and_log(e)
      else:
        SyncManager.show_message_and_log('There are not enough files to create the gist', False)

    ThreadProgress(lambda: create_and_upload_request(), 'Creating and uploading files')
