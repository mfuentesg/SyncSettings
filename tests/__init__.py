# -*- coding: utf-8 -*-

import sys, os, json
sys.path.append(os.path.abspath('..'))
from sync_settings import gistapi, logger

try:
	with open(os.path.abspath('tests/options.json'), 'r') as f:
		Opts = json.loads(f.read())
except Exception as e:
	Opts = {}
	print('Sync Settings: Options file not exists')
	print(e)
