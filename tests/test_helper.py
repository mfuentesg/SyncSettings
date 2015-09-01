# -*- coding: utf-8 -*-

from unittest import TestCase
from tests import *
import os

class TestHelper (TestCase):
  def test_difference (self):
    l = (list(helper.getDifference([1, 2, 3, 4], [1, 2, 3])))
    self.assertEqual(len(l), 1)
    self.assertEqual(l[0], 4)

  def test_home_path (self):
    homePath = os.path.expanduser('~')
    self.assertEqual(os.path.join(homePath, 'foo'), helper.getHomePath('foo'))
    self.assertEqual(homePath, helper.getHomePath())
    #Wrong Cases
    self.assertEqual(homePath, helper.getHomePath(None))
    self.assertEqual(homePath, helper.getHomePath(1234))
