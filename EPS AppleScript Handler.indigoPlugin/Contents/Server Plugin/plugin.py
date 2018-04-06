#! /usr/bin/env python
# -*- coding: utf-8 -*-

import indigo

import os
import sys
import time
import datetime
import applescript
import glob

################################################################################
# Indigo Plugin Class
################################################################################
class Plugin(indigo.PluginBase):
	
	CONFIGDIR = ""  # Initialized in startup
	
	###
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = False
		self.devicestates = {}

	###
	def __del__(self):
		indigo.PluginBase.__del__(self)
	
	###
	def startup(self):
		self.CONFIGDIR = '{}/Preferences/Plugins/{}'.format(indigo.server.getInstallFolderPath(), self.pluginId)
		self.logger.info (u"AppleScript script path set to {}".format(self.CONFIGDIR))
			
		if not os.path.exists (self.CONFIGDIR):
			os.makedirs (self.CONFIGDIR)

	###	
	def shutdown(self):
		pass

	###
	def runConcurrentThread(self):
		try:
			while True:
				self.sleep(1)
					
		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.

	
	###
	def scriptRun (self, action):
		"""
		Run an AppleScript from Actions.
		"""
		
		self.logger.info (u"Running AppleScript '{}'".format(action.props['script']))
		script = applescript.AppleScript(path=u"{}/{}.scpt".format(self.CONFIGDIR, action.props['script']))
		response = script.run()
		
		return response
			
	###
	def getScripts (self, filter="", valuesDict=None, typeId="", targetId=0):
		"""
		Read preference folder for all scripts and return them as a list.
		"""
		
		try:
			retList = []
			
			scripts = glob.glob(self.CONFIGDIR + "/*.scpt")
			for script in scripts:
				scriptName = script.replace(self.CONFIGDIR + "/", "").replace(".scpt", "")
				retList.append ((scriptName, scriptName))
				
			return retList
			
		except Exception as e:
			self.logger.error(unicode(e))