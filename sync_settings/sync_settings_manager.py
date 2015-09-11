# -*- coding: utf-8 -*-

import sublime
from .logger import Logger
from .helper import *

class SyncSettingsManager:
  settings_filename = 'SyncSettings.sublime-settings'
  files = [
    "Package Control.merged-ca-bundle",
    "Package Control.system-ca-bundle",
    "Package Control.user-ca-bundle",
    "Package Control.sublime-settings",
    "Preferences.sublime-settings",
    "Package Control.last-run",
    "Default (OSX).sublime-keymap",
    "Default (Windows).sublime-keymap",
    "Default (Linux).sublime-keymap"
  ]

  @staticmethod
  def settings(key = None, new_value = None):
    settings =  sublime.load_settings(SyncSettingsManager.settings_filename)
    if not key is None and not new_value is None:
      settings.set(key, new_value)
    elif not key is None and new_value is None:
      return settings.get(key)
    else:
      return settings

  @staticmethod
  def get_files():
    excluded_files = SyncSettingsManager.settings('excluded_files')
    return get_difference(SyncSettingsManager.files, excluded_files)

  @staticmethod
  def get_files_content():
    r = {}
    for f in SyncSettingsManager.get_files():
      full_path = SyncSettingsManager.get_packages_path(f)
      if exists_path(full_path):
        try:
          content = open(full_path, 'r').read()
          r.update({f: {'content': content}})
        except Exception as e:
          Logger.log(str(e), Logger.MESSAGE_ERROR_TYPE)
    return r

  @staticmethod
  def get_packages_path(filename = None):
    path = join_path((sublime.packages_path(), 'User'))
    if not filename is None:
      return join_path((path, filename))
    return path

  @staticmethod
  def get_settings_filename():
    return SyncSettingsManager.settings_filename

  @staticmethod
  def show_message_and_log(message, error = True):
    m = l = ''
    if isinstance(message, Exception):
      message = message.to_json()
      m = message.get('app_message')
      l = message.get('error_description')+ ', File: ' + message.get('filename') +' - Line: ' + message.get('line')
    elif isinstance(message, str):
      m = l = message

    sublime.status_message('Sync Settings: ' + m)
    Logger.log(l, Logger.MESSAGE_ERROR_TYPE if error else Logger.MESSAGE_INFO_TYPE)
