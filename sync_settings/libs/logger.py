# -*- coding: utf-8 -*-

import time
from .utils import Utils

class Logger:
  FILE_NAME = '.sync-settings.log'

  @staticmethod
  def log(message, is_error = False):
    """Writes to the log file

    Arguments:
      message {string}: Content of the log
      message_type {int}: Type of the log
    """

    Logger.write('ERROR: ' + message if is_error else 'INFO: ' + message)

  @staticmethod
  def get_path():
    """Gets the log file path

    Returns:
      [string]: File path
    """

    return Utils.get_home_path(Logger.FILE_NAME)

  @staticmethod
  def write(message):
    """Adds extra info to the log

    Arguments:
      message {string}: Log content
    """

    full_time = time.strftime("[%d/%m/%Y - %H:%M:%S] ")
    message = full_time + message + '\n'
    path = Logger.get_path()
    action = 'ab+' if Utils.exists_path(path) else 'wb+'

    Utils.write_to_file(path, message, action)
