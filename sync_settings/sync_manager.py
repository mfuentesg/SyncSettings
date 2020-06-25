# -*- coding: utf-8 -*-

from fnmatch import fnmatch
import os
import sys
import requests
import shutil
import sublime
import threading
import time

from .libs import path, settings
from .libs.logger import logger

if sys.version_info < (3,):
    from Queue import Queue
else:
    from queue import Queue


def get_content(file):
    if not path.exists(file):
        return ''
    try:
        with open(file, 'rb') as fi:
            # TODO: Figure how to solve these kind of errors (for now ignore it)
            #  `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x86 in position 23: invalid start byte`
            return fi.read().decode('utf-8', errors='ignore')
    except Exception as e:
        logger.warning('file `{}` has errors'.format(file))
        logger.exception(e)
    return ''


def should_exclude(file_name):
    patterns = settings.get('excluded_files') or []
    # copy list to avoid side effects
    p = patterns[:]
    # ignore SyncSettings.sublime-settings file to avoid not wanted changes
    p.extend(['*SyncSettings.sublime-settings'])
    for pattern in p:
        if fnmatch(file_name, pattern):
            return True
    return False


def should_include(file_name):
    patterns = settings.get('included_files') or []
    # copy list to avoid side effects
    for pattern in patterns:
        # ignore SyncSettings.sublime-settings file to avoid not wanted changes
        if fnmatch(file_name, '*SyncSettings.sublime-settings'):
            return False
        if fnmatch(file_name, pattern):
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


def download_file(q):
    while not q.empty():
        url, name = q.get()
        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(name, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        except:  # noqa: E722
            pass
        finally:
            q.task_done()


def fetch_files(files, to=''):
    if not path.exists(to, folder=True):
        os.mkdir(to)
    rq = Queue(maxsize=0)
    user_path = path.join(sublime.packages_path(), 'User')
    items = files.items()
    for k, file in items:
        decoded_name = path.decode(k)
        name = path.join(user_path, decoded_name)
        if should_exclude(name) and not should_include(name):
            continue
        rq.put((file['raw_url'], path.join(to, k)))
    threads = min(10, len(items))
    for i in range(threads):
        worker = threading.Thread(target=download_file, args=(rq,))
        worker.setDaemon(True)
        worker.start()
        time.sleep(0.1)
    rq.join()


def move_files(origin):
    user_path = path.join(sublime.packages_path(), 'User')
    for f in os.listdir(origin):
        # set preferences and package control files to the final of the list
        if fnmatch(f, '*Preferences.sublime-settings') or fnmatch(f, '*Package%20Control.sublime-settings'):
            continue
        name = path.join(user_path, path.decode(f))
        directory = os.path.dirname(name)
        if not path.exists(directory, True):
            os.makedirs(directory)
        shutil.move(path.join(origin, f), name)

    pending_files = ['Preferences.sublime-settings', 'Package%20Control.sublime-settings']
    for f in pending_files:
        if not path.exists(path.join(origin, f)):
            continue
        shutil.move(path.join(origin, f), path.join(user_path, path.decode(f)))
