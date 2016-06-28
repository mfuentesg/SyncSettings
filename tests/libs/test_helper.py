# # -*- coding: utf-8 -*-
import os
import shutil
from sync_settings.libs.helper import Helper
from tests import test_file_path
from unittest import TestCase

class TestHelper(TestCase):
  base_path = Helper.join_path(os.getcwd(), 'tests')

  def test_merge_objects(self):
    base_object = {'a': 'b', 'b': 'a'}
    update_object = {'a': 'a', 'b': 'b', 'c': 'c'}

    result = Helper.merge_objects({}, {})
    self.assertDictEqual(result, {})

    result = Helper.merge_objects(base_object, {})
    self.assertDictEqual(result, base_object)

    result = Helper.merge_objects({}, base_object)
    self.assertDictEqual(result, base_object)

    result = Helper.merge_objects(base_object, update_object)
    self.assertDictEqual(result, update_object)

    result = Helper.merge_objects({}, {'a': 1}, {'b': 2}, {'c': 3})
    self.assertDictEqual(result, {'a': 1, 'b': 2, 'c': 3})

  def test_merge_lists(self):
    base_list = ['a', 'b']
    update_list = ['b', 'c']

    result = Helper.merge_lists([], [])
    self.assertListEqual(result, [])

    result = Helper.merge_lists(sorted(base_list), [])
    self.assertListEqual(sorted(result), sorted(base_list))

    result = Helper.merge_lists([], sorted(base_list))
    self.assertListEqual(sorted(result), sorted(base_list))

    result = Helper.merge_lists(sorted(base_list), sorted(update_list))
    self.assertListEqual(sorted(result), ['a', 'b', 'c'])

    result = Helper.merge_lists([], ['a'], ['b'], ['c'], ['d'])
    self.assertListEqual(sorted(result), ['a', 'b', 'c', 'd'])

  def test_difference(self):
    l = Helper.get_difference([1, 2, 3, 4], [1, 2, 3])
    self.assertEqual(len(l), 1)
    self.assertEqual(l[0], 4)

  def test_home_path(self):
    home_path = os.path.expanduser('~')
    self.assertEqual(Helper.join_path(home_path, 'foo'), Helper.get_home_path('foo'))
    self.assertEqual(home_path, Helper.get_home_path())
    #Wrong Cases
    self.assertEqual(home_path, Helper.get_home_path(None))
    self.assertEqual(home_path, Helper.get_home_path(1234))

  def test_exists_path(self):
    self.assertFalse(Helper.exists_path(test_file_path, True))
    with self.assertRaises(TypeError): Helper.exists_path()
    with self.assertRaises(TypeError): Helper.exists_path(isFolder=True)
    self.assertFalse(Helper.exists_path(self.base_path))
    self.assertTrue(Helper.exists_path(test_file_path))
    self.assertTrue(Helper.exists_path(self.base_path, True))

  def test_join_path(self):
    self.assertIsNotNone(Helper.join_path(''))
    self.assertIsNotNone(Helper.join_path('123', '1234'))

  def test_get_files(self):
    with self.assertRaises(TypeError): Helper.get_files()
    self.assertListEqual(Helper.get_files('t'), [])
    self.assertListEqual(Helper.get_files(1234), [])
    self.assertListEqual(Helper.get_files(1234), [])
    self.assertGreater(len(Helper.get_files(self.base_path)), 0)

    #Create a test folder structure
    os.makedirs(Helper.join_path(self.base_path, 'hello', 'world'))
    open(Helper.join_path(self.base_path, 'hello', 'foo.txt'), 'a').close()
    open(Helper.join_path(self.base_path, 'hello', 'bar.txt'), 'a').close()
    open(Helper.join_path(self.base_path, 'hello', 'world', 'foo.txt'), 'a').close()
    allFiles = sorted([
      Helper.join_path(self.base_path, 'hello', 'bar.txt'),
      Helper.join_path(self.base_path, 'hello', 'foo.txt'),
      Helper.join_path(self.base_path, 'hello', 'world', 'foo.txt')
    ])
    files = sorted(Helper.get_files(Helper.join_path(self.base_path, 'hello')))
    self.assertEqual(len(files), 3)
    self.assertListEqual(files, allFiles)
    shutil.rmtree(Helper.join_path(self.base_path, 'hello'))

  def test_match_with_folder(self):
    success_cases = [
      Helper.join_path(self.base_path, 'hello', 'foo.txt'),
      Helper.join_path(self.base_path, 'hello', 'world', 'bar.txt'),
      Helper.join_path(self.base_path, 'hello', 'world', 'anything.py'),
      Helper.join_path(self.base_path, 'hello', '.txt'),
      Helper.join_path(self.base_path, 'hello', '.py')
    ]

    wrong_cases = [
      Helper.join_path(self.base_path, 'hello2', 'foo.txt'),
      Helper.join_path(self.base_path, 'hello2', 'world', 'bar.txt'),
      Helper.join_path(self.base_path, 'hello2', 'world', 'anything.py'),
      Helper.join_path(self.base_path, 'hello2', '.txt'),
      Helper.join_path(self.base_path, 'hello2', '.py')
    ]

    self.assertFalse(Helper.match_with_folder(self.base_path, self.base_path))

    for s in success_cases:
      self.assertTrue(Helper.match_with_folder(s, Helper.join_path(
        self.base_path, 'hello'
      )))

    for w in wrong_cases:
      self.assertFalse(Helper.match_with_folder(w, Helper.join_path(
        self.base_path, 'hello'
      )))

  def test_match_with_filename(self):
    success_case = Helper.join_path(self.base_path, 'hello', 'world', 'file.foo')
    file_path = success_case

    wrong_cases = [
      Helper.join_path(self.base_path, 'hello', 'file.foo'),
      Helper.join_path(self.base_path, 'hello', 'world', 'bar.txt'),
      Helper.join_path(self.base_path, 'hello', '.txt'),
      Helper.join_path(self.base_path, 'hello', 'any_name', 'file.foo'),
      Helper.join_path(self.base_path, 'hello', 'world', 'file', '.foo')
    ]

    self.assertTrue(Helper.match_with_filename(success_case, file_path))

    for w in wrong_cases:
      self.assertFalse(Helper.match_with_filename(w, file_path))

  def test_match_with_extension(self):
    pattern = '.py'

    success_cases = [
      Helper.join_path(self.base_path, 'hello', '____foo', 'other', '.py'),
      Helper.join_path(self.base_path, 'hello', 'file.py'),
      Helper.join_path(self.base_path, 'hello', '.py'),
      Helper.join_path(self.base_path, 'hello', '...', 'another.python', 'file.py'),
      Helper.join_path(self.base_path, 'hello', '_file.python.___.__.py'),
      Helper.join_path(self.base_path, 'hello', 'other', 'folder', 'dot', 'py.py')
    ]

    wrong_cases = [
      Helper.join_path(self.base_path, 'hello', 'file.foo'),
      Helper.join_path(self.base_path, 'hello', 'world', 'bar.txt'),
      Helper.join_path(self.base_path, 'hello', '.txt'),
      Helper.join_path(self.base_path, 'hello', 'file.pypy'),
      Helper.join_path(self.base_path, 'hello', 'file.python'),
      Helper.join_path(self.base_path, 'hello', 'file.otherpy'),
      Helper.join_path(self.base_path, 'hello', '_.py', 'file.otherpy')
    ]

    for s in success_cases:
      self.assertTrue(Helper.match_with_extension(s, pattern))

    for w in wrong_cases:
      self.assertFalse(Helper.match_with_extension(w, pattern))

  def test_is_file_extension(self):
    success_cases = [
      '.DStore',
      '.DStore?',
      '.jpg',
      '.png',
      '.txt',
      '.Trashes'
    ]

    wrong_cases = [
      'SublimeLinter',
      'SublieCodeIntel',
      'file.jpg',
      'file.file.png',
      '_.txt'
    ]

    for s in success_cases:
      self.assertTrue(Helper.is_file_extension(s))

    for w in wrong_cases:
      self.assertFalse(Helper.is_file_extension(w))

  def test_exclude_files_by_patterns(self):
    #Assuming <../tests/foo> is <../User/>
    os.makedirs(Helper.join_path(self.base_path, 'foo', 'bar'))
    open(Helper.join_path(self.base_path, 'foo', 'foo.txt'), 'a').close()
    open(Helper.join_path(self.base_path, 'foo', 'bar.txt'), 'a').close()
    open(Helper.join_path(self.base_path, 'foo', 'bar', 'foo.txt'), 'a').close()
    open(Helper.join_path(self.base_path, 'foo', 'bar', 'foo.py'), 'a').close()

    files = Helper.get_files(Helper.join_path(self.base_path, 'foo'))

    #Unfiltered
    self.assertEqual(len(files), 4)
    self.assertListEqual(Helper.exclude_files_by_patterns(files, []), files)
    self.assertListEqual(Helper.exclude_files_by_patterns(files, ['.boo']), files)

    # By extension
    filteredFiles = Helper.exclude_files_by_patterns(files, ['.txt'])

    self.assertEqual(len(filteredFiles), 1)
    self.assertListEqual(filteredFiles, [
      Helper.join_path(self.base_path, 'foo', 'bar', 'foo.py')
    ])

    filteredFiles = sorted(Helper.exclude_files_by_patterns(files, ['.py']))
    self.assertEqual(len(filteredFiles), 3)
    self.assertListEqual(filteredFiles, sorted([
      Helper.join_path(self.base_path, 'foo', 'bar.txt'),
      Helper.join_path(self.base_path, 'foo', 'foo.txt'),
      Helper.join_path(self.base_path, 'foo', 'bar', 'foo.txt')
    ]))

    # By Filename
    filteredFiles = sorted(Helper.exclude_files_by_patterns(files, [
      Helper.join_path(self.base_path, 'foo', 'bar.txt')
    ]))

    self.assertEqual(len(filteredFiles), 3)
    self.assertListEqual(filteredFiles, sorted([
      Helper.join_path(self.base_path, 'foo', 'foo.txt'),
      Helper.join_path(self.base_path, 'foo', 'bar', 'foo.py'),
      Helper.join_path(self.base_path, 'foo', 'bar', 'foo.txt')
    ]))

    filteredFiles = sorted(Helper.exclude_files_by_patterns(files, [
      Helper.join_path(self.base_path, 'foo', 'bar.txt'),
      Helper.join_path(self.base_path, 'foo', 'foo.txt')
    ]))

    self.assertEqual(len(filteredFiles), 2)
    self.assertListEqual(filteredFiles, sorted([
      Helper.join_path(self.base_path, 'foo', 'bar', 'foo.py'),
      Helper.join_path(self.base_path, 'foo', 'bar', 'foo.txt')
    ]))

    # By folder
    filteredFiles = sorted(Helper.exclude_files_by_patterns(files, [
      Helper.join_path(self.base_path, 'foo', 'bar')
    ]))
    self.assertEqual(len(filteredFiles), 2)
    self.assertListEqual(filteredFiles, sorted([
      Helper.join_path(self.base_path, 'foo', 'bar.txt'),
      Helper.join_path(self.base_path, 'foo', 'foo.txt')
    ]))

    shutil.rmtree(Helper.join_path(self.base_path, 'foo'))

  def test_encode_path(self):
    self.assertIsNone(Helper.encode_path(""))
    with self.assertRaises(TypeError): Helper.encode_path()

    path = '/some/path with spaces/to/file.txt'
    encoded_path = '%2Fsome%2Fpath%20with%20spaces%2Fto%2Ffile.txt'
    self.assertNotEqual(Helper.encode_path(path), '/some/path%20with%20spaces/to/file.txt')
    self.assertEqual(Helper.encode_path(path), encoded_path)

  def test_decode_path(self):
    self.assertIsNone(Helper.decode_path(""))
    with self.assertRaises(TypeError): Helper.decode_path()

    path = '/some/path with spaces/to/file.txt'
    encoded_path = '%2Fsome%2Fpath%20with%20spaces%2Fto%2Ffile.txt'
    self.assertEqual(Helper.decode_path(encoded_path), path.replace('/', Helper.os_separator()))

  def test_os_separator(self):
    self.assertNotEqual(os.sep, '')
    self.assertEqual(os.sep, Helper.os_separator())

  def test_parse_to_os(self):
    paths = [
      'something/path\\to/test',
      'another\\something/path\\to/test'
    ]
    expected_paths = [
      Helper.join_path('something', 'path', 'to', 'test'),
      Helper.join_path('another', 'something', 'path', 'to', 'test')
    ]

    result = Helper.parse_to_os(paths)
    self.assertEqual(result, expected_paths)

  def test_create_empty_file(self):
    test_path = Helper.join_path(os.getcwd(), 'empty_file.txt')

    self.assertFalse(os.path.exists(test_path))
    Helper.create_empty_file(test_path)
    self.assertTrue(os.path.exists(test_path))
    self.assertEqual(os.path.getsize(test_path), 0)
    os.remove(test_path)
    self.assertFalse(os.path.exists(test_path))

  def test_write_to_file(self):
    test_filename = 'empty_file.txt'
    message = 'file content'
    file_path = Helper.join_path(os.getcwd(), test_filename)

    self.assertFalse(Helper.exists_path(file_path))
    Helper.write_to_file(file_path, message)

    self.assertTrue(os.path.exists(file_path))

    with open(file_path, 'r') as f:
      self.assertEqual(f.read().find(message), 0)

    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    file_path = Helper.join_path(os.getcwd(), 'some_path', 'sub_path', test_filename)

    Helper.write_to_file(file_path, message)
    self.assertTrue(os.path.exists(file_path))
    with open(file_path, 'r') as f:
      self.assertEqual(f.read().find(message), 0)
    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))
    shutil.rmtree(Helper.join_path(os.getcwd(), 'some_path'))

    os.makedirs(Helper.join_path(os.getcwd(), 'some_path'))

    file_path = Helper.join_path(os.getcwd(), 'some_path', 'sub_path', test_filename)

    Helper.write_to_file(file_path, message)
    self.assertTrue(os.path.exists(file_path))
    with open(file_path, 'r') as f:
      self.assertEqual(f.read().find(message), 0)
    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    shutil.rmtree(Helper.join_path(os.getcwd(), 'some_path'))

  def test_parse_patterns(self):
    patterns = ['.txt', '.py', 'foo', 'bar.py']
    expected = sorted([
      '.txt',
      '.py',
      Helper.join_path(self.base_path, 'foo'),
      Helper.join_path(self.base_path, 'bar.py')
    ])

    result = sorted(Helper.parse_patterns(patterns, self.base_path))
    self.assertListEqual(result, expected)

    patterns = sorted(['.foo', '.DStore', '.file.name'])
    expected = sorted(['.foo', '.DStore', Helper.join_path(self.base_path, '.file.name')])
    result = sorted(Helper.parse_patterns(patterns, self.base_path))
    self.assertListEqual(result, expected)

  def test_filter_files_by_patterns(self):
    #Assuming <../tests/foo> is <../User/>
    base_path = Helper.join_path(self.base_path, 'foo')

    os.makedirs(Helper.join_path(self.base_path, 'foo', 'bar'))
    open(Helper.join_path(base_path, 'foo.txt'), 'a').close()
    open(Helper.join_path(base_path, 'bar.rb'), 'a').close()
    open(Helper.join_path(base_path, 'bar', 'foo.txt'), 'a').close()
    open(Helper.join_path(base_path, 'bar', 'foo.py'), 'a').close()


    files = Helper.get_files(base_path)
    patterns = Helper.parse_patterns(['.rb', '.py'], base_path)
    expected = sorted([
      Helper.join_path(base_path, 'bar.rb'),
      Helper.join_path(base_path, 'bar', 'foo.py')
    ])
    filtered_files = sorted(Helper.filter_files_by_patterns(files, patterns))

    self.assertEqual(len(filtered_files), 2)
    self.assertListEqual(filtered_files, expected)

    patterns = Helper.parse_patterns(['bar/foo.txt'], base_path)
    expected = [Helper.join_path(base_path, 'bar', 'foo.txt')]
    filtered_files = sorted(Helper.filter_files_by_patterns(files, patterns))

    self.assertEqual(len(filtered_files), 1)
    self.assertListEqual(filtered_files, expected)

    shutil.rmtree(Helper.join_path(self.base_path, 'foo'))
