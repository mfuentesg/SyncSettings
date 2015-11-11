import sublime, os
from sublime_plugin import WindowCommand
from ..libs.logger import Logger
from ..libs import helper

class SyncSettingsOpenLogsCommand(WindowCommand):
  def run(self):
    path = Logger.get_path()
    if not helper.exists_path(path):
      Logger.create_empty_file()

    sublime.active_window().open_file(path)
