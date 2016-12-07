# # -*- coding: utf-8 -*-
import os
import shutil
from sync_settings.libs.utils import Utils
from tests import test_file_path
from unittest import TestCase

class TestUtils(TestCase):
  base_path = Utils.join_path(os.getcwd(), 'tests')

  def create_folder(self, path):
    self.delete_folder(path)
    os.makedirs(path)

  def delete_folder(self, path):
    if os.path.exists(path):
      shutil.rmtree(path)

  def test_merge_objects(self):
    base_object = {'a': 'b', 'b': 'a'}
    update_object = {'a': 'a', 'b': 'b', 'c': 'c'}

    result = Utils.merge_objects({}, {})
    self.assertDictEqual(result, {})

    result = Utils.merge_objects(base_object, {})
    self.assertDictEqual(result, base_object)

    result = Utils.merge_objects({}, base_object)
    self.assertDictEqual(result, base_object)

    result = Utils.merge_objects(base_object, update_object)
    self.assertDictEqual(result, update_object)

    result = Utils.merge_objects({}, {'a': 1}, {'b': 2}, {'c': 3})
    self.assertDictEqual(result, {'a': 1, 'b': 2, 'c': 3})

  def test_merge_lists(self):
    base_list = ['a', 'b']
    update_list = ['b', 'c']

    result = Utils.merge_lists([], [])
    self.assertListEqual(result, [])

    result = Utils.merge_lists(sorted(base_list), [])
    self.assertListEqual(sorted(result), sorted(base_list))

    result = Utils.merge_lists([], sorted(base_list))
    self.assertListEqual(sorted(result), sorted(base_list))

    result = Utils.merge_lists(sorted(base_list), sorted(update_list))
    self.assertListEqual(sorted(result), ['a', 'b', 'c'])

    result = Utils.merge_lists([], ['a'], ['b'], ['c'], ['d'])
    self.assertListEqual(sorted(result), ['a', 'b', 'c', 'd'])

  def test_difference(self):
    l = Utils.get_difference([1, 2, 3, 4], [1, 2, 3])
    self.assertEqual(len(l), 1)
    self.assertEqual(l[0], 4)

  def test_home_path(self):
    home_path = os.path.expanduser('~')
    self.assertEqual(Utils.join_path(home_path, 'foo'), Utils.get_home_path('foo'))
    self.assertEqual(home_path, Utils.get_home_path())
    #Wrong Cases
    self.assertEqual(home_path, Utils.get_home_path(None))
    self.assertEqual(home_path, Utils.get_home_path(1234))

  def test_exists_path(self):
    self.assertFalse(Utils.exists_path(test_file_path, True))
    with self.assertRaises(TypeError): Utils.exists_path()
    with self.assertRaises(TypeError): Utils.exists_path(isFolder=True)
    self.assertFalse(Utils.exists_path(self.base_path))
    self.assertTrue(Utils.exists_path(test_file_path))
    self.assertTrue(Utils.exists_path(self.base_path, True))

  def test_join_path(self):
    self.assertIsNotNone(Utils.join_path(''))
    self.assertIsNotNone(Utils.join_path('123', '1234'))

  def test_get_files(self):
    with self.assertRaises(TypeError): Utils.get_files()
    self.assertListEqual(Utils.get_files('t'), [])
    self.assertListEqual(Utils.get_files(1234), [])
    self.assertListEqual(Utils.get_files(1234), [])
    self.assertGreater(len(Utils.get_files(self.base_path)), 0)

    #Create a test folder structure
    self.create_folder(Utils.join_path(self.base_path, 'hello', 'world'))
    open(Utils.join_path(self.base_path, 'hello', 'foo.txt'), 'a').close()
    open(Utils.join_path(self.base_path, 'hello', 'bar.txt'), 'a').close()
    open(Utils.join_path(self.base_path, 'hello', 'world', 'foo.txt'), 'a').close()
    allFiles = sorted([
      Utils.join_path(self.base_path, 'hello', 'bar.txt'),
      Utils.join_path(self.base_path, 'hello', 'foo.txt'),
      Utils.join_path(self.base_path, 'hello', 'world', 'foo.txt')
    ])
    files = sorted(Utils.get_files(Utils.join_path(self.base_path, 'hello')))
    self.assertEqual(len(files), 3)
    self.assertListEqual(files, allFiles)
    self.delete_folder(Utils.join_path(self.base_path, 'hello'))

  def test_match_with_folder(self):
    success_cases = [
      Utils.join_path(self.base_path, 'hello', 'foo.txt'),
      Utils.join_path(self.base_path, 'hello', 'world', 'bar.txt'),
      Utils.join_path(self.base_path, 'hello', 'world', 'anything.py'),
      Utils.join_path(self.base_path, 'hello', '.txt'),
      Utils.join_path(self.base_path, 'hello', '.py')
    ]

    wrong_cases = [
      Utils.join_path(self.base_path, 'hello2', 'foo.txt'),
      Utils.join_path(self.base_path, 'hello2', 'world', 'bar.txt'),
      Utils.join_path(self.base_path, 'hello2', 'world', 'anything.py'),
      Utils.join_path(self.base_path, 'hello2', '.txt'),
      Utils.join_path(self.base_path, 'hello2', '.py')
    ]

    self.assertFalse(Utils.match_with_folder(self.base_path, self.base_path))

    for s in success_cases:
      self.assertTrue(Utils.match_with_folder(s, Utils.join_path(
        self.base_path, 'hello'
      )))

    for w in wrong_cases:
      self.assertFalse(Utils.match_with_folder(w, Utils.join_path(
        self.base_path, 'hello'
      )))

  def test_match_with_filename(self):
    success_case = Utils.join_path(self.base_path, 'hello', 'world', 'file.foo')
    file_path = success_case

    wrong_cases = [
      Utils.join_path(self.base_path, 'hello', 'file.foo'),
      Utils.join_path(self.base_path, 'hello', 'world', 'bar.txt'),
      Utils.join_path(self.base_path, 'hello', '.txt'),
      Utils.join_path(self.base_path, 'hello', 'any_name', 'file.foo'),
      Utils.join_path(self.base_path, 'hello', 'world', 'file', '.foo')
    ]

    self.assertTrue(Utils.match_with_filename(success_case, file_path))

    for w in wrong_cases:
      self.assertFalse(Utils.match_with_filename(w, file_path))

  def test_match_with_willcard(self):
    pattern = Utils.join_path(self.base_path, 'packages', 'Package Control.cache*')
    success_cases = [
      Utils.join_path(self.base_path, 'packages', 'Package Control.cache123123'),
      Utils.join_path(self.base_path, 'packages', 'Package Control.cache'),
      Utils.join_path(self.base_path, 'packages', 'Package Control.cached'),
      Utils.join_path(self.base_path, 'packages', 'Package Control.cache-any-pattern')
    ]

    wrong_cases = [
      Utils.join_path(self.base_path, 'packages', 'Package Cntrol.cache123123'),
      Utils.join_path(self.base_path, 'packages', 'Package Control.cach123123'),
      Utils.join_path(self.base_path, 'packages', 'Package.cache'),
      Utils.join_path(self.base_path, 'packages', 'Package', '.cache'),
      Utils.join_path(self.base_path, 'packages', 'Package', ' Control', '.cache'),
      Utils.join_path(self.base_path, 'packages', 'any', 'directory', 'Package Control.cache')
    ]

    for w in wrong_cases:
      self.assertFalse(Utils.match_with_willcard(w, pattern))

    for s in success_cases:
      self.assertTrue(Utils.match_with_willcard(s, pattern))

  def test_match_with_extension(self):
    pattern = '.py'

    success_cases = [
      Utils.join_path(self.base_path, 'hello', '____foo', 'other', '.py'),
      Utils.join_path(self.base_path, 'hello', 'file.py'),
      Utils.join_path(self.base_path, 'hello', '.py'),
      Utils.join_path(self.base_path, 'hello', '...', 'another.python', 'file.py'),
      Utils.join_path(self.base_path, 'hello', '_file.python.___.__.py'),
      Utils.join_path(self.base_path, 'hello', 'other', 'folder', 'dot', 'py.py')
    ]

    wrong_cases = [
      Utils.join_path(self.base_path, 'hello', 'file.foo'),
      Utils.join_path(self.base_path, 'hello', 'world', 'bar.txt'),
      Utils.join_path(self.base_path, 'hello', '.txt'),
      Utils.join_path(self.base_path, 'hello', 'file.pypy'),
      Utils.join_path(self.base_path, 'hello', 'file.python'),
      Utils.join_path(self.base_path, 'hello', 'file.otherpy'),
      Utils.join_path(self.base_path, 'hello', '_.py', 'file.otherpy')
    ]

    for s in success_cases:
      self.assertTrue(Utils.match_with_extension(s, pattern))

    for w in wrong_cases:
      self.assertFalse(Utils.match_with_extension(w, pattern))

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
      self.assertTrue(Utils.is_file_extension(s))

    for w in wrong_cases:
      self.assertFalse(Utils.is_file_extension(w))

  def test_exclude_files_by_patterns(self):
    #Assuming <../tests/foo> is <../User/>
    self.create_folder(Utils.join_path(self.base_path, 'foo', 'bar'))
    open(Utils.join_path(self.base_path, 'foo', 'foo.txt'), 'a').close()
    open(Utils.join_path(self.base_path, 'foo', 'bar.txt'), 'a').close()
    open(Utils.join_path(self.base_path, 'foo', 'bar', 'foo.txt'), 'a').close()
    open(Utils.join_path(self.base_path, 'foo', 'bar', 'foo.py'), 'a').close()
    open(Utils.join_path(self.base_path, 'foo', 'bar', 'file.go'), 'a').close()
    open(Utils.join_path(self.base_path, 'foo', 'bar', 'new_file.go'), 'a').close()

    files = sorted(Utils.get_files(Utils.join_path(self.base_path, 'foo')))

    #Unfiltered
    self.assertEqual(len(files), 6)
    self.assertListEqual(sorted(Utils.exclude_files_by_patterns(files, [])), files)
    self.assertListEqual(sorted(Utils.exclude_files_by_patterns(files, ['.boo'])), files)

    # By extension
    filteredFiles = Utils.exclude_files_by_patterns(files, ['.txt'])

    self.assertEqual(len(filteredFiles), 3)
    self.assertListEqual(filteredFiles, sorted([
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.py'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'file.go'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'new_file.go')
    ]))

    filteredFiles = sorted(Utils.exclude_files_by_patterns(files, ['.py']))
    self.assertEqual(len(filteredFiles), 5)
    self.assertListEqual(filteredFiles, sorted([
      Utils.join_path(self.base_path, 'foo', 'bar.txt'),
      Utils.join_path(self.base_path, 'foo', 'foo.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'file.go'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'new_file.go')
    ]))

    # By Filename
    filteredFiles = sorted(Utils.exclude_files_by_patterns(files, [
      Utils.join_path(self.base_path, 'foo', 'bar.txt')
    ]))

    self.assertEqual(len(filteredFiles), 5)
    self.assertListEqual(filteredFiles, sorted([
      Utils.join_path(self.base_path, 'foo', 'foo.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.py'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'file.go'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'new_file.go')
    ]))

    filteredFiles = sorted(Utils.exclude_files_by_patterns(files, [
      Utils.join_path(self.base_path, 'foo', 'bar.txt'),
      Utils.join_path(self.base_path, 'foo', 'foo.txt')
    ]))

    self.assertEqual(len(filteredFiles), 4)
    self.assertListEqual(filteredFiles, sorted([
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.py'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'file.go'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'new_file.go')
    ]))

    # By folder
    filteredFiles = sorted(Utils.exclude_files_by_patterns(files, [
      Utils.join_path(self.base_path, 'foo', 'bar')
    ]))
    self.assertEqual(len(filteredFiles), 2)
    self.assertListEqual(filteredFiles, sorted([
      Utils.join_path(self.base_path, 'foo', 'bar.txt'),
      Utils.join_path(self.base_path, 'foo', 'foo.txt'),
    ]))

    # By willcard
    filteredFiles = sorted(Utils.exclude_files_by_patterns(files, [
      Utils.join_path(self.base_path, 'foo', '**', '*.go')
    ]))

    self.assertEqual(len(filteredFiles), 4)
    self.assertListEqual(filteredFiles, sorted([
      Utils.join_path(self.base_path, 'foo', 'foo.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.txt'),
      Utils.join_path(self.base_path, 'foo', 'bar', 'foo.py')
    ]))


    self.delete_folder(Utils.join_path(self.base_path, 'foo'))

  def test_encode_path(self):
    self.assertIsNone(Utils.encode_path(""))
    with self.assertRaises(TypeError): Utils.encode_path()

    path = '/some/path with spaces/to/file.txt'
    encoded_path = '%2Fsome%2Fpath%20with%20spaces%2Fto%2Ffile.txt'
    self.assertNotEqual(Utils.encode_path(path), '/some/path%20with%20spaces/to/file.txt')
    self.assertEqual(Utils.encode_path(path), encoded_path)

  def test_decode_path(self):
    self.assertIsNone(Utils.decode_path(""))
    with self.assertRaises(TypeError): Utils.decode_path()

    path = '/some/path with spaces/to/file.txt'
    encoded_path = '%2Fsome%2Fpath%20with%20spaces%2Fto%2Ffile.txt'
    self.assertEqual(Utils.decode_path(encoded_path), path.replace('/', Utils.os_separator()))

  def test_os_separator(self):
    self.assertNotEqual(os.sep, '')
    self.assertEqual(os.sep, Utils.os_separator())

  def test_parse_to_os(self):
    paths = [
      'something/path\\to/test',
      'another\\something/path\\to/test'
    ]
    expected_paths = [
      Utils.join_path('something', 'path', 'to', 'test'),
      Utils.join_path('another', 'something', 'path', 'to', 'test')
    ]

    result = Utils.parse_to_os(paths)
    self.assertEqual(result, expected_paths)

  def test_create_empty_file(self):
    test_path = Utils.join_path(os.getcwd(), 'empty_file.txt')

    self.assertFalse(os.path.exists(test_path))
    Utils.create_empty_file(test_path)
    self.assertTrue(os.path.exists(test_path))
    self.assertEqual(os.path.getsize(test_path), 0)
    os.remove(test_path)
    self.assertFalse(os.path.exists(test_path))

  def test_write_to_file(self):
    test_filename = 'empty_file.txt'
    message = 'file content'
    file_path = Utils.join_path(os.getcwd(), test_filename)

    self.assertFalse(Utils.exists_path(file_path))
    Utils.write_to_file(file_path, message)

    self.assertTrue(os.path.exists(file_path))

    with open(file_path, 'rb') as f:
      self.assertEqual(f.read().decode('utf-8').find(message), 0)

    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    file_path = Utils.join_path(os.getcwd(), 'some_path', 'sub_path', test_filename)

    Utils.write_to_file(file_path, message)
    self.assertTrue(os.path.exists(file_path))
    with open(file_path, 'rb') as f:
      self.assertEqual(f.read().decode('utf-8').find(message), 0)
    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    self.create_folder(Utils.join_path(os.getcwd(), 'some_path'))

    file_path = Utils.join_path(os.getcwd(), 'some_path', 'sub_path', test_filename)

    Utils.write_to_file(file_path, message)
    self.assertTrue(os.path.exists(file_path))
    with open(file_path, 'rb') as f:
      self.assertEqual(f.read().decode('utf-8').find(message), 0)
    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    Utils.write_to_file(file_path, {"some": "content"}, action='a+', as_json=True)
    self.assertTrue(os.path.exists(file_path))
    with open(file_path, 'rb') as f:
      self.assertEqual(f.read().decode('utf-8'), '{"some": "content"}')

    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    self.delete_folder(Utils.join_path(os.getcwd(), 'some_path'))

  def test_parse_patterns(self):
    patterns = ['.txt', '.py', 'foo', 'bar.py', '*.go']
    expected = sorted([
      '.txt',
      '.py',
      Utils.join_path(self.base_path, 'foo'),
      Utils.join_path(self.base_path, 'bar.py'),
      Utils.join_path(self.base_path, '*.go')
    ])

    result = sorted(Utils.parse_patterns(patterns, self.base_path))
    self.assertListEqual(result, expected)

    patterns = sorted(['.foo', '.DStore', '.file.name', '**/*.txt'])
    expected = sorted([
      '.foo',
      '.DStore',
      Utils.join_path(self.base_path, '.file.name'),
      Utils.join_path(self.base_path, '**/*.txt')
    ])
    result = sorted(Utils.parse_patterns(patterns, self.base_path))
    self.assertListEqual(result, expected)

  def test_filter_files_by_patterns(self):
    #Assuming <../tests/foo> is <../User/>
    base_path = Utils.join_path(self.base_path, 'foo')

    self.create_folder(Utils.join_path(self.base_path, 'foo', 'bar'))
    open(Utils.join_path(base_path, 'foo.txt'), 'a').close()
    open(Utils.join_path(base_path, 'bar.rb'), 'a').close()
    open(Utils.join_path(base_path, 'bar', 'foo.txt'), 'a').close()
    open(Utils.join_path(base_path, 'bar', 'foo.py'), 'a').close()
    open(Utils.join_path(base_path, 'bar', 'main.go'), 'a').close()
    open(Utils.join_path(base_path, 'bar', 'other.go'), 'a').close()

    files = Utils.get_files(base_path)
    patterns = Utils.parse_patterns([
      '.rb',
      '.py',
      Utils.join_path('bar', '*.go')
    ], base_path)

    expected = sorted([
      Utils.join_path(base_path, 'bar.rb'),
      Utils.join_path(base_path, 'bar', 'foo.py'),
      Utils.join_path(base_path, 'bar', 'main.go'),
      Utils.join_path(base_path, 'bar', 'other.go')
    ])

    filtered_files = sorted(Utils.filter_files_by_patterns(files, patterns))

    self.assertEqual(len(filtered_files), 4)
    self.assertListEqual(filtered_files, expected)

    patterns = Utils.parse_patterns(['bar/foo.txt'], base_path)
    expected = [Utils.join_path(base_path, 'bar', 'foo.txt')]
    filtered_files = sorted(Utils.filter_files_by_patterns(files, patterns))

    self.assertEqual(len(filtered_files), 1)
    self.assertListEqual(filtered_files, expected)

    self.delete_folder(Utils.join_path(self.base_path, 'foo'))

  def test_get_file_content(self):
    test_path = Utils.join_path(os.getcwd(), 'empty_file.json')

    Utils.create_empty_file(test_path)
    Utils.write_to_file(test_path,'Some content')
    file_content = Utils.get_file_content(test_path)

    self.assertEqual(file_content, 'Some content')

    os.remove(test_path)
    self.assertFalse(os.path.exists(test_path))
