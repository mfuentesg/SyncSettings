# -*- coding: utf-8 -*-

import sublime
from .libs.logger import Logger
from .libs.helper import Helper
from .libs.gistapi import Gist

import os

class SyncSettingsManager:
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
    files = Helper.get_files(cls.get_packages_path())

    return Helper.merge_lists(
      Helper.exclude_files_by_patterns(files, excluded_patterns),
      Helper.filter_files_by_patterns(files, included_patterns)
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

    return Helper.parse_patterns(patterns, base_path)

  @classmethod
  def get_encoded_files(cls):
    """Generates a valid list with the filtered files to upload

    Returns:
      [list]
    """

    pp = cls.get_packages_path
    encoded_files = cls.get_filtered_files()
    return [Helper.encode_path(f.replace(pp(), '')) for f in encoded_files]

  @classmethod
  def get_files_content(cls):
    """Creates a list dict with the files content

    Returns:
      [dict]
    """

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
    """Gets the Sublime package path

    Arguments:
      filename {string}: If is specified the file is append to the final path
    """

    path = Helper.join_path(sublime.packages_path(), 'User' + Helper.os_separator())
    if not filename is None:
      return Helper.join_path(path, filename)
    return path

  @classmethod
  def get_settings_filename(cls):
    """Gets the Plug-in settings file name

    Returns:
      [string]
    """

    return cls.SETTINGS_FILENAME

  @classmethod
  def show_message_and_log(cls, message, error = True):
    """Writes and show the log message to the user

    Arguments:
      message {dict}: The message to show
      error {bool}: Indicates if the message is an Error
    """

    m = l = ''

    if isinstance(message, Exception):
      message = message.to_json()
      m = message.get('app_message')
      l = '%s, File: %s - Line: %s' % (
        message.get('error_description'),
        message.get('filename'),
        message.get('line')
      )
    elif isinstance(message, str):
      m = l = message

    sublime.status_message('Sync Settings: ' + m)
    error_type = Logger.MESSAGE_ERROR_TYPE if error else Logger.MESSAGE_INFO_TYPE
    Logger.log(l, error_type)

  @classmethod
  def update_from_remote_files(cls, remote_files):
    """Overwrite the local files content with the remote content

    Arguments:
      remote_files {dict}: List of remote files
    """

    if isinstance(remote_files, dict):
      decoded_files = [cls.get_packages_path(Helper.decode_path(f)) for f in remote_files]
      excluded_patterns = cls.parse_patterns('excluded_files')
      included_patterns = cls.parse_patterns('included_files')

      filtered_files = Helper.merge_lists(
        Helper.exclude_files_by_patterns(decoded_files, excluded_patterns),
        Helper.filter_files_by_patterns(decoded_files, included_patterns),
      )

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
    """Gets an Gist object

    Returns:
      [Gist]: Gist instance
    """

    try:
      return Gist(cls.settings('access_token'))
    except Exception as e:
      cls.show_message_and_log(e)

    return None

  @classmethod
  def load(cls):
    cache = cls.get_cache()
    settings = cls.settings()

    if (settings.get('access_token') and settings.get('gist_id')):
      api = cls.gist_api()
      cache_path = cls.get_cache_path()

      if (api is not None):
        gist_content = api.get(settings.get('gist_id'))
        gist_history = gist_content.get('history')[0]

        if (not cache.get('revision_hash')):
          content = {
            'revision_date': gist_history.get('committed_at'),
            'revision_hash': gist_history.get('version')
          }

          Helper.write_to_file(cache_path, content, 'w', True)

        content = '''
          Your settings is out to date.
          <a href = "#download">Download the latest version</a>
        '''

        cls.show_popup(content)

  @classmethod
  def get_cache_path(cls):
    parent_dir = os.path.abspath(__file__ + "/../../")
    return Helper.join_path(parent_dir, '.sync_settings_cache')

  @classmethod
  def get_cache(cls):
    cache_path = cls.get_cache_path()

    if (not Helper.exists_path(cache_path)):
      Helper.create_empty_file(cache_path)
      Helper.write_to_file(cache_path, '{}')

    return Helper.get_file_content(cache_path, True)

  @classmethod
  def show_popup(cls, content):
    current_view = sublime.active_window().active_view()
    message = cls.get_message_template(content, 'error')

    current_view.show_popup(message, on_navigate=cls.on_nav)

  @classmethod
  def on_nav(cls, url):
    current_window = sublime.active_window()
    current_view = current_window.active_view()

    current_window.run_command('sync_settings_download')
    current_view.hide_popup()

  @classmethod
  def get_message_template(cls, message, type):
    if (type == 'warning'):
      message = '<div class = "warning">👉 - %s</div>' % (message)
    elif (type == 'error'):
      message = '<div class = "error">💩 - %s</div>' % (message)
    else:
      message = '<div class = "success">⚡️ - %s</div>' % (message)

    return '''
      <style>
        body {
          margin: 0;
          font-size: 16px;
        }

        div {
          padding: 10px 15px;
        }

        div.success {
          color: #43783b;
          background-color: #ace1ae;
        }

        div.warning {
          color: #9c9759;
          background-color: #f6f0a6;
        }

        div.error {
          background-color: #f89d9d;
          color: #751414;
        }
      </style>

      %s
    ''' % (message)
