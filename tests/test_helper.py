# -*- coding: utf-8 -*-

from unittest import TestCase
from tests import *

class TestHelper (TestCase):
  def test_difference (self):
    l = (list(helper.getDifference([1, 2, 3, 4], [1, 2, 3])))
    self.assertEqual(len(l), 1)
    self.assertEqual(l[0], 4)
