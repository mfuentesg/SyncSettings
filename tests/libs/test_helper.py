# # -*- coding: utf-8 -*-
import os
import shutil
from sync_settings.libs import helper
from tests import test_file_path
from unittest import TestCase

class TestHelper(TestCase):
  def test_difference(self):
    l = helper.get_difference([1, 2, 3, 4], [1, 2, 3])
    self.assertEqual(len(l), 1)
    self.assertEqual(l[0], 4)

  def test_home_path(self):
    home_path = os.path.expanduser('~')
    self.assertEqual(helper.join_path((home_path, 'foo')), helper.get_home_path('foo'))
    self.assertEqual(home_path, helper.get_home_path())
    #Wrong Cases
    self.assertEqual(home_path, helper.get_home_path(None))
    self.assertEqual(home_path, helper.get_home_path(1234))

  def test_exists_path(self):
    self.assertFalse(helper.exists_path(test_file_path, True))
    with self.assertRaises(TypeError): helper.exists_path()
    with self.assertRaises(TypeError): helper.exists_path(isFolder=True)
    self.assertFalse(helper.exists_path(helper.join_path((os.getcwd(), 'tests'))))
    self.assertTrue(helper.exists_path(test_file_path))
    self.assertTrue(helper.exists_path(helper.join_path((os.getcwd(), 'tests')), True))

  def test_join_path(self):
    self.assertIsNone(helper.join_path(''))
    self.assertIsNone(helper.join_path([]))
    self.assertIsNone(helper.join_path(1234))
    self.assertIsNone(helper.join_path(('')))
    self.assertIsNotNone(helper.join_path(('123', '1234')))

  def test_get_files(self):
    with self.assertRaises(TypeError): helper.get_files()
    self.assertListEqual(helper.get_files('t'), [])
    self.assertListEqual(helper.get_files(1234), [])
    self.assertListEqual(helper.get_files(1234), [])
    self.assertGreater(len(helper.get_files(helper.join_path((os.getcwd(), 'tests')))), 0)

    #Create a test folder structure
    os.makedirs(helper.join_path((os.getcwd(), 'tests', 'hello', 'world')))
    open(helper.join_path((os.getcwd(), 'tests', 'hello', 'foo.txt')), 'a').close()
    open(helper.join_path((os.getcwd(), 'tests', 'hello', 'bar.txt')), 'a').close()
    open(helper.join_path((os.getcwd(), 'tests', 'hello', 'world', 'foo.txt')), 'a').close()
    allFiles = sorted([
      helper.join_path((os.getcwd(), 'tests', 'hello', 'bar.txt')),
      helper.join_path((os.getcwd(), 'tests', 'hello', 'foo.txt')),
      helper.join_path((os.getcwd(), 'tests', 'hello', 'world', 'foo.txt'))
    ])
    files = sorted(helper.get_files(helper.join_path((os.getcwd(), 'tests', 'hello'))))
    self.assertEqual(len(files), 3)
    self.assertListEqual(files, allFiles)
    shutil.rmtree(helper.join_path((os.getcwd(), 'tests', 'hello')))

  def test_is_folder_pattern(self):
    file_path = helper.join_path((os.getcwd(), 'tests', 'hello', 'foo.txt'))
    folder_path = helper.join_path((os.getcwd(), 'tests', 'hello'))

    os.makedirs(folder_path)
    open(file_path, 'a').close()

    self.assertFalse(helper.is_folder_pattern(file_path, file_path))
    self.assertFalse(helper.is_folder_pattern(folder_path, folder_path))
    self.assertTrue(helper.is_folder_pattern(file_path, folder_path))

    shutil.rmtree(helper.join_path((os.getcwd(), 'tests', 'hello')))

  def test_exclude_files_by_patterns(self):
    #Assuming <../tests/foo> is <../User/>
    os.makedirs(helper.join_path((os.getcwd(), 'tests', 'foo', 'bar')))
    open(helper.join_path((os.getcwd(), 'tests', 'foo', 'foo.txt')), 'a').close()
    open(helper.join_path((os.getcwd(), 'tests', 'foo', 'bar.txt')), 'a').close()
    open(helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt')), 'a').close()
    open(helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py')), 'a').close()

    files = helper.get_files(helper.join_path((os.getcwd(), 'tests', 'foo')))

    #Unfiltered
    self.assertEqual(len(files), 4)
    self.assertListEqual(helper.exclude_files_by_patterns(files, []), files)
    self.assertListEqual(helper.exclude_files_by_patterns(files, ['.boo']), files)

    # By extension
    filteredFiles = helper.exclude_files_by_patterns(files, ['.txt'])

    self.assertEqual(len(filteredFiles), 1)
    self.assertListEqual(filteredFiles, [
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py'))
    ])

    filteredFiles = sorted(helper.exclude_files_by_patterns(files, ['.py']))
    self.assertEqual(len(filteredFiles), 3)
    self.assertListEqual(filteredFiles, sorted([
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar.txt')),
      helper.join_path((os.getcwd(), 'tests', 'foo', 'foo.txt')),
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt'))
    ]))

    # By Filename
    filteredFiles = sorted(helper.exclude_files_by_patterns(files, [
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar.txt'))
    ]))

    self.assertEqual(len(filteredFiles), 3)
    self.assertListEqual(filteredFiles, sorted([
      helper.join_path((os.getcwd(), 'tests', 'foo', 'foo.txt')),
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py')),
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt'))
    ]))

    filteredFiles = sorted(helper.exclude_files_by_patterns(files, [
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar.txt')),
      helper.join_path((os.getcwd(), 'tests', 'foo', 'foo.txt'))
    ]))

    self.assertEqual(len(filteredFiles), 2)
    self.assertListEqual(filteredFiles, sorted([
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py')),
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt'))
    ]))

    # By folder
    filteredFiles = sorted(helper.exclude_files_by_patterns(files, [
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar'))
    ]))
    self.assertEqual(len(filteredFiles), 2)
    self.assertListEqual(filteredFiles, sorted([
      helper.join_path((os.getcwd(), 'tests', 'foo', 'bar.txt')),
      helper.join_path((os.getcwd(), 'tests', 'foo', 'foo.txt'))
    ]))

    shutil.rmtree(helper.join_path((os.getcwd(), 'tests', 'foo')))

  def test_encode_path(self):
    self.assertIsNone(helper.encode_path(""))
    with self.assertRaises(TypeError): helper.encode_path()

    path = '/some/path with spaces/to/file.txt'
    encoded_path = '%2Fsome%2Fpath%20with%20spaces%2Fto%2Ffile.txt'
    self.assertNotEqual(helper.encode_path(path), '/some/path%20with%20spaces/to/file.txt')
    self.assertEqual(helper.encode_path(path), encoded_path)

  def test_decode_path(self):
    self.assertIsNone(helper.decode_path(""))
    with self.assertRaises(TypeError): helper.decode_path()

    path = '/some/path with spaces/to/file.txt'
    encoded_path = '%2Fsome%2Fpath%20with%20spaces%2Fto%2Ffile.txt'
    self.assertEqual(helper.decode_path(encoded_path), path.replace('/', helper.os_separator()))

  def test_os_separator(self):
    self.assertNotEqual(os.sep, '')
    self.assertEqual(os.sep, helper.os_separator())

  def test_parse_to_os(self):
    paths = [
      'something/path\\to/test',
      'another\\something/path\\to/test'
    ]
    expected_paths = [
      helper.join_path(('something', 'path', 'to', 'test')),
      helper.join_path(('another', 'something', 'path', 'to', 'test'))
    ]

    result = helper.parse_to_os(paths)
    self.assertEqual(result, expected_paths)

  def test_create_empty_file(self):
    test_path = helper.join_path((os.getcwd(), 'empty_file.txt'))
    self.assertFalse(os.path.exists(test_path))
    helper.create_empty_file(test_path)
    self.assertTrue(os.path.exists(test_path))
    self.assertEqual(os.path.getsize(test_path), 0)
    os.remove(test_path)
    self.assertFalse(os.path.exists(test_path))

  def test_write_to_file(self):
    test_filename = 'empty_file.txt'
    message = 'file content'

    file_path = helper.join_path((os.getcwd(), test_filename))
    self.assertFalse(helper.exists_path(file_path))
    helper.write_to_file(file_path, message)

    self.assertTrue(os.path.exists(file_path))

    with open(file_path, 'r') as f:
      self.assertEqual(f.read().find(message), 0)
    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    file_path = helper.join_path((os.getcwd(), 'some_path', 'sub_path', test_filename))
    helper.write_to_file(file_path, message)
    self.assertTrue(os.path.exists(file_path))
    with open(file_path, 'r') as f:
      self.assertEqual(f.read().find(message), 0)
    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))
    shutil.rmtree(helper.join_path((os.getcwd(), 'some_path')))

    os.makedirs(helper.join_path((os.getcwd(), 'some_path')))

    file_path = helper.join_path((os.getcwd(), 'some_path', 'sub_path', test_filename))
    helper.write_to_file(file_path, message)
    self.assertTrue(os.path.exists(file_path))
    with open(file_path, 'r') as f:
      self.assertEqual(f.read().find(message), 0)
    os.remove(file_path)
    self.assertFalse(os.path.exists(file_path))

    shutil.rmtree(helper.join_path((os.getcwd(), 'some_path')))
