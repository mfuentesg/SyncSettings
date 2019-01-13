# -*- coding: utf-8 -*-

from fnmatch import fnmatch
import os
import sublime

from .libs import path, settings
from .libs.logger import logger


def get_content(file):
    try:
        with open(file, 'rb') as fi:
            # TODO: Figure how to solve these kind of errors (for now ignore it)
            #  `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x86 in position 23: invalid start byte`
            return fi.read().decode('utf-8', errors='ignore')
    except Exception as e:
        logger.warning('file `{}` has errors'.format(file))
        logger.exception(e)
        return ''


def edit_content(file, content):
    # TODO: Figure how to solve these kind of errors (for now ignore it)
    #  `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x86 in position 23: invalid start byte`
    file_content = content.encode('utf-8', errors='ignore')
    # ignore files without content
    if not file_content:
        return
    # ensure full path before to create the file
    directory = os.path.dirname(file)
    if not path.exists(directory, True):
        os.makedirs(directory)
    with open(file, 'wb+') as fi:
        fi.write(file_content)


def should_exclude(file):
    patterns = settings.get('excluded_files') or []
    # ignore SyncSettings.sublime-settings file to avoid not wanted changes
    patterns.extend(['*SyncSettings.sublime-settings'])
    for pattern in patterns:
        if fnmatch(file, pattern):
            return True
    return False


def should_include(file):
    patterns = settings.get('included_files') or []
    for pattern in patterns:
        # ignore SyncSettings.sublime-settings file to avoid not wanted changes
        if fnmatch(file, '*SyncSettings.sublime-settings'):
            return False
        if fnmatch(file, pattern):
            return True
    return False


def get_files():
    files_with_content = dict()
    user_path = path.join(sublime.packages_path(), 'User')
    for f in path.list_files(user_path):
        encoded_path = path.encode(f.replace('{}{}'.format(user_path, path.separator()), ''))
        if encoded_path in files_with_content:
            continue
        if should_exclude(f) and not should_include(f):
            continue
        content = get_content(f)
        if not content.strip():
            continue
        files_with_content[encoded_path] = {'content': content, 'path': f}
    return files_with_content


def update_files(files):
    user_path = path.join(sublime.packages_path(), 'User')
    for k, file in files.items():
        decoded_name = path.decode(k)
        name = path.join(user_path, decoded_name)
        if should_exclude(name) and not should_include(name):
            continue
        try:
            edit_content(name, file['content'])
        except Exception as e:
            logger.warning('can`t edit file `{}`'.format(name))
            logger.exception(e)
