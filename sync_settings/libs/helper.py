# -*- coding: utf-8 -*-

import os
import re
import sys

try:
  from urllib import parse
except Exception as e:
  import urllib as parse


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
      f.extend([join_path((root, _file)) for _file in files])
    return f
  return []

def match_with_extension(element, pattern):
  regex = '([^.]*|^())\\%s$' % (pattern)
  return __match_regex(regex, element)

def match_with_filename(element, pattern):
  regex = '([^.]*|^())%s$' % (pattern)
  return __match_regex(regex, element)

def match_with_folder(element, pattern):
  regex = '^%s/(.*)$' % (pattern)
  return __match_regex(regex, element)

def __match_regex(reg, value):
  regex = re.compile(reg)
  return not regex.search(value) is None

def exclude_files_by_patterns(elements, patterns):
  elements = parse_to_os(elements)
  patterns = parse_to_os(patterns)

  are_valid_elements = isinstance(elements, list) and len(elements) > 0
  are_valid_patterns = isinstance(patterns, list) and len(patterns) > 0
  results = []

  if are_valid_elements and are_valid_patterns:
    for element in elements:
      for pattern in patterns:
        if match_with_folder(element, pattern) or \
           match_with_filename(element, pattern) or \
           match_with_extension(element, pattern):
            results.append(element)

    return get_difference(elements, results)
  return elements

def encode_path(path):
  if isinstance(path, str) and len(path) > 0:
    path = path.replace('\\', '/')
    return parse.quote(path, safe='')
  return None

def decode_path(path):
  if isinstance(path, str) and len(path) > 0:
    return parse.unquote(path).replace('/', os_separator())
  return None

def os_separator():
  separator = '\\' if sys.platform.startswith('win') else '/'
  return separator

def parse_to_os(paths):
  if (isinstance(paths, list)):
    return [p.replace('/', os_separator()).replace('\\', os_separator()) for p in paths]
  return None

def create_empty_file(path):
  try:
    open(path, 'a').close()
  except Exception as e:
    print(e)

def write_to_file(path, content, action = 'a+'):
  if isinstance(path, str) and isinstance(content, str):
    try:
      dir_path = os.path.dirname(path)
      if not exists_path(dir_path, True):
        os.makedirs(dir_path)

      with open(path, action) as f:
        f.write(content + '\n')
        f.close()
    except Exception as e:
      print(e)
  else:
    raise Exception('Invalid Parameters')
