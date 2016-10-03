# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..sync_logger import SyncLogger
from ..sync_version import SyncVersion
from ..thread_progress import ThreadProgress

class SyncSettingsDownloadCommand(WindowCommand):

  def __download_request(self):
    gist_id = SyncManager.settings('gist_id')

    if gist_id:
      try:
        api = SyncManager.gist_api()

        if api is not None:
          gist_content = api.get(gist_id)
          remote_files = gist_content.get('files')

          if len(remote_files):
            # Excluding SyncSettings.sublime-settings
            remote_files.pop(SyncManager.get_settings_filename(), None)

            SyncManager.update_from_remote_files(remote_files)
            success_message = ''.join([
              'Your settings were upgraded correctly, ',
              'restart ST to complete the upgrade.',
            ])
            SyncLogger.log(success_message, SyncLogger.LOG_LEVEL_SUCCESS)
            SyncVersion.upgrade(gist_content)
          else:
            SyncLogger.log(
              'There are not enough files to create the backup.',
              SyncLogger.LOG_LEVEL_WARNING
            )
      except Exception as ex:
        SyncLogger.log(ex, SyncLogger.LOG_LEVEL_ERROR)

    else:
      SyncLogger.log(
        'Set `gist_id` property on the configuration file',
        SyncLogger.LOG_LEVEL_WARNING
      )

  def run(self):
    ThreadProgress(lambda: self.__download_request(), 'Downloading the latest version')
