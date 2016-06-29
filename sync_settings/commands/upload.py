# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_manager import SyncManager
from ..thread_progress import ThreadProgress

class SyncSettingsUploadCommand(WindowCommand):
  def run(self):
    def upload_request():
      gist_id = SyncManager.settings('gist_id')

      if gist_id:
        try:
          api = SyncManager.gist_api()

          if api is not None:
            files = SyncManager.get_files_content()

            if len(files) > 0:
              data = {'files': files}
              api.edit(gist_id, data)
              SyncManager.show_message_and_log('Your files was uploaded successfully!', False)
            else:
              SyncManager.show_message_and_log('There are not enough files to upload', False)
        except Exception as e:
          SyncManager.show_message_and_log(e)
      else:
        SyncManager.show_message_and_log('Set gist_id property on the configuration file', False)

    ThreadProgress(lambda: upload_request(), 'Uploading files')
