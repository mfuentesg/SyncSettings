# -*- coding: utf-8 -*-

import sys, os, json
sys.path.append(os.path.abspath('..'))
from sync_settings import gistapi, logger, helper

try:
  with open(os.path.abspath('tests/options.json'), 'r') as f:
    Opts = json.loads(f.read())
except Exception as e:
  Opts = {}
  print ('\033[91m'+'Sync Settings: options.json file not exists'+'\033[0m')

