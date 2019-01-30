# -*- coding: utf-8 -*-
# Credits to @wbond package_control

import sublime
import threading


class ThreadProgress:
    """
      Animates an indicator, [=   ], in the status area while a thread runs

      :param target:
        The thread to track for activity

      :param message:
        The message to display next to the activity indicator
    """

    def __init__(self, target, message, success_message=''):
        self.message = message
        self.success_message = success_message
        self.addend = 1
        self.size = 8

        self.thread = threading.Thread(target=target)
        self.thread.start()
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            msg = '' if not self.success_message else 'Sync Settings: {}'.format(self.success_message)
            sublime.status_message(msg)
            return
        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('Sync Settings: {} [{}={}]'.format(self.message, ' ' * before, ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1

        i += self.addend
        sublime.set_timeout(lambda: self.run(i), 100)
