# -*- coding: utf-8 -*-

import json, os, sys

def getFile (path, prop = 'r'):
	if os.path.exists(path):
		return open(fullPath, prop)

	return False

def replaceContentFile (path, content):
	pass	

def getFullPath (filenamePath):
	if dirname != "":
		return dirname + os.pathsep + filenamePath
	
	return filenamePath

def excludeValues (l, e):
	try:
		for el in e:
			 l.remove(el)
	except Exception as e:
		pass

	return l

def getSeparator ():
	return "\\" if sys.platform.startswith('win') else "/"
