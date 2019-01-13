import unittest
import requests
import json
import sys
import os
from ..libs import gist as gist, path

if sys.version_info < (3,):
    import mock
else:
    from unittest import mock


def get_mock_path(f):
    return path.join(os.path.abspath(os.path.dirname(__file__)), 'mocks', f)


class GistTest(unittest.TestCase):
    def setUp(self):
        self.api = gist.Gist()
        self.mock_response = mock.Mock()


class GetGistTest(GistTest):
    def test_raise_error_without_gist_id(self):
        with self.assertRaises(ValueError):
            self.api.get('')

    @mock.patch('requests.get')
    def test_raise_gist_not_found_error(self, mock_get):
        self.mock_response.status_code = 404
        mock_get.return_value = self.mock_response

        with self.assertRaises(gist.NotFoundError):
            self.api.get('not found')

    @mock.patch('requests.get')
    def test_raise_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()

        with self.assertRaises(gist.NetworkError):
            self.api.get('123123123')

    @mock.patch('requests.get')
    def test_unexpected_error_with_invalid_data(self, mock_get):
        self.mock_response.status_code = 408
        self.mock_response.json.return_value = {
            'message': 'an error',
        }
        mock_get.return_value = self.mock_response

        with self.assertRaises(gist.UnexpectedError):
            self.api.get('123123123')

    @mock.patch('requests.get')
    def test_valid_response(self, mock_get):
        self.mock_response.status_code = 200
        with open(get_mock_path('gist.json'), 'r') as f:
            content = json.load(f)
            self.mock_response.json.return_value = content

        mock_get.return_value = self.mock_response
        self.assertEqual(self.api.get('aa5a315d61ae9438b18d'), content)

    @mock.patch('requests.get')
    def test_valid_response_with_truncated_data(self, mock_get):
        self.mock_response.status_code = 200
        with open(get_mock_path('truncated_gist.json'), 'r') as f:
            content = json.load(f)
            self.mock_response.json.return_value = content

        self.mock_response.content = 'truncated content'
        mock_get.return_value = self.mock_response
        response = self.api.get('aa5a315d61ae9438b18d0')
        self.assertEqual(content['files']['dummy_file']['content'], 'truncated content')
        self.assertNotEqual(content['files']['dummy_file']['content'], response['files']['sync_file']['content'])
        self.assertEqual(content['files']['sync_file']['content'], response['files']['sync_file']['content'])


class CreateGistTest(GistTest):
    def test_raise_authentication_error_without_token(self):
        with self.assertRaises(gist.AuthenticationError):
            self.api.create({'files': {}})

    def test_argument_exception_without_data(self):
        self.api = gist.Gist('some_access_token')
        with self.assertRaises(ValueError):
            self.api.create({})


class DeleteGistTest(GistTest):
    def test_raise_authentication_error_without_token(self):
        with self.assertRaises(gist.AuthenticationError):
            self.api.delete('....')

    def test_argument_exception_without_id(self):
        self.api = gist.Gist('123123')
        with self.assertRaises(ValueError):
            self.api.delete('')

    @mock.patch('requests.delete')
    def test_failed_delete(self, mock_delete):
        self.api = gist.Gist('123123')
        self.mock_response.status_code = 205
        mock_delete.return_value = self.mock_response

        self.assertFalse(self.api.delete('123123'))

    @mock.patch('requests.delete')
    def test_success_delete(self, mock_delete):
        self.api = gist.Gist('123123')
        self.mock_response.status_code = 204
        mock_delete.return_value = self.mock_response

        self.assertTrue(self.api.delete('123123'))


class UpdateGistTest(GistTest):
    def setUp(self):
        self.api = gist.Gist('access token')

    def test_raise_argument_exception_without_data(self):
        with self.assertRaises(ValueError):
            self.api.update('asdfasdf', {})

    def test_raise_argument_exception_without_id(self):
        with self.assertRaises(ValueError):
            self.api.update('', {'files': {}})

    def test_raise_authentication_error_without_token(self):
        self.api = gist.Gist()
        with self.assertRaises(gist.AuthenticationError):
            self.api.update('123', {})
