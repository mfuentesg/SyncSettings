# -*- coding: utf-8 -*-

import logging
from os import path

filename = path.join(path.expanduser('~'), '.sync_settings', 'sync.log')

logging.basicConfig(filename=filename, level=logging.DEBUG)
logger = logging.getLogger(__name__)
