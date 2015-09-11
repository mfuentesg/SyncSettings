# -*- coding: utf-8 -*-

import sys, os, json
sys.path.append(os.path.abspath('..'))
from sync_settings import gistapi, logger, helper

try:
  options_path = os.path.abspath('tests/options.json')
  with open(options_path, 'r') as f:
    opts = json.loads(f.read())
except Exception as e:
  opts = {}
  print('\033[91m'+'Sync Settings: options.json file not exists'+'\033[0m')

