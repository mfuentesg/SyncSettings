# -*- coding: utf-8 -*-

import sublime

def encode_json(content):
    """
    It removes any comment inside json file, in order to have a valid json file.
    :param content:
        Content of the json file in plain text
    :return:
        Deserialized json
    """
    return sublime.decode_value(content)
