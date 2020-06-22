# -*- coding: utf-8 -*-

import os

import sublime

from . import logger, path

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
        os.mkdir(sync_settings_path, exist_ok=True)
    except FileExistsError:
        pass
    except Exception as e:
        logger.logger.exception(e)
        try:
            os.makedirs(_default_file_path, exist_ok=True)
        except FileExistsError:
            pass
        except Exception as e:
            logger.logger.exception(e)
            raise
        sync_settings_path = _default_file_path


_default_file_path = path.join(os.path.expanduser('~'), '.sync_settings', 'sync.json')
sync_settings_path = get("config_location") or _default_file_path
