import unittest

import os
import mock
import shutil
from ..libs import path


class TestPath(unittest.TestCase):
    def create_folder(self, p):
        self.delete_folder(p)
        os.makedirs(p)

    @staticmethod
    def delete_folder(p):
        if os.path.exists(p):
            shutil.rmtree(p)

    def test_join(self):
        tests = [
            {'paths': [], 'expected': ''},
            {'paths': [''], 'expected': ''},
            {'paths': ['', ''], 'expected': ''},
            {'paths': ['a', ''], 'expected': os.path.join('a', '')},
            {'paths': ['', 'a'], 'expected': 'a'},
            {'paths': ['a', 'b'], 'expected': os.path.join('a', 'b')},
        ]
        for test in tests:
            self.assertEqual(test['expected'], path.join(*test['paths']))

    def test_encode(self):
        tests = [
            {'text': 'text', 'expected': 'text'},
            {'text': 'my-text', 'expected': 'my-text'},
            {'text': 'my text', 'expected': 'my%20text'},
            {'text': 'my/text', 'expected': 'my%2Ftext'},
            {'text': '/my/text', 'expected': '%2Fmy%2Ftext'},
            {'text': '/my\\text', 'expected': '%2Fmy%2Ftext'},
        ]
        for test in tests:
            self.assertEqual(test['expected'], path.encode(test['text']))

    def test_decode(self):
        tests = [
            {'expected': 'text', 'text': 'text'},
            {'expected': 'my-text', 'text': 'my-text'},
            {'expected': 'my text', 'text': 'my%20text'},
            {'expected': 'my/text', 'text': 'my%2Ftext'},
            {'expected': '/my/text', 'text': '%2Fmy%2Ftext'},
        ]
        for test in tests:
            self.assertEqual(test['expected'], path.decode(test['text']))

    @mock.patch('platform.system', mock.MagicMock(return_value='Windows'))
    def test_separator_windows(self):
        self.assertEqual(path.separator(), '\\')

    def test_separator_unix(self):
        self.assertEqual(path.separator(), '/')

    @mock.patch('platform.system', mock.MagicMock(return_value='Windows'))
    def test_os_path_windows(self):
        def my_func():
            return 'C:/my/windows/path/file.txt'
        self.assertEqual('C:\\my\\windows\\path\\file.txt', path.os_path(my_func)())

    def test_os_path_unix(self):
        def my_func():
            return 'C:/my/windows/path/file.txt'
        self.assertEqual('C:/my/windows/path/file.txt', path.os_path(my_func)())

    def test_exists_path(self):
        folder_path = os.path.abspath(os.path.dirname(__file__))

        self.assertFalse(path.exists(folder_path))
        self.assertFalse(path.exists(path.join(folder_path, __file__), True))
        self.assertFalse(path.exists('/unexistent/folder', True))
        self.assertFalse(path.exists('/unexistent/folder', True))

        self.assertTrue(path.exists(folder_path, True))
        self.assertTrue(path.exists(path.join(folder_path, __file__)))

    def test_list_files(self):
        self.assertEqual(len(path.list_files(path.join('unexistent', 'path'))), 0)
        self.assertListEqual(path.list_files(path.join('unexistent', 'path')), [])

        folder_path = os.path.abspath(os.path.dirname(__file__))
        base_path = path.join(folder_path, 'foo')
        self.create_folder(path.join(folder_path, 'foo', 'bar'))
        paths = [
            ['foo.txt'],
            ['bar.rb'],
            ['bar', 'foo.txt'],
            ['bar', 'foo.py'],
            ['bar', 'main.go'],
            ['bar', 'other.go'],
        ]

        for p in paths:
            with open(path.join(base_path, *p), 'a') as f:
                f.close()

        files = path.list_files(base_path)
        self.assertEqual(6, len(files))
        expected = [
            path.join(folder_path, 'foo', 'bar.rb'),
            path.join(folder_path, 'foo', 'foo.txt'),
            path.join(folder_path, 'foo', 'bar', 'other.go'),
            path.join(folder_path, 'foo', 'bar', 'foo.txt'),
            path.join(folder_path, 'foo', 'bar', 'foo.py'),
            path.join(folder_path, 'foo', 'bar', 'main.go'),
        ]
        self.assertListEqual(sorted(expected), sorted(files))
        self.delete_folder(base_path)
