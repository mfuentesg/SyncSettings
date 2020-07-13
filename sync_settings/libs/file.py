# -*- coding: utf-8 -*-

import json
import re


def encode_json(content):
    """
    It removes any comment inside json file, in order to have a valid json file.
    :param content:
        Content of the json file in plain text
    :return:
        Deserialized json
    """
    decoded = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", content)
    return json.loads(re.sub(re.compile(r"(?:(?:^\s*)|\s+)//.*$", re.MULTILINE), "", decoded))
