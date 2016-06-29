import sublime, os
from sublime_plugin import WindowCommand
from ..libs.logger import Logger
from ..libs.utils import Utils

class SyncSettingsOpenLogsCommand(WindowCommand):
  def run(self):
    path = Logger.get_path()

    if not Utils.exists_path(path):
      Utils.create_empty_file(Logger.get_path())

    self.window.open_file(path)
