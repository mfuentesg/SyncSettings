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
        'included_files': [],
        'excluded_files': []
    })
