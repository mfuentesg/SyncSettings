# -*- coding: utf-8 -*-

import os
import sublime_plugin

from ..libs import path


class SyncSettingsOpenLogsCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = os.path.join(os.path.expanduser('~'), '.sync_settings', 'sync.log')
        if not path.exists(filename):
            with open(filename, 'a'):
                pass
        self.window.open_file(filename)
