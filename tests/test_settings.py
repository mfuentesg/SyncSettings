import unittest
import mock
from sync_settings.libs import settings


class TestSettings(unittest.TestCase):
    @mock.patch('sublime.save_settings')
    def test_update(self, save_mock):
        settings.update('some_key', 'value')
        self.assertTrue(save_mock.called)
