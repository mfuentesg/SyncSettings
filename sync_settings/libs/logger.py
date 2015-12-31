# -*- coding: utf-8 -*-

import time
from .helper import Helper

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
    return Helper.get_home_path(Logger.FILE_NAME)

  @staticmethod
  def write(message):
    full_time = time.strftime("[%d/%m/%Y - %H:%M:%S] ")
    message = full_time + message
    path = Logger.get_path()
    action = 'a+' if Helper.exists_path(path) else 'w+'

    Helper.write_to_file(path, message, action)
