# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist
from ..thread_progress import ThreadProgress

class SyncSettingsUploadCommand (WindowCommand):
  def run (self):
    def upload_request ():
      gistId = Manager.settings('gist_id')
      if gistId:
        try:
          api = Gist(Manager.settings('access_token'))
          files = Manager.getContentFiles()
          if len(files) > 0:
            data = { 'files': files}
            api.edit(gistId, data)
          else:
            Manager.showMessageAndLog('There are not enough files to upload', False)
        except Exception as e:
          Manager.showMessageAndLog(e)
      else:
        Manager.showMessageAndLog('Set the gist_id in the configuration file', False)
    ThreadProgress(
      lambda: upload_request(),
      'Uploading files',
      'Your files was uploaded successfully!'
    )
