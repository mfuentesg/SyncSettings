# -*- coding: utf-8 -*-

import requests
import json
from .exceptions import GistException

class Gist:
  BASE_URL = 'https://api.github.com'

  def __init__(self, token):
    response = requests.get(self.BASE_URL + '/user?access_token=' + token)
    if response.status_code != 200:
      raise GistException(Gist.__get_response_error('The entered token is invalid', response))
    else:
      self.__user_data = response.json()
      self.__headers = {
        'X-Github-Username': self.__user_data.get('login'),
        'Content-Type': 'application/json',
        'Authorization': 'token %s' %token
      }
      self.__defaults = {
        'public': False,
        'files': {}
      }

  def create(self, gist_data):
    _data = json.dumps(dict(self.__defaults, **gist_data))

    response = requests.post(
      self.BASE_URL + '/gists',
      data = _data,
      headers = self.__headers
    )

    if response.status_code == 201:
      return response.json()

    raise GistException(Gist.__get_response_error('Gist can\'t created', response))

  def edit(self, gist_id, gist_data):
    self.__defaults.pop('description', None)
    gist_data = json.dumps(dict(self.__defaults, **gist_data))
    response = requests.patch(
      self.BASE_URL + '/gists/%s' %gist_id,
      data=gist_data,
      headers=self.__headers
    )

    if response.status_code == 200:
      return response.json()

    raise GistException(Gist.__get_response_error('Can\'t edit the gist', response))

  def list(self, include_secret = False):
    base_url = ''.join((
      self.BASE_URL + '/users/',
      self.__user_data.get('login') + '/gists',
    ))
    response = None

    if include_secret:
      response = requests.get(base_url, headers=self.__headers)
    else:
      response = requests.get(base_url)

    if response.status_code == 200:
      return response.json()

    raise GistException(Gist.__get_response_error('It is not possible to list files', response))

  def delete(self, gist_id):
    response = requests.delete(
      self.BASE_URL + '/gists/' + gist_id,
      headers=self.__headers
    )

    if response.status_code == 204:
      return True

    raise GistException(Gist.__get_response_error('The Gist can be deleted', response))

  def get(self, gist_id):
    response = requests.get(self.BASE_URL + '/gists/' + gist_id)
    if response.status_code == 200:
      return response.json()

    raise GistException(Gist.__get_response_error('The gist not exist', response))

  @staticmethod
  def __get_response_error(message, response):
    rjson = response.json()
    error_description = "Code %s - %s" %(str(response.status_code), rjson.get('message'))

    return {
      'app_message': "%s - %s" % (error_description, message),
      'error_description': "[%s] - %s" % (message, error_description),
      'code': response.status_code
    }
