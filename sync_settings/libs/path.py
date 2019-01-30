# -*- coding: utf-8 -*-

import sys
import os
import platform
from functools import wraps

if sys.version_info < (3,):
    from urllib import unquote
    from urllib import quote
else:
    from urllib.parse import unquote
    from urllib.parse import quote


def separator():
    return '\\' if platform.system() == 'Windows' else '/'


def os_path(func):
    @wraps(func)
    def path_wrapper(*args, **kwargs):
        w = func(*args, **kwargs)
        sep = separator()
        return w.replace('/', sep).replace('\\', sep)
    return path_wrapper


def encode(path):
    return quote(path.replace('\\', '/'), safe='')


@os_path
def decode(path):
    return unquote(path)


@os_path
def join(*paths):
    if not len(paths):
        return ''
    return os.path.join(*paths)


def exists(path, folder=False):
    return os.path.isdir(path) if folder else os.path.isfile(path)


def list_files(path):
    if not exists(path, folder=True):
        return []
    f = []
    for root, dirs, files in os.walk(path):
        f.extend([join(root, _file) for _file in files])
    return f
