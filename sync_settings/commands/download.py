# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..sync_logger import SyncLogger
from ..thread_progress import ThreadProgress

class SyncSettingsDownloadCommand(WindowCommand):

  def __download_request(self):
    gist_id = SyncManager.settings('gist_id')

    if gist_id:
      try:
        api = SyncManager.gist_api()

        if api is not None:
          remote_files = api.get(gist_id).get('files')

          if len(remote_files):
            SyncManager.update_from_remote_files(remote_files)
            success_message = ''.join([
              'Files Downloaded Successfully. ',
              'Please restart Sublime Text to install all dependencies!.'
            ])
            SyncLogger.log(success_message, SyncLogger.LOG_LEVEL_SUCCESS)
          else:
            SyncLogger.log(
              'There are not enough files to create the gist',
              SyncLogger.LOG_LEVEL_WARNING
            )
      except Exception as e:
        SyncLogger.log(e, SyncLogger.LOG_LEVEL_ERROR)
    else:
      SyncLogger.log(
        'Set `gist_id property on the configuration file',
        SyncLogger.LOG_LEVEL_WARNING
      )

  def run(self):
    ThreadProgress(lambda: self.__download_request(), 'Downloading files')
