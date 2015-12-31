import sublime, os
from sublime_plugin import WindowCommand
from ..libs.logger import Logger
from ..libs.helper import Helper

class SyncSettingsOpenLogsCommand(WindowCommand):
  def run(self):
    path = Logger.get_path()
    if not Helper.exists_path(path):
      Helper.create_empty_file(Logger.get_path())

    sublime.active_window().open_file(path)
