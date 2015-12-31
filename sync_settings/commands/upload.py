# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..thread_progress import ThreadProgress

class SyncSettingsUploadCommand(WindowCommand):
  def run(self):
    def upload_request():
      gist_id = Manager.settings('gist_id')

      if gist_id:
        try:
          api = Manager.gist_api()

          if api is not None:
            files = Manager.get_files_content()

            if len(files) > 0:
              data = {'files': files}
              api.edit(gist_id, data)
              Manager.show_message_and_log('Your files was uploaded successfully!', False)
            else:
              Manager.show_message_and_log('There are not enough files to upload', False)
        except Exception as e:
          Manager.show_message_and_log(e)
      else:
        Manager.show_message_and_log('Set gist_id property on the configuration file', False)

    ThreadProgress(lambda: upload_request(), 'Uploading files')
