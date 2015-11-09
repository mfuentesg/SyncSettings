# -*- coding: utf-8 -*-

import json
import sys
import traceback

class GistException(Exception):
  def to_json(self):
    json_error = json.loads(json.dumps(self.args[0]))
    trace = traceback.extract_tb(sys.exc_info()[2])[-1]

    return json_error.update({
      'filename': str(trace[0]),
      'line': str(trace[1])
    })
