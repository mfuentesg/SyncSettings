# -*- coding: utf-8 -*-

import os

def getDifference (setA, setB):
  return filter(lambda el: el not in setB, setA)

def getHomePath (fl = ""):
  if isinstance(fl, str) and fl != "":
    return os.path.join(os.path.expanduser('~'), fl)
  return os.path.expanduser('~')
