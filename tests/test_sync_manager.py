import unittest
import mock
from sync_settings import sync_manager as manager


class TestSyncManager(unittest.TestCase):
    def test_should_exclude_sync_settings_file(self):
        self.assertTrue(manager.should_exclude('/User/Settings/SyncSettings.sublime-settings'))

    @mock.patch('sync_settings.libs.settings.get', mock.MagicMock(return_value=[
        '*Package Control.sublime-settings',
        '*.txt',
        'foo/**/*.py',
        'bar/*.py',
        'bar/*.md',
    ]))
    def test_should_exclude_with_patterns(self):
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

    def test_should_include(self):
        pass
