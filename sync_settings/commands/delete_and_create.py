# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..thread_progress import ThreadProgress

class SyncSettingsDeleteAndCreateCommand(WindowCommand):
  def run(self, create = True):
    print(create)
    if not (Manager.settings('access_token') and Manager.settings('gist_id')):
      error_msg = 'You need set the `access_token` and `gist_id` properties'
      Manager.show_message_and_log(error_msg, False)
    else:
      dialog_message = ''.join([
        'Sync Settings: \n',
        'Your Gist will be deleted, are you sure?\n',
        'This action is irreversible'
      ])

      if sublime.yes_no_cancel_dialog(dialog_message) == sublime.DIALOG_YES:
        ThreadProgress(lambda: self.delete_and_create_gist(create), 'Deleting gist')

  def delete_and_create_gist(self, create):
    gist_id = Manager.settings('gist_id')

    if gist_id:
      try:
        api = Manager.gist_api()

        if api is not None:
          api.delete(gist_id)
          Manager.settings('gist_id', '')
          Manager.show_message_and_log('Gist deleted successfully, id = %s' % (gist_id), False)
          if create:
            self.window.run_command('sync_settings_create_and_upload')
      except Exception as e:
        Manager.show_message_and_log(e)
    else:
      Manager.show_message_and_log('Set gist_id property on the configuration file', False)
