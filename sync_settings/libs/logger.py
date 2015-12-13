# -*- coding: utf-8 -*-

import time
from .helper import get_home_path, exists_path, write_to_file

class Logger:
  FILE_NAME = '.sync-settings.log'
  MESSAGE_INFO_TYPE = 1
  MESSAGE_ERROR_TYPE = 2

  @staticmethod
  def log(message, message_type):
    if message_type == Logger.MESSAGE_ERROR_TYPE:
      message = 'ERROR: ' + message
    elif message_type == Logger.MESSAGE_INFO_TYPE:
      message = 'INFO: ' + message
    Logger.write(message)

  @staticmethod
  def get_path():
    return get_home_path(Logger.FILE_NAME)

  @staticmethod
  def write(message):
    full_time = time.strftime("[%d/%m/%Y - %H:%M:%S] ")
    message = full_time + message
    path = Logger.get_path()
    action = 'a+' if exists_path(path) else 'w+'

    write_to_file(path, message, action)
