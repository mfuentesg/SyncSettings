# # -*- coding: utf-8 -*-

from sync_settings.libs.logger import Logger
from unittest import TestCase
from tests import opts
import os

Logger.FILE_NAME = opts.get('logger_filename')
test_path = os.path.join(os.path.expanduser('~'), opts.get('logger_filename'))

class TestLogger(TestCase):
  def test_filename(self):
    self.assertEqual(Logger.FILE_NAME, opts.get('logger_filename'))

  def test_get_path(self):
    self.assertEqual(Logger.get_path(), test_path)

  def test_create_file(self):
    self.assertFalse(os.path.exists(test_path))
    Logger.create_empty_file()
    self.assertTrue(os.path.exists(test_path))
    self.assertEqual(os.path.getsize(test_path), 0)

  def test_log(self):
    Logger.log('Some content', Logger.MESSAGE_ERROR_TYPE)
    self.assertGreater(os.path.getsize(test_path), 0)
    os.remove(test_path)
    self.assertFalse(os.path.exists(test_path))
