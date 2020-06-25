# -*- coding: utf-8 -*-

import os
import sys

import sublime

from . import path
from .logger import logger

if sys.version_info[0] == 2:
    import errno

    class FileExistsError(OSError):
        def __init__(self, msg):
            super(FileExistsError, self).__init__(errno.EEXIST, msg)


filename = 'SyncSettings.sublime-settings'


def save():
    sublime.save_settings(filename)


def update(key, value):
    sublime.load_settings(filename).set(key, value)
    save()


def get(key):
    return sublime.load_settings(filename).get(key)


def create_sync_settings_path():
    global sync_settings_path
    try:
        if not os.path.isabs(sync_settings_path):
            raise ValueError("not absolute path")
        os.mkdir(sync_settings_path, exist_ok=True)
    except FileExistsError:
        pass
    except Exception as e:
        logger.exception(e)
        try:
            os.makedirs(_default_file_path, exist_ok=True)
        except FileExistsError:
            pass
        except Exception as e:
            logger.exception(e)
            raise
        sync_settings_path = _default_file_path


_default_file_path = path.join(os.path.expanduser('~'), '.sync_settings', 'sync.json')
sync_settings_path = get("config_location") or _default_file_path
