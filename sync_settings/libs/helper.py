# -*- coding: utf-8 -*-

import os
import re
import sys

try:
  from urllib import parse
except Exception as e:
  import urllib as parse


class Helper:

  @classmethod
  def merge_objects(cls, base, update):
    return dict(base, **update)

  @classmethod
  def get_difference(cls, seta, setb):
    return list(filter(lambda el: el not in setb, seta))

  @classmethod
  def get_home_path(cls, fl = ""):
    home_path = os.path.expanduser('~')
    if isinstance(fl, str) and fl != "":
      return cls.join_path((home_path, fl))
    return home_path

  @classmethod
  def exists_path(cls, path, is_folder = False):
    opath = os.path
    if isinstance(path, str) and path != "" and opath.exists(path):
      if(is_folder and opath.isdir(path)): return True
      if(not is_folder and opath.isfile(path)): return True
    return False

  @classmethod
  def join_path(cls, path_tuple):
    if isinstance(path_tuple, tuple) and len(path_tuple) > 1:
      return os.path.join(*path_tuple)
    return None

  @classmethod
  def get_files(cls, path):
    if cls.exists_path(path, True):
      f = []
      for root, dirs, files in os.walk(path):
        f.extend([cls.join_path((root, _file)) for _file in files])
      return f
    return []

  @classmethod
  def is_file_extension(cls, ext):
    regex = "^\.[^.]*$"
    return cls.__match_regex(regex, ext)

  @classmethod
  def match_with_extension(cls, element, pattern):
    regex = '([^.]*|^())\\%s$' % (pattern)
    return cls.__match_regex(regex, element)

  @classmethod
  def match_with_filename(cls, element, pattern):
    regex = '([^.]*|^())%s$' % (pattern)
    return cls.__match_regex(regex, element)

  @classmethod
  def match_with_folder(cls, element, pattern):
    regex = '^%s/(.*)$' % (pattern)
    return cls.__match_regex(regex, element)

  @classmethod
  def __match_regex(cls, reg, value):
    regex = re.compile(reg)
    return not regex.search(value) is None

  @classmethod
  def exclude_files_by_patterns(cls, elements, patterns):
    elements = cls.parse_to_os(elements)
    patterns = cls.parse_to_os(patterns)

    are_valid_elements = isinstance(elements, list) and len(elements) > 0
    are_valid_patterns = isinstance(patterns, list) and len(patterns) > 0
    results = []

    if are_valid_elements and are_valid_patterns:
      for element in elements:
        for pattern in patterns:
          if cls.match_with_folder(element, pattern) or \
             cls.match_with_filename(element, pattern) or \
             cls.match_with_extension(element, pattern):
              results.append(element)

      return cls.get_difference(elements, results)
    return elements

  @classmethod
  def encode_path(cls, path):
    if isinstance(path, str) and len(path) > 0:
      path = path.replace('\\', '/')
      return parse.quote(path, safe='')
    return None

  @classmethod
  def decode_path(cls, path):
    if isinstance(path, str) and len(path) > 0:
      return parse.unquote(path).replace('/', cls.os_separator())
    return None

  @classmethod
  def os_separator(cls, ):
    separator = '\\' if sys.platform.startswith('win') else '/'
    return separator

  @classmethod
  def parse_to_os(cls, paths):
    if (isinstance(paths, list)):
      return [p.replace('/', cls.os_separator()).replace('\\', cls.os_separator()) for p in paths]
    return None

  @classmethod
  def create_empty_file(cls, path):
    try:
      open(path, 'a').close()
    except Exception as e:
      print(e)

  @classmethod
  def write_to_file(cls, path, content, action = 'a+'):
    if isinstance(path, str) and isinstance(content, str):
      try:
        dir_path = os.path.dirname(path)
        if not cls.exists_path(dir_path, True):
          os.makedirs(dir_path)

        with open(path, action) as f:
          f.write(content + '\n')
          f.close()
      except Exception as e:
        print(e)
    else:
      raise Exception('Invalid Parameters')
