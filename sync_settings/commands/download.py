# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist
from ..thread_progress import ThreadProgress

class SyncSettingsDownloadCommand(WindowCommand):
  def run(self):
    def download_request():
      gist_id = Manager.settings('gist_id')
      if gist_id:
        try:
          api = Gist(Manager.settings('access_token'))
          remote_files = api.get(gist_id).get('files')
          files = Manager.get_files()

          if len(files) > 0:
            for f in files:
              file_json = remote_files.get(f)
              if not file_json is None:
                 opened_file = open(Manager.get_packages_path(f), 'w+')
                 opened_file.write(file_json.get('content'))
                 opened_file.close()
          else:
            Manager.show_message_and_log('There are not enough files to create the gist', False)
        except Exception as e:
          Manager.show_message_and_log(e)
      else:
        Manager.show_message_and_log('Set the gist_id in the configuration file', False)
    success_message = 'Files Downloaded Successfully. Please restart Sublime Text to install all dependencies!.'
    ThreadProgress(
      lambda: download_request(),
      'Downloading files',
      success_message
    )
