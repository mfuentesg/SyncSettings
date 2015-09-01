# -*- coding: utf-8 -*-

import sublime, threading
from sublime_plugin import WindowCommand
from ..gistapi import Gist
from ..sync_settings_manager import SyncSettingsManager as Manager

class SyncSettingsAboutCommand (WindowCommand):
  def run (self):
    try:
      def callRelease ():
        repoData = Gist.getCurrentRelease()
        sublime.message_dialog('Sync Settings Plugin\n\nCurrent Release: %s' % repoData.get('name'))

      t = threading.Thread(target=lambda: callRelease())
      sublime.set_timeout(lambda: t.start(), 100)
    except Exception as e:
      Manager.showMessageAndLog(e)
