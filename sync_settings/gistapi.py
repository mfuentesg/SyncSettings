# -*- coding: utf-8 -*-

import requests, json

class Gist:
	BASE_URL = 'https://api.github.com'

	def __init__ (self, token):
		response = requests.get(self.BASE_URL + '/user?access_token=' + token)
		if response.status_code != 200:
			raise Exception('The entered token is invalid')
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
				'description': 'Sublime Text Configuration',
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

		raise Exception('Gist can\'t created')

	def edit (self, gistId, gistData):
		gistData = json.dumps(dict(self.__defaults, **gistData))
		response = requests.patch(
			self.BASE_URL + '/gists/%s' %gistId,
			data=gistData,
			headers=self.__headers
		)

		if response.status_code == 200:
			return response.json()

		raise Exception('Can\'t edit the gist')

	def list (self):
		listUrl = (
			self.BASE_URL + '/users/',
			self.__userData.get('login') + '/gists'
		)

		response = requests.get(''.join(listUrl))
		if response.status_code == 200:
			return response.json()

		raise Exception('It is not possible to list files')

	def delete (self, gistId):
		response = requests.delete(
			self.BASE_URL + '/gists/' + gistId,
			headers=self.__headers
		)

		if response.status_code == 204:
			return True

		raise Exception('The Gist can be deleted')

	def get (self, gistId):
		response = requests.get(self.BASE_URL + '/gists/' + gistId)
		if response.status_code == 200:
			return response.json()

		raise Exception('The gist not exist')
