# -*- coding: utf-8 -*-

import os, re
from urllib import parse

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

def excludeFilesByPatterns (elements, patterns):
  isValidElements = isinstance(elements, list) and len(elements) > 0
  isValidPattern = isinstance(patterns, list) and len(patterns) > 0
  results = []

  if isValidElements and isValidPattern:
    for element in elements:
      for pattern in patterns:
        extension = '.' + element.split(os.extsep)[-1]
        filename = os.path.basename(element)

        if element.startswith(pattern) and existsPath(pattern, True) and existsPath(joinPath((pattern, filename))):
          results.append(element)
        elif (extension == pattern or element == pattern) and existsPath(element):
          results.append(element)
    return getDifference(elements, results)
  return elements

def encodePath(path):
  if isinstance(path, str) and len(path) > 0:
    return parse.quote(path)
  return None

def decodePath(path):
  if isinstance(path, str) and len(path) > 0:
    return parse.unquote(path)
  return None

def isWindows ():
  return sys.platform.startswith('win')
