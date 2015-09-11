# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist
from ..thread_progress import ThreadProgress

class SyncSettingsDownloadCommand (WindowCommand):
  def run (self):
    def processDownloadRequest ():
      gistId = Manager.settings('gist_id')
      if gistId:
        try:
          api = Gist(Manager.settings('access_token'))
          remoteFiles = api.get(gistId).get('files')
          files = Manager.getFiles()

          if len(files) > 0:
            for f in files:
              fileJSON = remoteFiles.get(f)
              if not fileJSON is None:
                 fileOpened = open(Manager.getPackagesPath(f), 'w+')
                 fileOpened.write(fileJSON.get('content'))
                 fileOpened.close()
          else:
            Manager.showMessageAndLog('There are not enough files to create the gist', False)
        except Exception as e:
          Manager.showMessageAndLog(e)
      else:
        Manager.showMessageAndLog('Set the gist_id in the configuration file', False)
    success_message = 'Files Downloaded Successfully. Please restart Sublime Text to install all dependencies!.'
    ThreadProgress(
      lambda: processDownloadRequest(),
      'Downloading files',
      success_message
    )
