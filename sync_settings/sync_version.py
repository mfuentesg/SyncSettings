# -*- coding: utf-8 -*

import sublime
import json
import os
from .libs.gist import Gist
from .libs import settings


file_path = os.path.join(os.path.expanduser('~'), '.sync_settings', 'sync.json')


def get_local_version():
    if not os.path.isfile(file_path):
        return {}
    with open(file_path) as f:
        data = json.load(f)
    return data


def get_remote_version():
    try:
        commit, *_ = Gist().commits(settings.get('gist_id'))
        return {
            'hash': commit['version'],
            'created_at': commit['committed_at'],
        }
    except Exception:
        return {}


def update_config_file(info):
    with open(file_path, 'w') as f:
        json.dump(info, f)


def show_update_dialog(on_yes=None):
    msg = (
        'Sync Settings:\n\n'
        'Your settings seem out of date.\n\n'
        'Do you want to download the latest version?'
    )
    if sublime.yes_no_cancel_dialog(msg) == sublime.DIALOG_YES:
        # call download command
        if on_yes:
            on_yes()


def upgrade():
    local = get_local_version()
    if not local.get('hash', ''):
        show_update_dialog()
        return
    remote = get_remote_version()
    if local['hash'] == remote.get('hash', ''):
        return
    # TODO: check if get remote version failed
    if local['created_at'] < remote.get('created_at', ''):
        show_update_dialog(
            on_yes=lambda: update_config_file(remote)
        )
