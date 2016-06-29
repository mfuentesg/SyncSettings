# -*- coding: utf-8 -*-

import sublime
import sys
import threading

VERSION = int(sublime.version())

reloader = "sync_settings.reloader"

if VERSION > 3000:
  reloader = 'SyncSettings.' + reloader
  from imp import reload

# Make sure all dependencies are reloaded on upgrade
if reloader in sys.modules:
  reload(sys.modules[reloader])

if VERSION > 3000:
  from .sync_settings import reloader
  from .sync_settings.commands import *
  from .sync_settings.sync_version import SyncVersion
else:
  from sync_settings import reloader
  from sync_settings.commands import *
  from sync_settings.sync_version import SyncVersion


def plugin_loaded():
  threading.Thread(
    target=SyncVersion.check_version
  ).start()

"""
  Sublime Text 2 Compatibility
"""
if sys.version_info < (3,):
  plugin_loaded()
