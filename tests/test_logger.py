# -*- coding: utf-8 -*-

from unittest import TestCase
from tests import *
import os

_logger = logger.Logger
_logger.FILE_NAME = Opts.get('logger_filename')
test_path = os.path.join(os.path.expanduser('~'), Opts.get('logger_filename'))

class TestLogger (TestCase):
  def test_filename (self):
    self.assertEqual(_logger.FILE_NAME, Opts.get('logger_filename'))

  def test_get_path (self):
    self.assertEqual(_logger.getPath(), test_path)

  def test_create_file (self):
    self.assertFalse(os.path.exists(test_path))
    _logger.createEmptyFile()
    self.assertTrue(os.path.exists(test_path))
    self.assertEqual(os.path.getsize(test_path), 0)

  def test_log (self):
    _logger.log('Some content', _logger.MESSAGE_ERROR_TYPE)
    self.assertGreater(os.path.getsize(test_path), 0)
    os.remove(test_path)
    self.assertFalse(os.path.exists(test_path))
