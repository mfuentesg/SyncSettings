# -*- coding: utf-8 -*-

import sublime
import sys

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
else:
    from sync_settings import reloader
    from sync_settings.commands import *
