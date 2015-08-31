# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..sync_settings_manager import SyncSettingsManager as Manager
from ..gistapi import Gist

class SyncSettingsDownloadCommand (WindowCommand):
  def run (self):
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
          sublime.message_dialog('Sync Settings: Files Downloaded Successfully\nNow you need restart Sublime Text for Package Control installs all dependencies!')
          Manager.showMessageAndLog('Files Downloaded Successfully', False)
        else:
          Manager.showMessageAndLog('There are not enough files to create the gist', False)
      except Exception as e:
        Manager.showMessageAndLog(e)
    else:
      Manager.showMessageAndLog('Set the gist_id in the configuration file', False)
