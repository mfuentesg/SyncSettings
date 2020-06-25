import unittest
from sync_settings.libs import json


class TestJSON(unittest.TestCase):
    def test_loads_with_comment_blocks(self):
        content = """
            {
                // gist id
                "gist_id": "123123",
                /**
                   another comment
                 */
                "access_token": "access_token"
            }
        """
        self.assertDictEqual({'gist_id': '123123', 'access_token': 'access_token'}, json.loads(content))

    def test_loads_without_comment_blocks(self):
        content = """
            {
                "gist_id": "123123",
                "access_token": "access_token"
            }
        """
        self.assertDictEqual({'gist_id': '123123', 'access_token': 'access_token'}, json.loads(content))
