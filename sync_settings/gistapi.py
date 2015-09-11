# -*- coding: utf-8 -*-

import requests, json, traceback, sys

class GistException (Exception):
  def toJSON (self):
    jsonError = json.loads(json.dumps(self.args[0]))
    trace = traceback.extract_tb(sys.exc_info()[2])[-1]
    jsonError.update({
      'filename': str(trace[0]),
      'line': str(trace[1])
    })
    return jsonError

class Gist:
  BASE_URL = 'https://api.github.com'

  def __init__ (self, token):
    response = requests.get(self.BASE_URL + '/user?access_token=' + token)
    if response.status_code != 200:
      raise GistException(Gist.__getResponseError('The entered token is invalid', response))
    else:
      self.__userData = response.json()
      self.__accessToken = token
      self.__headers = {
        'X-Github-Username': self.__userData.get('login'),
        'Content-Type': 'application/json',
        'Authorization': 'token %s' %token
      }
      self.__defaults = {
        'public': False,
        'files': {}
      }

  def create (self, gistData):
    _data = json.dumps(dict(self.__defaults, **gistData))

    response = requests.post(
      self.BASE_URL + '/gists',
      data = _data,
      headers = self.__headers
    )

    if response.status_code == 201:
      return response.json()

    raise GistException(Gist.__getResponseError('Gist can\'t created', response))

  def edit (self, gistId, gistData):
    self.__defaults.pop('description', None)
    gistData = json.dumps(dict(self.__defaults, **gistData))
    response = requests.patch(
      self.BASE_URL + '/gists/%s' %gistId,
      data=gistData,
      headers=self.__headers
    )

    if response.status_code == 200:
      return response.json()

    raise GistException(Gist.__getResponseError('Can\'t edit the gist', response))

  def list (self):
    listUrl = (
      self.BASE_URL + '/users/',
      self.__userData.get('login') + '/gists'
    )

    response = requests.get(''.join(listUrl))
    if response.status_code == 200:
      return response.json()

    raise GistException(Gist.__getResponseError('It is not possible to list files', reponse))

  def delete (self, gistId):
    response = requests.delete(
      self.BASE_URL + '/gists/' + gistId,
      headers=self.__headers
    )

    if response.status_code == 204:
      return True

    raise GistException(Gist.__getResponseError('The Gist can be deleted', response))

  def get (self, gistId):
    response = requests.get(self.BASE_URL + '/gists/' + gistId)
    if response.status_code == 200:
      return response.json()

    raise GistException(Gist.__getResponseError('The gist not exist', response))

  @staticmethod
  def __getResponseError (message, response):
    rjson = response.json()
    errorDescription = "Code " + str(response.status_code) + " - " + rjson.get('message')
    return {
      'app_message': message,
      'error_description': errorDescription,
      'code': response.status_code
    }
