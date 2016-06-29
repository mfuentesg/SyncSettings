# # -*- coding: utf-8 -*-

import os
from sync_settings.libs.logger import Logger
from unittest import TestCase
from tests import opts

Logger.FILE_NAME = opts.get('logger_filename')
test_path = os.path.join(os.path.expanduser('~'), opts.get('logger_filename'))

class TestLogger(TestCase):
  def test_filename(self):
    self.assertEqual(Logger.FILE_NAME, opts.get('logger_filename'))

  def test_get_path(self):
    self.assertEqual(Logger.get_path(), test_path)

  def test_log(self):
    Logger.log('Some content', True)
    self.assertGreater(os.path.getsize(test_path), 0)
    os.remove(test_path)
    self.assertFalse(os.path.exists(test_path))

  def test_write(self):
    message = 'some message'
    self.assertFalse(os.path.exists(test_path))
    Logger.write(message)
    self.assertTrue(os.path.exists(test_path))
    with open(Logger.get_path(), 'r') as f:
      self.assertGreater(f.read().find(message), 0)
    os.remove(Logger.get_path())
    self.assertFalse(os.path.exists(test_path))
