# -*- coding: utf-8 -*-

import os
import sublime
import sublime_plugin

from . import decorators
from .. import sync_version as version, sync_manager as manager
from ..libs import settings, path, file
from ..libs.gist import Gist
from ..libs.logger import logger
from ..thread_progress import ThreadProgress


class SyncSettingsDownloadCommand(sublime_plugin.WindowCommand):
    temp_folder = path.join(os.path.expanduser('~'), '.sync_settings', 'temp')

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

    def on_done(self, g):
        manager.move_files(self.temp_folder)
        commit = g['history'][0]
        settings.update('gist_id', g['id'])
        version.update_config_file({
            'hash': commit['version'],
            'created_at': commit['committed_at'],
        })

    def download(self):
        try:
            g = Gist(
                token=settings.get('access_token'),
                http_proxy=settings.get('http_proxy'),
                https_proxy=settings.get('https_proxy')
            ).get(settings.get('gist_id'))
            files = g['files']

            manager.fetch_files(files, self.temp_folder)
            file_content = manager.get_content(
                path.join(self.temp_folder, path.encode('Package Control.sublime-settings'))
            )
            package_settings = file.encode_json('{}' if file_content == '' else file_content)
            # read installed_packages from remote reference and merge it with the local version
            local_settings = sublime.load_settings('Package Control.sublime-settings')
            setting = 'installed_packages'
            if setting not in package_settings:
                package_settings[setting] = []
            package_settings[setting].append('Sync Settings')
            diff = set(package_settings.get(setting)).difference(set(local_settings.get(setting)))
            if len(diff) > 0:
                self.window.run_command('advanced_install_package', {'packages': list(diff)})
            sublime.set_timeout(lambda: self.check_installation(diff, on_done=lambda: self.on_done(g)), 100)
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
