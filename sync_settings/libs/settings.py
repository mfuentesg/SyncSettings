# -*- coding: utf-8 -*-

import errno
import os

import sublime

from . import path
from .logger import logger

filename = 'SyncSettings.sublime-settings'


def save():
    sublime.save_settings(filename)


def update(key, value):
    sublime.load_settings(filename).set(key, value)
    save()


def get(key):
    return sublime.load_settings(filename).get(key)


def create_sync_settings_path(location):
    global sync_settings_path
    try:
        if not os.path.isabs(location):
            sublime.error_message('%s is not absolute path, defaulting to %s' %
                                  (location, default_file_path))
            location = default_file_path
        os.makedirs(location, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            sublime.message_dialog(
                'Failed to make the path ({}), defaulting to {}'.format(
                    location, default_file_path))
            logger.exception(e)
            try:
                os.makedirs(default_file_path, exist_ok=True)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e
            sync_settings_path = path.join(default_file_path, 'sync.json')
            return
    sync_settings_path = path.join(location, 'sync.json')
    return


default_file_path = path.join(os.path.expanduser('~'), '.sync_settings')
sync_settings_path = str()
