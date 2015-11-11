# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..thread_progress import ThreadProgress
from ..libs.gistapi import Gist

class SyncSettingsDownloadCommand(WindowCommand):
  def run(self):
    def download_request():
      gist_id = Manager.settings('gist_id')

      if gist_id:
        try:
          api = Gist(Manager.settings('access_token'))
          remote_files = api.get(gist_id).get('files')

          if len(remote_files) > 0:
            Manager.update_from_remote_files(remote_files)
            success_message = ''.join([
              'Files Downloaded Successfully. ',
              'Please restart Sublime Text to install all dependencies!.'
            ])
            Manager.show_message_and_log(success_message, False)
          else:
            Manager.show_message_and_log('There are not enough files to create the gist', False)
        except Exception as e:
          Manager.show_message_and_log(e)
      else:
        Manager.show_message_and_log('Set the gist_id in the configuration file', False)

    ThreadProgress(lambda: download_request(),'Downloading files')
