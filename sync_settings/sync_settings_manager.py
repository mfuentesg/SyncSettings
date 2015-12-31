# -*- coding: utf-8 -*-

import sublime
from .libs.logger import Logger
from .libs.helper import Helper
from .libs.gistapi import Gist

class SyncSettingsManager:
  SETTINGS_FILENAME = 'SyncSettings.sublime-settings'

  @classmethod
  def settings(cls, key = None, new_value = None):
    settings =  sublime.load_settings(cls.SETTINGS_FILENAME)
    if not key is None and not new_value is None:
      settings.set(key, new_value)
    elif not key is None and new_value is None:
      return settings.get(key)
    else:
      return settings

  @classmethod
  def get_filtered_files(cls):
    excluded_files = cls.parse_patterns('excluded_files')
    files = Helper.get_files(cls.get_packages_path())

    return Helper.exclude_files_by_patterns(files, excluded_files)

  @classmethod
  def parse_patterns(cls, setting_key):
    result_list = []

    for f in cls.settings(setting_key):
      if not Helper.is_file_extension(f):
        result_list.append(cls.get_packages_path(f))
        continue
      result_list.append(f)

    return result_list

  @classmethod
  def get_encoded_files(cls):
    pp = cls.get_packages_path
    encoded_files = cls.get_filtered_files()
    encoded_files = [Helper.encode_path(f.replace(pp(), '')) for f in encoded_files]

    return encoded_files

  @classmethod
  def get_files_content(cls):
    files = cls.get_filtered_files()
    r = {}

    for f in files:
      if Helper.exists_path(f):
        try:
          content = open(f, 'r', encoding = 'ISO-8859-1').read()
          if content.strip() is not '':
            f = Helper.encode_path(f.replace(cls.get_packages_path(), ''))
            r.update({f: {'content': content}})
        except Exception as e:
          Logger.log(str(e), Logger.MESSAGE_ERROR_TYPE)
    return r

  @classmethod
  def get_packages_path(cls, filename = None):
    path = Helper.join_path((sublime.packages_path(), 'User' + Helper.os_separator()))
    if not filename is None:
      return Helper.join_path((path, filename))
    return path

  @classmethod
  def get_settings_filename(cls):
    return cls.SETTINGS_FILENAME

  @classmethod
  def show_message_and_log(cls, message, error = True):
    m = l = ''
    if isinstance(message, Exception):
      message = message.to_json()
      m = message.get('app_message')
      l = '%s, File: %s - Line: %s' % (message.get('error_description'), message.get('filename'), message.get('line'))
    elif isinstance(message, str):
      m = l = message

    sublime.status_message('Sync Settings: ' + m)
    error_type = Logger.MESSAGE_ERROR_TYPE if error else Logger.MESSAGE_INFO_TYPE
    Logger.log(l, error_type)

  @classmethod
  def update_from_remote_files(cls, remote_files):
    if isinstance(remote_files, dict):
      decoded_files = [cls.get_packages_path(Helper.decode_path(f)) for f in remote_files]
      excluded_files = cls.settings('excluded_files')
      filtered_files = Helper.exclude_files_by_patterns(decoded_files, excluded_files)

      for f in filtered_files:
        encode_file = Helper.encode_path(f.replace(cls.get_packages_path(), ''))
        current_file = remote_files.get(encode_file)
        try:
          Helper.write_to_file(f, current_file.get('content'), 'w+')
        except Exception as e:
          message = 'It has generated an error when to update or create the file %s' % (f)
          Logger.log(message + str(e), Logger.MESSAGE_ERROR_TYPE)

  @classmethod
  def gist_api(cls):
    try:
      return Gist(cls.settings('access_token'))
    except Exception as e:
      cls.show_message_and_log(e)

    return None
