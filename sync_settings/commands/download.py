# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..thread_progress import ThreadProgress

class SyncSettingsDownloadCommand(WindowCommand):
  def run(self):
    def download_request():
      gist_id = SyncManager.settings('gist_id')

      if gist_id:
        try:
          api = SyncManager.gist_api()

          if api is not None:
            remote_files = api.get(gist_id).get('files')

            if len(remote_files) > 0:
              SyncManager.update_from_remote_files(remote_files)
              success_message = ''.join([
                'Files Downloaded Successfully. ',
                'Please restart Sublime Text to install all dependencies!.'
              ])
              SyncManager.show_message_and_log(success_message, False)
            else:
              SyncManager.show_message_and_log('There are not enough files to create the gist', False)
        except Exception as e:
          SyncManager.show_message_and_log(e)
      else:
        SyncManager.show_message_and_log('Set gist_id property on the configuration file', False)

    ThreadProgress(lambda: download_request(), 'Downloading files')
