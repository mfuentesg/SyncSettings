# -*- coding: utf-8 -*-

import sublime
import sys
import os

f = os.path.join(os.path.expanduser('~'), '.sync_settings')
if not os.path.isdir(f):
    os.mkdir(f)

reloader = 'sync_settings.reloader'

if int(sublime.version()) > 3000:
    from .sync_settings.commands import *  # noqa: F403, F401

    reloader = 'SyncSettings.' + reloader
    from imp import reload
else:
    from sync_settings.commands import *  # noqa: F403, F401

# Make sure all dependencies are reloaded on upgrade
if reloader in sys.modules:
    reload(sys.modules[reloader])
