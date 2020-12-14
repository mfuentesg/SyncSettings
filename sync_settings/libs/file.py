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
    trailing_object_commas_re = re.compile(
        r'(,)\s*}(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
    trailing_array_commas_re = re.compile(
        r'(,)\s*\](?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')

    decoded = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", content)
    decoded = trailing_array_commas_re.sub("]", decoded)
    decoded = trailing_object_commas_re.sub("}", decoded)

    return json.loads(re.sub(re.compile(r"(?:(?:^\s*)|\s+)//.*$", re.MULTILINE), "", decoded))
