# -*- coding: utf-8 -*-

import os
from urllib import parse

def get_difference(seta, setb):
  return list(filter(lambda el: el not in setb, seta))

def get_home_path(fl = ""):
  home_path = os.path.expanduser('~')
  if isinstance(fl, str) and fl != "":
    return join_path((home_path, fl))
  return home_path

def exists_path(path, is_folder = False):
  opath = os.path
  if isinstance(path, str) and path != "" and opath.exists(path):
    if(is_folder and opath.isdir(path)): return True
    if(not is_folder and opath.isfile(path)): return True
  return False

def join_path(path_tuple):
  if isinstance(path_tuple, tuple) and len(path_tuple) > 1:
    return os.path.join(*path_tuple)
  return None

def get_files(path):
  if exists_path(path, True):
    f = []
    for root, dirs, files in os.walk(path):
      f.extend([join_path((root, file)) for file in files])
    return f
  return []

def exclude_files_by_patterns(elements, patterns):
  def is_folder_pattern(element, pattern):
    if element.startswith(pattern) and exists_path(pattern, True):
      sub_path = element.replace(pattern, '')
      sub_path = sub_path[1:] if sub_path.startswith(('\\', '/')) else sub_path
      pattern_path = join_path((pattern, sub_path))
      return exists_path(pattern_path)

    return False

  are_valid_elements = isinstance(elements, list) and len(elements) > 0
  are_valid_patterns = isinstance(patterns, list) and len(patterns) > 0
  results = []

  if are_valid_elements and are_valid_patterns:
    for element in elements:
      for pattern in patterns:
        extension = '.' + element.split(os.extsep)[-1]
        if is_folder_pattern(element, pattern):
          results.append(element)
        elif(extension == pattern or element == pattern) and exists_path(element):
          results.append(element)
    return get_difference(elements, results)
  return elements

def encode_path(path):
  if isinstance(path, str) and len(path) > 0:
    return parse.quote(path, safe='')
  return None

def decode_path(path):
  if isinstance(path, str) and len(path) > 0:
    return parse.unquote(path)
  return None
