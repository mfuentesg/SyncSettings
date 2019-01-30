# -*- coding: utf-8 -*-

import sublime

filename = 'SyncSettings.sublime-settings'


def save():
    sublime.save_settings(filename)


def update(key, value):
    sublime.load_settings(filename).set(key, value)
    save()


def get(key):
    return sublime.load_settings(filename).get(key)
