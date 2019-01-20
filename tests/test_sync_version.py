import unittest
import mock
from sync_settings import sync_version as version


class TestSyncVersion(unittest.TestCase):
    @mock.patch('requests.get')
    def test_get_remote_version_failed(self, get_mock):
        response = mock.Mock()
        response.status_code = 404
        get_mock.return_value = response
        self.assertDictEqual({}, version.get_remote_version())

    @mock.patch('sync_settings.libs.gist.Gist.commits')
    def test_get_remote_version(self, commits_mock):
        commits_mock.return_value = [{
            'version': '123123123',
            'committed_at': '2019-01-11T02:15:15Z'
        }]
        v = version.get_remote_version()
        self.assertDictEqual({'hash': '123123123', 'created_at': '2019-01-11T02:15:15Z'}, v)

    @mock.patch('sync_settings.libs.path.exists', mock.MagicMock(return_value=False))
    def test_get_local_version_no_file(self):
        v = version.get_local_version()
        self.assertDictEqual({}, v)

    @mock.patch('sync_settings.libs.path.exists', mock.MagicMock(return_value=True))
    @mock.patch('sync_settings.sync_version.open', mock.mock_open(read_data='plain text'))
    def test_get_local_version_invalid_content(self):
        self.assertDictEqual({}, version.get_local_version())

    @mock.patch('sync_settings.libs.path.exists', mock.MagicMock(return_value=True))
    @mock.patch('sync_settings.sync_version.open', mock.mock_open(read_data='{}'))
    def test_get_local_version_empty_json(self):
        self.assertDictEqual({}, version.get_local_version())

    @mock.patch('sync_settings.libs.path.exists', mock.MagicMock(return_value=True))
    @mock.patch('sync_settings.sync_version.open', mock.mock_open(
        read_data='{"created_at": "2019-01-11T02:15:15Z", "hash": "123123123"}'))
    def test_get_local_version_with_content(self):
        v = version.get_local_version()
        self.assertDictEqual({'hash': '123123123', 'created_at': '2019-01-11T02:15:15Z'}, v)

    @mock.patch('sublime.yes_no_cancel_dialog', mock.MagicMock(return_value=1))
    def test_show_update_dialog(self):
        def on_done():
            on_done.called = True

        on_done.called = False
        version.show_update_dialog(on_done)
        self.assertTrue(on_done.called)

    @mock.patch('sync_settings.sync_version.get_local_version', mock.MagicMock(return_value={}))
    @mock.patch('sync_settings.sync_version.show_update_dialog')
    def test_upgrade_without_local_version(self, dialog_mock):
        version.upgrade()
        self.assertTrue(dialog_mock.called)

    @mock.patch('sync_settings.sync_version.get_local_version', mock.MagicMock(return_value={
        'hash': '123123123',
        'created_at': '2019-01-11T02:15:15Z'
    }))
    @mock.patch('sync_settings.sync_version.get_remote_version', mock.MagicMock(return_value={}))
    @mock.patch('sync_settings.sync_version.show_update_dialog')
    def test_upgrade_without_remote_version(self, dialog_mock):
        version.upgrade()
        self.assertFalse(dialog_mock.called)

    @mock.patch('sync_settings.sync_version.get_local_version', mock.MagicMock(return_value={
        'hash': '123123123',
        'created_at': '2019-01-11T02:15:15Z'
    }))
    @mock.patch('sync_settings.sync_version.get_remote_version', mock.MagicMock(return_value={
        'hash': '123123123',
        'created_at': '2019-01-11T02:15:15Z'
    }))
    @mock.patch('sync_settings.sync_version.show_update_dialog')
    def test_upgrade_same_version(self, dialog_mock):
        version.upgrade()
        self.assertFalse(dialog_mock.called)

    @mock.patch('sync_settings.sync_version.get_local_version', mock.MagicMock(return_value={
        'hash': '123123123',
        'created_at': '2019-01-11T02:15:15Z'
    }))
    @mock.patch('sync_settings.sync_version.get_remote_version', mock.MagicMock(return_value={
        'hash': '123123124',
        'created_at': '2019-01-12T02:15:15Z'
    }))
    @mock.patch('sync_settings.sync_version.show_update_dialog')
    def test_upgrade_outdated_version(self, dialog_mock):
        version.upgrade()
        self.assertTrue(dialog_mock.called)
