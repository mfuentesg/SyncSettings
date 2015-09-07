# -*- coding: utf-8 -*-

from unittest import TestCase
from tests import *
import os, shutil, re

class TestHelper (TestCase):
  def test_difference (self):
    l = helper.getDifference([1, 2, 3, 4], [1, 2, 3])
    self.assertEqual(len(l), 1)
    self.assertEqual(l[0], 4)

  def test_home_path (self):
    homePath = os.path.expanduser('~')
    self.assertEqual(helper.joinPath((homePath, 'foo')), helper.getHomePath('foo'))
    self.assertEqual(homePath, helper.getHomePath())
    #Wrong Cases
    self.assertEqual(homePath, helper.getHomePath(None))
    self.assertEqual(homePath, helper.getHomePath(1234))

  def test_exists_path (self):
    self.assertFalse(helper.existsPath(optionsPath, True))
    with self.assertRaises(TypeError):
      helper.existsPath()
    with self.assertRaises(TypeError):
      helper.existsPath(isFolder=True)
    self.assertFalse(helper.existsPath(helper.joinPath((os.getcwd(), 'tests'))))
    self.assertTrue(helper.existsPath(optionsPath))
    self.assertTrue(helper.existsPath(helper.joinPath((os.getcwd(), 'tests')), True))

  def test_join_path (self):
    self.assertIsNone(helper.joinPath(''))
    self.assertIsNone(helper.joinPath([]))
    self.assertIsNone(helper.joinPath(1234))
    self.assertIsNone(helper.joinPath(('')))
    self.assertIsNotNone(helper.joinPath(('123', '1234')))

  def test_get_files (self):
    with self.assertRaises(TypeError):
      helper.getFiles()
    self.assertListEqual(helper.getFiles('t'), [])
    self.assertListEqual(helper.getFiles(1234), [])
    self.assertListEqual(helper.getFiles(1234), [])
    self.assertGreater(len(helper.getFiles(helper.joinPath((os.getcwd(), 'tests')))), 0)

    #Create a test folder structure
    os.makedirs(helper.joinPath((os.getcwd(), 'tests', 'hello', 'world')), exist_ok=True)
    open(helper.joinPath((os.getcwd(), 'tests', 'hello', 'foo.txt')), 'a').close()
    open(helper.joinPath((os.getcwd(), 'tests', 'hello', 'bar.txt')), 'a').close()
    open(helper.joinPath((os.getcwd(), 'tests', 'hello', 'world', 'foo.txt')), 'a').close()
    allFiles = [
      helper.joinPath((os.getcwd(), 'tests', 'hello', 'bar.txt')),
      helper.joinPath((os.getcwd(), 'tests', 'hello', 'foo.txt')),
      helper.joinPath((os.getcwd(), 'tests', 'hello', 'world', 'foo.txt'))
    ]
    files = helper.getFiles(helper.joinPath((os.getcwd(), 'tests', 'hello')))
    self.assertEqual(len(files), 3)
    self.assertListEqual(files, allFiles)
    shutil.rmtree(helper.joinPath((os.getcwd(), 'tests', 'hello')))

  def test_filter_by_patterns (self):
    os.makedirs(helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar')), exist_ok=True)
    open(helper.joinPath((os.getcwd(), 'tests', 'foo', 'foo.txt')), 'a').close()
    open(helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar.txt')), 'a').close()
    open(helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt')), 'a').close()
    open(helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py')), 'a').close()

    files = helper.getFiles(helper.joinPath((os.getcwd(), 'tests', 'foo')))

    #Unfiltered
    self.assertListEqual(helper.excludeByPatterns(files, []), files)
    self.assertListEqual(helper.excludeByPatterns(files, ['.boo']), files)

    # By extension
    filteredFiles = helper.excludeByPatterns(files, ['.txt'])

    self.assertEqual(len(filteredFiles), 1)
    self.assertListEqual(filteredFiles, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py'))
    ])

    filteredFiles = helper.excludeByPatterns(files, ['.py'])
    self.assertEqual(len(filteredFiles), 3)
    self.assertListEqual(filteredFiles, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar.txt')),
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'foo.txt')),
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt'))
    ])

    # By Filename
    filteredFiles = helper.excludeByPatterns(files, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar.txt'))
    ])

    self.assertEqual(len(filteredFiles), 3)
    self.assertListEqual(filteredFiles, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'foo.txt')),
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py')),
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt'))
    ])

    filteredFiles = helper.excludeByPatterns(files, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar.txt')),
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'foo.txt'))
    ])

    self.assertEqual(len(filteredFiles), 2)
    self.assertListEqual(filteredFiles, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.py')),
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar', 'foo.txt'))
    ])

    # By folder
    filteredFiles = helper.excludeByPatterns(files, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar'))
    ])
    self.assertEqual(len(filteredFiles), 2)
    self.assertListEqual(filteredFiles, [
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'bar.txt')),
      helper.joinPath((os.getcwd(), 'tests', 'foo', 'foo.txt'))
    ])

    shutil.rmtree(helper.joinPath((os.getcwd(), 'tests', 'foo')))
