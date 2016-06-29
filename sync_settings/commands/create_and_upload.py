# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..sync_logger import SyncLogger
from ..sync_version import SyncVersion
from ..thread_progress import ThreadProgress

class SyncSettingsCreateAndUploadCommand(WindowCommand):
  def run(self):
    if SyncManager.settings('access_token'):
      return sublime.set_timeout(self.show_input_panel, 10)
    else:
      SyncLogger.log(
        'Your `access_token` property it is not configured',
        SyncLogger.LOG_LEVEL_WARNING
      )

  def show_input_panel(self):
    self.window.show_input_panel(
      caption='Sync Settings: Enter description',
      initial_text='',
      on_done=self.on_done,
      on_change=None,
      on_cancel=None
    )

  def __create_and_upload_request(self, description):
    d = description if description != '' else ''
    files = SyncManager.get_files_content()

    if len(files):
      try:
        data = {'files': files}
        api = SyncManager.gist_api()

        if d != '': data.update({'description': d})
        if api is not None:
          gist_data = api.create(data)
          dialog_message = ''.join([
            'Sync Settings:\n\n',
            'Do you want overwrite the current `gist_id` property?'
          ])

          if sublime.yes_no_cancel_dialog(dialog_message) == sublime.DIALOG_YES:
            SyncManager.settings('gist_id', gist_data.get('id')).save_settings()
            SyncVersion.upgrade(gist_data)

          SyncLogger.log('Your settings were correctly backed', SyncLogger.LOG_LEVEL_SUCCESS)

      except Exception as e:
        SyncLogger.log(e, SyncLogger.LOG_LEVEL_ERROR)
    else:
      SyncLogger.log(
        'There are not enough files to create a backup',
        SyncLogger.LOG_LEVEL_WARNING
      )

  def on_done(self, description):
    ThreadProgress(
      lambda: self.__create_and_upload_request(description),
      'Creating and uploading files'
    )
