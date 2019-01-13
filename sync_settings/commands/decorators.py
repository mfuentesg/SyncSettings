# -*- coding: utf-8 -*-

from functools import wraps
import sublime

from ..libs import settings


def check_settings(*props):
    def check_settings_wrapper(func):
        @wraps(func)
        def check_settings_inner(self, *args, **kwargs):
            for prop in props:
                if not settings.get(prop):
                    prop_text = 'properties' if len(args) > 1 else 'property'
                    msg = (
                        'Sync Settings:\n\n'
                        'The {} {}, must be defined. Edit your settings file.'
                    )
                    sublime.message_dialog(msg.format(prop_text, ' and '.join(props)))
                    sublime.active_window().run_command('open_file', {
                        'file': '${packages}/User/SyncSettings.sublime-settings'
                    })
                    return
            func(self, *args, **kwargs)
        return check_settings_inner
    return check_settings_wrapper
