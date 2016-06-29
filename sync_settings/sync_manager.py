# -*- coding: utf-8 -*-

import sublime
from .sync_logger import SyncLogger
from .libs.utils import Utils
from .libs.logger import Logger
from .libs.gist_api import Gist

class SyncManager:
  SETTINGS_FILENAME = 'SyncSettings.sublime-settings'

  @classmethod
  def settings(cls, key = None, new_value = None):
    """Gets all or a single setting from the Plug-in file

    Keyword Arguments:
      key {string}: Setting name
      new_value {string}: New value for the specified setting

    Returns:
      [dict]
    """

    settings =  sublime.load_settings(cls.SETTINGS_FILENAME)
    if not key is None and not new_value is None:
      settings.set(key, new_value)
    elif not key is None and new_value is None:
      return settings.get(key)
    else:
      return settings

  @classmethod
  def get_filtered_files(cls):
    """Gets the list files to synchronize

    Returns:
      [list]
    """

    excluded_patterns = cls.parse_patterns('excluded_files')
    included_patterns = cls.parse_patterns('included_files')
    files = Utils.get_files(cls.get_packages_path())

    return Utils.merge_lists(
      Utils.exclude_files_by_patterns(files, excluded_patterns),
      Utils.filter_files_by_patterns(files, included_patterns)
    )

  @classmethod
  def parse_patterns(cls, setting_key):
    """Converts the specified property to a valid format

    Arguments:
      setting_key {string}: Setting name

    Returns:
      [list]: Parsed list
    """

    result_list = []
    patterns = cls.settings(setting_key)
    base_path = cls.get_packages_path()

    return Utils.parse_patterns(patterns, base_path)

  @classmethod
  def get_encoded_files(cls):
    """Generates a valid list with the filtered files to upload

    Returns:
      [list]
    """

    pp = cls.get_packages_path
    encoded_files = cls.get_filtered_files()
    return [Utils.encode_path(f.replace(pp(), '')) for f in encoded_files]

  @classmethod
  def get_files_content(cls):
    """Creates a list dict with the files content

    Returns:
      [dict]
    """

    files = cls.get_filtered_files()
    r = {}

    for f in files:
      if Utils.exists_path(f):
        try:
          content = open(f, 'r', encoding = 'ISO-8859-1').read()
          if content.strip() is not '':
            f = Utils.encode_path(f.replace(cls.get_packages_path(), ''))
            r.update({f: {'content': content}})
        except Exception as e:
          Logger.log(str(e), True)

    return r

  @classmethod
  def get_packages_path(cls, filename = None):
    """Gets the Sublime package path

    Arguments:
      filename {string}: If is specified the file is append to the final path
    """

    path = Utils.join_path(sublime.packages_path(), 'User' + Utils.os_separator())
    if not filename is None:
      return Utils.join_path(path, filename)
    return path

  @classmethod
  def get_settings_filename(cls):
    """Gets the Plug-in settings file name

    Returns:
      [string]
    """

    return cls.SETTINGS_FILENAME

  @classmethod
  def update_from_remote_files(cls, remote_files):
    """Overwrite the local files content with the remote content

    Arguments:
      remote_files {dict}: List of remote files
    """

    if isinstance(remote_files, dict):
      decoded_files = [cls.get_packages_path(Utils.decode_path(f)) for f in remote_files]
      excluded_patterns = cls.parse_patterns('excluded_files')
      included_patterns = cls.parse_patterns('included_files')

      filtered_files = Utils.merge_lists(
        Utils.exclude_files_by_patterns(decoded_files, excluded_patterns),
        Utils.filter_files_by_patterns(decoded_files, included_patterns),
      )

      for f in filtered_files:
        encode_file = Utils.encode_path(f.replace(cls.get_packages_path(), ''))
        current_file = remote_files.get(encode_file)
        try:
          Utils.write_to_file(f, current_file.get('content'), 'w+')
        except Exception as e:
          message = 'It has generated an error when to update or create the file %s' % (f)
          Logger.log(message + str(e), True)

  @classmethod
  def gist_api(cls):
    """Gets an Gist object

    Returns:
      [Gist]: Gist instance
    """

    try:
      return Gist(cls.settings('access_token'))
    except Exception as e:
      SyncLogger.log(e, SyncLogger.LOG_LEVEL_ERROR)

    return None
