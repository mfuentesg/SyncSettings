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
            raise ValueError("not absolute path")
        os.mkdir(location)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            logger.exception(e)
            try:
                os.mkdir(_default_file_path)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    return
                else:
                    raise e
            sync_settings_path = path.join(_default_file_path, 'sync.json')
            return
    sync_settings_path = path.join(location, 'sync.json')
    return


_default_file_path = path.join(os.path.expanduser('~'), '.sync_settings')
sync_settings_path = str()
