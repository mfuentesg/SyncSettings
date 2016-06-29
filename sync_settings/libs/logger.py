# -*- coding: utf-8 -*-

import time
from .utils import Utils

class Logger:
  FILE_NAME = '.sync-settings.log'
  MESSAGE_INFO_TYPE = 1
  MESSAGE_ERROR_TYPE = 2

  @staticmethod
  def log(message, message_type):
    """Writes to the log file

    Arguments:
      message {string}: Content of the log
      message_type {int}: Type of the log
    """

    if message_type == Logger.MESSAGE_ERROR_TYPE:
      message = 'ERROR: ' + message
    elif message_type == Logger.MESSAGE_INFO_TYPE:
      message = 'INFO: ' + message

    Logger.write(message)

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
    message = full_time + message
    path = Logger.get_path()
    action = 'a+' if Utils.exists_path(path) else 'w+'

    Utils.write_to_file(path, message, action)
