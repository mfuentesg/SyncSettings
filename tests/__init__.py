# -*- coding: utf-8 -*-

import os
import sys
import json

opts = {}

try:
  test_file_path = os.path.abspath('README.md')
  access_token = os.environ['SYNC_ACCESS_TOKEN']
  opts = {
    'access_token': access_token,
    'logger_filename': '.logger_test.log'
  }
except Exception as e:
  message = ''.join((
    '\033[91m',
    'Sync Settings: The environment variable `SYNC_ACCESS_TOKEN` is not set.\n',
    'Try with `export SYNC_ACCESS_TOKEN="<YOUR_ACCESS_TOKEN>"`',
    '\033[0m'
  ))
  print(message)
  sys.exit(1)
