# -*- coding: utf-8 -*-

import os, re

def getDifference (setA, setB):
  return list(filter(lambda el: el not in setB, setA))

def getHomePath (fl = ""):
  if isinstance(fl, str) and fl != "":
    return joinPath((os.path.expanduser('~'), fl))
  return os.path.expanduser('~')

def existsPath(path, isFolder = False):
  opath = os.path
  if isinstance(path, str) and path != "" and opath.exists(path):
    if (isFolder and opath.isdir(path)): return True
    if (not isFolder and opath.isfile(path)): return True
  return False

"""
  @param tuple pathTuple
  @return str|None
"""
def joinPath (pathTuple):
  if isinstance(pathTuple, tuple) and len(pathTuple) > 1:
    return os.path.join(*pathTuple)
  return None

def getFiles (path):
  if existsPath(path, True):
    f = []
    for root, dirs, files in os.walk(path):
      f.extend([joinPath((root, file)) for file in files])
    return f
  return []

"""
  @param list elements
  @param list patterns
  @return list
"""
def filterByPatterns (elements, patterns = []):
  isValidElements = isinstance(elements, list) and len(elements) > 0
  isValidPattern = isinstance(patterns, list) and len(patterns) > 0
  if validElements and validPattern:
    for element in elements:
      for pattern in patterns:
        """
          Verify if the pattern is a:
          * extension file
          * regex
          * filename
        """
        pass
  return list
