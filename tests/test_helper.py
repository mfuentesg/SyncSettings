# -*- coding: utf-8 -*-

from unittest import TestCase
from tests import *
import os, shutil

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
    self.assertFalse(helper.existsPath(isFolder=True))
    self.assertFalse(helper.existsPath(optionsPath, True))
    self.assertFalse(helper.existsPath())
    self.assertFalse(helper.existsPath('tests'))
    self.assertTrue(helper.existsPath(optionsPath))
    self.assertTrue(helper.existsPath('tests', True))

  def test_join_path (self):
    self.assertIsNone(helper.joinPath(''))
    self.assertIsNone(helper.joinPath([]))
    self.assertIsNone(helper.joinPath(1234))
    self.assertIsNone(helper.joinPath(('')))
    self.assertIsNotNone(helper.joinPath(('123', '1234')))

  def test_get_files (self):
    self.assertListEqual(helper.getFiles(), [])
    self.assertListEqual(helper.getFiles('t'), [])
    self.assertListEqual(helper.getFiles(1234), [])
    self.assertListEqual(helper.getFiles(1234), [])
    self.assertGreater(len(helper.getFiles('tests')), 0)

    #Create a test folder structure
    os.makedirs(helper.joinPath(('tests', 'hello', 'world')), exist_ok=True)
    open(helper.joinPath(('tests', 'hello', 'foo.txt')), 'a').close()
    open(helper.joinPath(('tests', 'hello', 'bar.txt')), 'a').close()
    open(helper.joinPath(('tests', 'hello', 'world', 'foo.txt')), 'a').close()
    allFiles = [
      helper.joinPath(('tests', 'hello', 'bar.txt')),
      helper.joinPath(('tests', 'hello', 'foo.txt')),
      helper.joinPath(('tests', 'hello', 'world', 'foo.txt'))
    ]
    self.assertListEqual(helper.getFiles(helper.joinPath(('tests', 'hello'))), allFiles)
    self.assertEqual(len(allFiles), 3)
    shutil.rmtree('tests/hello')
