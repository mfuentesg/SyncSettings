# -*- coding: utf-8 -*-

import sublime
from sublime_plugin import WindowCommand
from ..gistapi import Gist

class SyncSettingsAboutCommand (WindowCommand):
	def run (self):
		repoData = Gist.getCurrentRelease()
		sublime.message_dialog('Sync Settings Plugin\n\n Current Release: %s' % repoData.get('name'))
