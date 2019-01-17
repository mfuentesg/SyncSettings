# -*- coding: utf-8 -*-

import json
import sublime
import sublime_plugin

from . import decorators
from .. import sync_version as version, sync_manager as manager
from ..libs import settings, path
from ..libs.gist import Gist
from ..libs.logger import logger
from ..thread_progress import ThreadProgress


class SyncSettingsDownloadCommand(sublime_plugin.WindowCommand):
    @staticmethod
    def parse_to_dict(files, filename):
        file = files.get(path.encode(filename), {})
        if not file or 'content' not in file:
            return {}
        try:
            return json.loads(file['content'], encoding='utf-8')
        except:
            return {}

    def check_installation(self, packages, on_done=None):
        package_settings = sublime.load_settings('Package Control.sublime-settings').get('installed_packages')
        should_call = False
        for package in packages:
            if package not in package_settings:
                should_call = True
                break
        if should_call:
            sublime.set_timeout(lambda: self.check_installation(packages, on_done), 100)
        if not should_call and on_done:
            on_done()

    @staticmethod
    def on_done(g, preferences, package_settings):
        manager.update_files({
            'Preferences.sublime-settings': {
                'content': json.dumps(preferences, sort_keys=True, indent=4)
            },
            path.encode('Package Control.sublime-settings'): {
                'content': json.dumps(package_settings, sort_keys=True, indent=4)
            }
        })
        commit = g['history'][0]
        settings.update('gist_id', g['id'])
        version.update_config_file({
            'hash': commit['version'],
            'created_at': commit['committed_at'],
        })

    def download(self):
        try:
            g = Gist().get(settings.get('gist_id'))
            files = g['files']

            # save a reference to preferences and package control settings files
            package_settings = self.parse_to_dict(files, 'Package Control.sublime-settings')
            preferences = self.parse_to_dict(files, 'Preferences.sublime-settings')

            # avoid update before installing all packages
            files.pop(path.encode('Package Control.sublime-settings'), None)
            files.pop('Preferences.sublime-settings', None)

            sublime.set_timeout(lambda: manager.update_files(files), 100)

            # read installed_packages from remote reference and merge it with the local version
            local_settings = sublime.load_settings('Package Control.sublime-settings')
            setting = 'installed_packages'
            package_settings[setting].append('Sync Settings')
            diff = set(package_settings.get(setting)).difference(set(local_settings.get(setting)))
            if len(diff) > 0:
                self.window.run_command('advanced_install_package', {'packages': list(diff)})
            sublime.set_timeout(lambda: self.check_installation(
                diff,
                on_done=lambda: self.on_done(g, preferences, package_settings)
            ), 100)
        except Exception as e:
            logger.exception(e)
            sublime.message_dialog('Sync Settings:\n\n{}'.format(str(e)))

    @decorators.check_settings('gist_id')
    def run(self):
        ThreadProgress(
            target=self.download,
            message='downloading files',
            success_message='files downloaded'
        )
