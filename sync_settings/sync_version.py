# -*- coding: utf-8 -*

import sublime
from os import path
from .sync_manager import SyncManager
from .sync_logger import SyncLogger
from .libs.utils import Utils

class SyncVersion:
  FILE_NAME = '.sync-settings.cache'

  @classmethod
  def check_version(cls):
    """Verifies if the current Gist is up to date or exists"""
    settings = SyncManager.settings()

    if (settings.get('access_token') and settings.get('gist_id')):

      outdate_message = 'Your settings is out to date, download the latest version!'

      if (cls.has_cache()):
        try:
          api = SyncManager.gist_api()

          if (api is not None):
            gist_content = api.get(settings.get('gist_id'))
            gist_history = gist_content.get('history')[0]

            if (not cls.its_updated(gist_content)):
              if SyncManager.settings('auto_upgrade'):
                sublime.active_window().run_command('sync_settings_download')
              else:
                SyncLogger.log(outdate_message, SyncLogger.LOG_LEVEL_WARNING)
        except Exception as ex:
          SyncLogger.log(ex, SyncLogger.LOG_LEVEL_ERROR)
      elif(settings.get('gist_id')):
        SyncLogger.log(outdate_message, SyncLogger.LOG_LEVEL_WARNING)

  @classmethod
  def has_cache(cls):
    """Checks if the cache file has content

    Returns:
      [bool]
    """
    cache = cls.get_cache()
    return cache and 'revision_hash' in cache and \
           'revision_date' in cache

  @classmethod
  def its_updated(cls, gist_data):
    """Verifies if the current settings are up to date

    Arguments:
      gist_data {dict}: Gist information

    Returns:
      [bool]
    """

    gist_history = gist_data.get('history')[0]
    cache = cls.get_cache()

    same_version = gist_history.get('version') == cache.get('revision_hash')
    updated_hash = cache.get('revision_date') <= gist_history.get('committed_at')

    return updated_hash and same_version

  @classmethod
  def __get_cache_path(cls):
    """Gets the cache file path

    Returns:
      [str]
    """

    return Utils.get_home_path(SyncVersion.FILE_NAME)

  @classmethod
  def get_cache(cls):
    """Gets the cache file content in JSON format

    Returns:
      [dict]
    """

    cache_path = cls.__get_cache_path()

    if (not Utils.exists_path(cache_path)):
      Utils.create_empty_file(cache_path)
      Utils.write_to_file(cache_path, '{}', 'wb+')

    return Utils.get_file_content(cache_path, True)

  @classmethod
  def clear_cache(cls, new_data = {}):
    """Removes all content in the cache file"""

    Utils.write_to_file(cls.__get_cache_path(), new_data, 'w', True)

  @classmethod
  def upgrade(cls, gist_content):
    """Update cache file with the last gist data

    Arguments:
      gist_content {dict}: Gist info
    """

    gist_history = gist_content.get('history')[0]
    cls.clear_cache({
      'revision_date': gist_history.get('committed_at'),
      'revision_hash': gist_history.get('version')
    })
