import sublime, os
from sublime_plugin import WindowCommand
from ..logger import Logger
from ..helper import *

class SyncSettingsOpenLogsCommand (WindowCommand):
  def run (self):
    path = Logger.getPath()
    if not existsPath(path):
      Logger.createEmptyFile()

    sublime.active_window().open_file(path)
