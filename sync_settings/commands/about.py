# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..gistapi import Gist
from ..sync_settings_manager import SyncSettingsManager as Manager

class SyncSettingsAboutCommand (WindowCommand):
  def run (self):
    try:
      repoData = Gist.getCurrentRelease()
      sublime.message_dialog('Sync Settings Plugin\n\nCurrent Release: %s' % repoData.get('name'))
    except Exception as e:
      Manager.showMessageAndLog(e)
