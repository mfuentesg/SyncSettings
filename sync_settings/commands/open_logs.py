import sublime, os
from sublime_plugin import WindowCommand
from ..logger import Logger
from ..helper import *

class SyncSettingsOpenLogsCommand(WindowCommand):
  def run(self):
    path = Logger.get_path()
    if not exists_path(path):
      Logger.create_empty_file()

    sublime.active_window().open_file(path)
