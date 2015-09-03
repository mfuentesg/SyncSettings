# -*- coding: utf-8 -*-

import os, time
from .helper import *

class Logger:
  FILE_NAME = '.sync-settings.log'
  MESSAGE_INFO_TYPE = 1
  MESSAGE_ERROR_TYPE = 2

  @staticmethod
  def log (message, type):
    if type == Logger.MESSAGE_ERROR_TYPE:
      message = 'ERROR: ' + message
    elif type == Logger.MESSAGE_INFO_TYPE:
      message = 'INFO: ' + message
    Logger.write(message)

  @staticmethod
  def getPath ():
    return getHomePath(Logger.FILE_NAME)

  @staticmethod
  def createEmptyFile ():
    try: open(Logger.getPath(), 'a').close()
    except Exception as e: print(e)

  @staticmethod
  def write (message):
    fullTime = time.strftime("[%d/%m/%Y - %H:%M:%S] ")
    message = fullTime + message
    path = Logger.getPath()
    action = 'a+' if existsPath(path) else 'w+'

    try:
      with open(path, action) as f:
        f.write(message + '\n')
        f.close()
    except Exception as e:
      print(e)
