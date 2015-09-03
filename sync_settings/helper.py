# -*- coding: utf-8 -*-

import os

def getDifference (setA, setB):
  return list(filter(lambda el: el not in setB, setA))

def getHomePath (fl = ""):
  if isinstance(fl, str) and fl != "":
    return joinPath((os.path.expanduser('~'), fl))
  return os.path.expanduser('~')

def existsPath(path = '', isFolder = False):
  opath = os.path
  if isinstance(path, str) and opath.exists(path):
    if (isFolder and opath.isdir(path)): return True
    if (not isFolder and opath.isfile(path)): return True
  return False

def joinPath (list):
  if isinstance(list, tuple) and len(list) > 1:
    return os.path.join(*list)
  return None

def getFiles (path = ''):
  if existsPath(path, True):
    f = []
    for root, dirs, files in os.walk(path):
      f.extend([joinPath((root, file)) for file in files])
    return f
  return []
