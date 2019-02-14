# -*- coding: utf-8 -*-

import unittest
import mock
import os
from sync_settings import sync_manager as manager


def create_file(file, mode='w', content=None):
    delete_file(file)
    with open(file, mode) as fi:
        if content:
            fi.write(content)


def delete_file(file):
    if os.path.isfile(file):
        os.unlink(file)


class TestSyncManager(unittest.TestCase):
    @mock.patch('sync_settings.libs.settings.get', mock.MagicMock(return_value=[
        '*Package Control.sublime-settings',
        '*.txt',
        'foo/**/*.py',
        'bar/*.py',
        'bar/*.md',
    ]))
    def test_should_exclude(self):
        tests = [
            {'file': '/usr/bin/conf/default.conf', 'expected': False},
            {'file': '/foo/bar/script.py', 'expected': False},
            {'file': 'file.js', 'expected': False},
            {'file': 'Theme.tmTheme', 'expected': False},
            {'file': 'foo/bar/file.py', 'expected': True},
            {'file': 'bar/README.md', 'expected': True},
            {'file': '/a/long/path/file.txt', 'expected': True},
            {'file': '/User/Settings/SyncSettings.sublime-settings', 'expected': True},
            {'file': '/User/Settings/Package Control.sublime-settings', 'expected': True},
        ]

        for test in tests:
            self.assertEqual(
                test['expected'],
                manager.should_exclude(test['file']),
                'comparing: {}'.format(test['file'])
            )

    @mock.patch('sync_settings.libs.settings.get', mock.MagicMock(return_value=[
        '*.sublime-settings',
        '*.txt',
    ]))
    def test_should_include(self):
        tests = [
            {'file': '/usr/bin/conf/default.conf', 'expected': False},
            {'file': '', 'expected': False},
            {'file': '/foo/bar/script.py', 'expected': False},
            {'file': 'file.js', 'expected': False},
            {'file': 'Theme.tmTheme', 'expected': False},
            {'file': 'foo/bar/file.py', 'expected': False},
            {'file': 'bar/README.md', 'expected': False},
            {'file': '/a/long/path/file.txt', 'expected': True},
            {'file': '/User/Settings/SyncSettings.sublime-settings', 'expected': False},
            {'file': '/User/Settings/Package Control.sublime-settings', 'expected': True},
        ]

        for test in tests:
            self.assertEqual(
                test['expected'],
                manager.should_include(test['file']),
                'comparing: {}'.format(test['file'])
            )

    def test_get_content(self):
        create_file('empty.txt')
        create_file('plain.txt', content='content')

        tests = [
            {'file': 'empty.txt', 'expected': ''},
            {'file': 'not-found.txt', 'expected': ''},
            {'file': 'plain.txt', 'expected': 'content'},
        ]

        for test in tests:
            self.assertEqual(manager.get_content(test['file']), test['expected'])

        delete_file('empty.txt')
        delete_file('plain.txt')

    @mock.patch('sync_settings.sync_manager.path.exists', mock.MagicMock(return_value=True))
    def test_get_content_with_exception(self):
        self.assertEqual(manager.get_content('file.error'), '')
