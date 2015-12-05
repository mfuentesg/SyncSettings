# -*- coding: utf-8 -*-

import sublime
from .libs.logger import Logger
from .libs import helper

class SyncSettingsManager:
  settings_filename = 'SyncSettings.sublime-settings'

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
  def get_filtered_files():
    pp = SyncSettingsManager.get_packages_path
    files = helper.get_files(pp())
    excluded_files = [pp(f) for f in SyncSettingsManager.settings('excluded_files')]
    resulting_files = helper.exclude_files_by_patterns(files, excluded_files)

    return resulting_files

  @staticmethod
  def get_encoded_files():
    pp = SyncSettingsManager.get_packages_path
    encoded_files = SyncSettingsManager.get_filtered_files()
    encoded_files = [helper.encode_path(f.replace(pp(), '')) for f in encoded_files]

    return encoded_files

  @staticmethod
  def get_files_content():
    files = SyncSettingsManager.get_filtered_files()
    r = {}

    for f in files:
      if helper.exists_path(f):
        try:
          content = open(f, 'r').read()
          if content.strip() is not '':
            f = helper.encode_path(f.replace(SyncSettingsManager.get_packages_path(), ''))
            r.update({f: {'content': content}})
        except Exception as e:
          Logger.log(str(e), Logger.MESSAGE_ERROR_TYPE)
    return r

  @staticmethod
  def get_packages_path(filename = None):
    path = helper.join_path((sublime.packages_path(), 'User' + helper.os_separator()))
    if not filename is None:
      return helper.join_path((path, filename))
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

  @staticmethod
  def update_from_remote_files(remote_files):
    if isinstance(remote_files, dict):
      decoded_files = [SyncSettingsManager.get_packages_path(helper.decode_path(f)) for f in remote_files]
      excluded_files = SyncSettingsManager.settings('excluded_files')
      filtered_files = helper.exclude_files_by_patterns(decoded_files, excluded_files)

      for f in filtered_files:
        encode_file = helper.encode_path(f.replace(SyncSettingsManager.get_packages_path(), ''))
        current_file = remote_files.get(encode_file)
        try:
          helper.update_content_file(f, current_file.get('content'))
        except Exception as e:
          message = 'It has generated an error when to update or create the file %s'%(f)
          Logger.log(message + str(e), Logger.MESSAGE_ERROR_TYPE)
