# -*- coding: utf-8 -*-

from sync_settings.libs.gist_api import Gist
from sync_settings.libs.exceptions import GistException
from tests import *
from unittest import TestCase

class TestGistAPI(TestCase):
  def __init__(self, *args, **kwargs):
    super(TestGistAPI, self).__init__(*args, **kwargs)
    self.api = Gist(opts.get('access_token'))

  def test_access_token(self):
    with self.assertRaises(GistException):
      Gist('')
    self.assertIsInstance(self.api, Gist)
    self.assertIsNotNone(self.api)

  def test_create_gist(self):
    data = {'description': 'test description'}

    # Try to create a gist with invalid data
    # Without files object
    with self.assertRaises(GistException):
      self.api.create(data)
    # With a wrong 'files' object
    with self.assertRaises(GistException):
      self.api.create({
        'description': 'some description',
        'files': 'some files'
      })

    # Create a gist with empty content
    with self.assertRaises(GistException):
      self.api.create({
        'description': 'some description',
        'files': {
          'file_test.txt': {
            'content': ''
          }
        }
      })

    # Create a gist without description
    gist = self.api.create({
      'files': {
        'file.txt': {
          'content': 'content for this file.txt'
        }
      }
    })
    self.assertIsNotNone(gist.get('id'))
    # Delete test gist
    self.assertTrue(self.api.delete(gist.get('id')))

    # Create a gist with description and files
    data.update({ 'files': {
      'someFile': {
        'content': 'Content of this file'
      }
    }})
    gist = self.api.create(data)
    self.assertIsNotNone(gist.get('id'))
    gist_id = gist.get('id')

    # Get a list with all public gists
    gist_items = self.api.list()

    # Check if the created gist isn't public gist list
    for gist_item in gist_items:
      if gist_id == gist_item.get('id'):
        self.assertFalse(gist_item.get('public'))

    # Delete test gist
    self.assertTrue(self.api.delete(gist_id))

  def test_edit_gist(self):
    test_gist = self.api.create({
      'files': {
        'test_gist.txt': { 'content': 'Gist test content' }
      }
    })
    # Get possible errors
    # Passing wrong parameters
    test_gist_id = test_gist.get('id')
    with self.assertRaises(GistException):
      self.api.edit('some_id', {})
    # With wrong files object
    with self.assertRaises(GistException):
      self.api.edit(test_gist_id, {
        'files': 'some content'
      })

    # Updating without changes
    gist = self.api.edit(test_gist_id, {})
    self.assertIsNotNone(gist.get('id'))
    self.assertEqual(len(gist.get('files')), 1)

    # Adding a new file
    gist = self.api.edit(test_gist_id, {
      'files': { 'other_file.txt': {
        'content': 'Some content'
      }}
    })
    self.assertIsNotNone(gist.get('id'))
    self.assertEqual(len(gist.get('files')), 2)

    self.assertTrue(self.api.delete(test_gist_id))

  def test_get_gist(self):
    test_gist = self.api.create({
      'files': {
        'test_gist.txt': { 'content': 'Gist test content' }
      }
    })
    test_gist_id = test_gist.get('id')
    # Getting errors
    with self.assertRaises(GistException):
      self.api.get('---')

    # Getting gist
    gist = self.api.get(test_gist_id)
    self.assertIsNotNone(gist.get('id'))
    self.assertEqual(test_gist_id, gist.get('id'))
    self.assertTrue(self.api.delete(test_gist_id))
