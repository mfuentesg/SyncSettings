# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..sync_logger import SyncLogger
from ..sync_version import SyncVersion
from ..thread_progress import ThreadProgress

class SyncSettingsUploadCommand(WindowCommand):

  def __upload_request(self):
    gist_id = SyncManager.settings('gist_id')

    if gist_id:
      try:
        api = SyncManager.gist_api()

        if api is not None:
          files = SyncManager.get_files_content()
          # Excluding SyncSettings.sublime-settings
          files.pop(SyncManager.get_settings_filename(), None)

          if len(files):
            data = {'files': files}
            gist_data = api.edit(gist_id, data)

            SyncLogger.log(
              'Your files were uploaded correctly',
              SyncLogger.LOG_LEVEL_SUCCESS
            )
            SyncVersion.upgrade(gist_data)
          else:
            SyncLogger.log(
              'There are not enough files to upload',
              SyncLogger.LOG_LEVEL_WARNING
            )
      except Exception as e:
        SyncLogger.log(e, SyncLogger.LOG_LEVEL_ERROR)

    else:
      SyncLogger.log(
        'Set `gist_id` property on the configuration file',
        SyncLogger.LOG_LEVEL_WARNING
      )

  def run(self):
    ThreadProgress(lambda: self.__upload_request(), 'Uploading files')
