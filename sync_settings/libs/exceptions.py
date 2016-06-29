# -*- coding: utf-8 -*-

import json
import sys
import traceback
from .utils import Utils

class GistException(Exception):
  def to_json(self):
    """Parse the raised exception to JSON format

    Returns:
      [dict]
    """

    json_error = json.loads(json.dumps(self.args[0]))
    trace = traceback.extract_tb(sys.exc_info()[2])[-1]

    return Utils.merge_objects({
      'filename': str(trace[0]),
      'line': str(trace[1])
    }, json_error)
