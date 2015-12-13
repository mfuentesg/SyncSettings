import sublime, os
from sublime_plugin import WindowCommand
from ..libs.logger import Logger
from ..libs import helper

class SyncSettingsOpenLogsCommand(WindowCommand):
  def run(self):
    path = Logger.get_path()
    if not helper.exists_path(path):
      helper.create_empty_file(Logger.get_path())

    sublime.active_window().open_file(path)
