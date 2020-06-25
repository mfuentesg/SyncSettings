import json
import re

DIALOG_YES = 1


class Settings:
    def __init__(self, data):
        self.data = data

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value


def yes_no_cancel_dialog(*args):
    pass


def save_settings(*args):
    pass


def load_settings(*args):
    return Settings({
        'gist_id': 'gist-123123',
        'access_token': 'access-token',
        'http_proxy': '',
        'https_proxy': '',
        'included_files': [],
        'excluded_files': []
    })


def encode_value(data, pretty):
    return json.dumps(data, ensure_ascii=False)


def decode_value(content):
    decoded = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", content)
    return json.loads(re.sub(re.compile(r"//.*?\n"), "", decoded))
