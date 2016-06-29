# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..sync_logger import SyncLogger
from ..thread_progress import ThreadProgress

class SyncSettingsDeleteAndCreateCommand(WindowCommand):
  def run(self, create = True):
    if not (SyncManager.settings('access_token') and SyncManager.settings('gist_id')):
      SyncLogger.log(
        'You need set the `access_token` and `gist_id` properties',
        SyncLogger.LOG_LEVEL_WARNING
      )
    else:
      dialog_message = ''.join([
        'Sync Settings:\n',
        'Your Gist will be deleted, are you sure?\n',
        'Warning: This action is irreversible'
      ])

      if sublime.yes_no_cancel_dialog(dialog_message) == sublime.DIALOG_YES:
        ThreadProgress(lambda: self.__delete_and_create_gist(create), 'Deleting gist')

  def __delete_and_create_gist(self, create):
    gist_id = SyncManager.settings('gist_id')

    if gist_id:
      try:
        api = SyncManager.gist_api()

        if api is not None:
          api.delete(gist_id)

          SyncManager.settings('gist_id', '')
          SyncLogger.log(
            'Gist deleted successfully, id = %s' % (gist_id),
            SyncLogger.LOG_LEVEL_SUCCESS
          )

          if create:
            self.window.run_command('sync_settings_create_and_upload')

      except Exception as e:
        SyncLogger.log(e, SyncLogger.LOG_LEVEL_ERROR)
    else:
      SyncLogger.log(
        'Set `gist_id` property on the configuration file',
        SyncLogger.LOG_LEVEL_WARNING
      )
