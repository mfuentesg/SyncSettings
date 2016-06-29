# -*- coding: utf-8 -*-
# Adapted from @wbond's resource loader.

import sys
import sublime

VERSION = int(sublime.version())

mod_prefix = 'sync_settings'
reload_mods = []

if VERSION > 3000:
  mod_prefix = 'SyncSettings.' + mod_prefix
  from imp import reload
  for mod in sys.modules:
    if mod[0:15] == 'SyncSettings' and sys.modules[mod] is not None:
      reload_mods.append(mod)
else:
  for mod in sorted(sys.modules):
    if mod[0:17] == 'sync_settings' and sys.modules[mod] is not None:
      reload_mods.append(mod)

mods_load_order = [
  '',
  '.libs',
  '.libs.gist_api',
  '.libs.logger',
  '.libs.utils',

  '.sync_manager',
  '.sync_logger',
  '.sync_version',
  '.thread_progress',

  '.commands',
  '.commands.create_and_upload',
  '.commands.delete_and_create',
  '.commands.download',
  '.commands.upload',
  '.commands.open_logs'
]

for suffix in mods_load_order:
  mod = mod_prefix + suffix
  if mod in reload_mods:
    reload(sys.modules[mod])
