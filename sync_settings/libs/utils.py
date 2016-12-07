# -*- coding: utf-8 -*-

import os
import re
import sys
import json
from fnmatch import fnmatch

from functools import reduce

if sys.version_info < (3,):
    from urllib import unquote
    from urllib import quote
else:
    from urllib.parse import unquote
    from urllib.parse import quote

class Utils:

  @classmethod
  def merge_objects(cls, base, *update):
    """Merge multiple dictionaries in a single

      Arguments:
        - base {dict}: Default data to merge
        - update {tuple}: Data list to merge

      Returns:
        [dict]: single dictionary with the merged result
    """

    return dict(base, **reduce(lambda x, y: dict(x, **y), update));

  @classmethod
  def merge_lists(cls, base, *update):
    """Merge multiple tuples in a single

      Arguments:
        - base {list}: Default data to merge
        - update {tuple}: Data list to merge

      Returns:
        [list]: single list with the merged result
    """

    return list(set(base + reduce(lambda x, y: x + y, update)))

  @classmethod
  def get_difference(cls, set_a, set_b):
    """Returns the missing data from the first list on the second list

      Arguments:
        - set_a {list}: Set to search
        - set_b {list}: Set to compare

      Returns:
        [list]: list with the missing data
    """

    return list(filter(lambda el: el not in set_b, set_a))

  @classmethod
  def get_home_path(cls, fl = ""):
    """Gets the user home path

      Arguments:
        - fl {str}: Extra path to complement the home path

      Returns:
        [string]: Home path joined with the extra path
    """

    home_path = os.path.expanduser('~')
    if isinstance(fl, str) and fl != "":
      return cls.join_path(home_path, fl)
    return home_path

  @classmethod
  def exists_path(cls, path, is_folder = False):
    """Checks if the indicated path exists

      Arguments:
        - path {str}: Path of the file or folder
        - is_folder {bool}: Indicates if the path is folder

      Returns:
        [bool]
    """

    opath = os.path
    if isinstance(path, str) and path != "" and opath.exists(path):
      if(is_folder and opath.isdir(path)): return True
      if(not is_folder and opath.isfile(path)): return True
    return False

  @classmethod
  def join_path(cls, *path_tuple):
    """Join the parameters to an OS path

      Arguments:
        - path_tuple {tuple}: Path in tuple format

      Returns:
        [string]: the joined path
    """

    return os.path.join(*path_tuple)

  @classmethod
  def get_files(cls, path):
    """Generates a list with the files inside a folder

      Arguments:
        - path {str}: Folder path

      Returns:
        [list]: the file list
    """

    if cls.exists_path(path, True):
      f = []
      for root, dirs, files in os.walk(path):
        f.extend([cls.join_path(root, _file) for _file in files])
      return f
    return []

  @classmethod
  def is_file_extension(cls, ext):
    """Checks if passed substring is a extension

    Arguments:
      ext {string}: Extension to validates

    Returns:
      [bool]
    """

    regex = '^\\.[^.]*$'
    return cls.__match_regex(regex, ext)

  @classmethod
  def match_with_extension(cls, element, pattern):
    """Checks if the element has the specified extension

    Arguments:
      element {string}: String to validates
      pattern {string}: Sought extension

    Returns:
      [bool]
    """

    pattern = pattern.replace('\\', '\\\\')
    regex = '([^.]*|^())\\%s$' % (pattern)
    return cls.__match_regex(regex, element)

  @classmethod
  def match_with_filename(cls, element, pattern):
    """Checks if the element has the specified name

    Arguments:
      element {string}: String to validates
      pattern {string}: Sought filename

    Returns:
      [bool]
    """

    return element == pattern

  @classmethod
  def match_with_folder(cls, element, pattern):
    """Checks if the element is inside the specified folder

    Arguments:
      element {string}: String to validates
      pattern {string}: Sought folder name

    Returns:
      [bool]
    """

    regex = '^%s%s(.*)$' % (pattern, cls.os_separator())
    return cls.__match_regex(regex.replace('\\', '\\\\'), element)

  @classmethod
  def match_with_willcard(cls, element, pattern):
    """Checks if the element is inside the specified folder

    Arguments:
      element {string}: String to validates
      pattern {string}: Sought folder name

    Returns:
      [bool]
    """

    return fnmatch(element, pattern)

  @classmethod
  def __match_regex(cls, reg, value):
    """Executes the specified regular expression

    Arguments:
      reg {string}: String to validates
      value {string}: Sought expression

    Returns:
      [bool]
    """

    try:
      regex = re.compile(reg)
      return not regex.search(value) is None
    except:
      return False

  @classmethod
  def exclude_files_by_patterns(cls, elements, patterns):
    """Removes the elements that match with the specified patterns

    Arguments:
      elements {list}: Set to evaluates
      patterns {list}: Sought patterns

    Returns:
      [list]: Files that does not match with the patterns
    """

    are_valid_elements = isinstance(elements, list)
    are_valid_patterns = isinstance(patterns, list)
    elements = cls.parse_to_os(elements)

    if are_valid_elements and are_valid_patterns:
      return cls.get_difference(
        elements,
        cls.filter_files_by_patterns(elements, patterns)
      )

    return elements

  @classmethod
  def filter_files_by_patterns(cls, elements, patterns):
    """Gets the elements that match with the specified patterns

    Arguments:
      elements {list}: Set to evaluates
      patterns {list}: Sought patterns

    Returns:
      [list]: Files that match with the patterns
    """

    elements = cls.parse_to_os(elements)
    patterns = cls.parse_to_os(patterns)
    results = []

    for element in elements:
      for pattern in patterns:
        if cls.match_with_folder(element, pattern) or \
           cls.match_with_filename(element, pattern) or \
           cls.match_with_extension(element, pattern) or \
           cls.match_with_willcard(element, pattern):
            results.append(element)

    return results

  @classmethod
  def encode_path(cls, path):
    """Encodes a path in URL encoding format

    Arguments:
      path {string}: Path to encode

    Returns:
      [string]: Encoded path
    """

    if isinstance(path, str) and len(path):
      path = path.replace('\\', '/')
      return quote(path, safe='')
    return None

  @classmethod
  def decode_path(cls, path):
    """Parse an URL encoded path to a string

    Arguments:
      path {string}: Path to decode

    Returns:
      [string]: Decoded path
    """

    if isinstance(path, str) and len(path):
      """
        This is to deal with source files with non-ascii names
        We get url-quoted UTF-8 from dbus; convert to url-quoted ascii
        and then unquote. If you don't first convert ot ascii, it fails.
        It's a bit magical, but it seems to work
      """
      path = path.encode('ascii') if sys.version_info < (3,) else path
      return unquote(path).replace('/', cls.os_separator())
    return None

  @classmethod
  def os_separator(cls):
    """Gets the OS path separator

      Returns:
        [string]
    """

    separator = '\\' if sys.platform.startswith('win') else '/'
    return separator

  @classmethod
  def parse_to_os(cls, paths):
    """Replaces the slashes to OS separators

    Arguments:
      paths {list}: Paths to parse

    Returns:
      [list]: Parsed paths
    """

    if (isinstance(paths, list)):
      separator = cls.os_separator()
      return [p.replace('/', separator).replace('\\', separator) for p in paths]

    return None

  @classmethod
  def create_empty_file(cls, path):
    """Creates an empty file in the specified path

    Arguments:
      path {string}: Full file path

    Raises:
      Exception: The file cannot be created
    """

    try:
      open(path, 'a').close()
    except Exception as e:
      print('Fail to create the file %s - %s' % (path, str(e)))

  @classmethod
  def write_to_file(cls, path, content, action = 'ab+', as_json = False):
    """Writes the content in the specified file

    Arguments:
      path {string}: Full file path
      content {string}: Content to write in the file

    Raises:
      Exception: Cannot write to the file
    """

    if isinstance(path, str) and (isinstance(content, (str, dict))):
      try:
        dir_path = os.path.dirname(path)
        if not cls.exists_path(dir_path, True):
          os.makedirs(dir_path)

        with open(path, action) as f:
          if (as_json and isinstance(content, dict)):
            json.dump(content, f)
          else:
            f.write(content.encode("utf-8"))
          f.close()
      except Exception as e:
        print('An exception in file %s - %s: ' % (path, str(e)))
    else:
      raise Exception('Invalid Parameters')

  @classmethod
  def parse_patterns(cls, files, base_path):
    """Converts the specified file list to a valid format

    Arguments:
      files {list}: Set to convert
      base_path {string}: Base application path

    Returns:
      [list]: Parsed set
    """

    result_list = []
    for f in files:
      if not cls.is_file_extension(f):
        result_list.append(cls.join_path(base_path, f))
        continue
      result_list.append(f)

    return result_list

  @classmethod
  def get_file_content(cls, file_path, as_json = False):
    """Gets the content of a file

    Arguments:
      file_path {string}: File path
    """

    try:
      f = open(file_path, 'rb')
      file_content = f.read().decode('utf-8')
      f.close()
      return json.loads(file_content) if as_json else file_content

    except Exception as e:
      print('Error in file %s - %s' % (file_path, str(e)))
