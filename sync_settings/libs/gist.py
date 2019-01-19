# -*- coding: utf-8 -*-

import requests
import json
from functools import wraps

from .logger import logger


class NotFoundError(RuntimeError):
    pass


class UnexpectedError(RuntimeError):
    pass


class NetworkError(RuntimeError):
    pass


class AuthenticationError(RuntimeError):
    pass


class UnprocessableDataError(RuntimeError):
    pass


def auth(func):
    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        if self.token is None:
            raise AuthenticationError('GitHub`s credentials are required')
        return func(self, *args, **kwargs)

    return auth_wrapper


def with_gid(func):
    @wraps(func)
    def with_gid_wrapper(self, *args, **kwargs):
        if not args[0]:
            raise ValueError('The given id `{}` is not valid'.format(args[0]))
        return func(self, *args, **kwargs)

    return with_gid_wrapper


class Gist:
    def __init__(self, token=None):
        self.token = token

    @staticmethod
    def make_uri(endpoint=''):
        e = '' if not endpoint else '/{}'.format(endpoint)
        return 'https://api.github.com/gists{}'.format(e)

    @auth
    def create(self, data):
        if not isinstance(data, dict) or not len(data):
            raise ValueError('Gist can`t be created without data')
        return self.__do_request('post', self.make_uri(), data=json.dumps(data)).json()

    @auth
    @with_gid
    def update(self, gid, data):
        if not isinstance(data, dict) or not len(data):
            raise ValueError('Gist can`t be updated without data')
        return self.__do_request('patch', self.make_uri(gid), data=json.dumps(data)).json()

    @auth
    @with_gid
    def delete(self, gid):
        response = self.__do_request('delete', self.make_uri(gid))
        return response.status_code == 204

    @with_gid
    def get(self, gid):
        def get_raw_content(url):
            return self.__do_request('get', url).content

        data = self.__do_request('get', self.make_uri(gid)).json()
        for _, file_data in data['files'].items():
            if file_data['truncated']:
                raw_content = get_raw_content(file_data['raw_url'])
                file_data['content'] = raw_content if raw_content else file_data['content']
        return data

    @with_gid
    def commits(self, gid):
        return self.__do_request('get', self.make_uri('{}/commits'.format(gid))).json()

    def __do_request(self, verb, url, **kwargs):
        # @TODO add support for proxies
        try:
            response = getattr(requests, verb)(url, headers=self.headers, **kwargs)
        except requests.exceptions.ConnectionError:
            raise NetworkError('Can`t perform this action due to network errors. Check your internet connection.')
        if response.status_code >= 300:
            logger.warning(response.json())
        if response.status_code == 404:
            raise NotFoundError('The requested gist do not exists, or the token has not enough permissions')
        if response.status_code in [401, 403]:
            raise AuthenticationError('The credentials are invalid, or the token does not have permissions')
        if response.status_code == 422:
            raise UnprocessableDataError('The provided data has errors')
        if response.status_code >= 300:
            raise UnexpectedError('Unexpected Error, Reason: {}'.format(response.json()['message']))

        return response

    @property
    def headers(self):
        return {} if self.token is None else {
            'accept': 'application/vnd.github.v3+json',
            'content-type': 'application/json',
            'authorization': 'token {}'.format(self.token)
        }
