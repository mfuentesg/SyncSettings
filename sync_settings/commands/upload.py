# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

from . import decorators
from .. import sync_version as version, sync_manager as manager
from ..libs import settings
from ..libs import gist
from ..libs.logger import logger
from ..thread_progress import ThreadProgress


class SyncSettingsUploadCommand(sublime_plugin.WindowCommand):
    def upload(self):
        files = manager.get_files()
        if not len(files):
            sublime.status_message('Sync Settings: there are not files to upload')
            return
        try:
            g = gist.Gist(settings.get('access_token')).update(
                settings.get('gist_id'),
                data={'files': files}
            )
            commit = g['history'][0]
            version.update_config_file({
                'hash': commit['version'],
                'created_at': commit['committed_at'],
            })
        except gist.NotFoundError as e:
            msg = (
                'Sync Settings:\n\n'
                '{}\n\n'
                'Please check if the access token was created with the gist scope.\n\n'
                'If the access token is correct, please, delete the value of `gist_id` property manually.'
            )
            sublime.message_dialog(msg.format(str(e)))
        except Exception as e:
            logger.exception(e)
            sublime.message_dialog('Sync Settings:\n\n{}'.format(str(e)))

    @decorators.check_settings('gist_id', 'access_token')
    def run(self):
        ThreadProgress(
            target=self.upload,
            message='uploading files',
            success_message='files uploaded'
        )
