#! /usr/bin/env python
# -*- coding: utf-8 -*-

import indigo

import os
import sys
import time
import datetime
import applescript
import glob
import re

################################################################################
# Indigo Plugin Class
################################################################################
class Plugin(indigo.PluginBase):
	
	CONFIGDIR = ""  # Initialized in startup
	
	###
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

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
	def run_applescript (self, action):
		"""
		Run an AppleScript from Actions.
		"""
		
		if not os.path.exists (u"{}/{}.scpt".format(self.CONFIGDIR, action.props['script'])):
			self.logger.error(u"Action to run AppleScript '{}' failed because that script does not exist in the folder".format(action.props['script']))
			return None
		
		self.logger.info (u"Running AppleScript '{}'".format(action.props['script']))
		script = applescript.AppleScript(path=u"{}/{}.scpt".format(self.CONFIGDIR, action.props['script']))
		response = script.run()
		
		if "extra" in action.props and action.props["extra"]:
			try:
				if action.props["extraAction"] == "storeNewVariable": 
					self.store_to_variable (action.props["name"], response)
				elif action.props["extraAction"] == "storeExistingVariable": 
					self.store_to_variable (action.props["variable"], response)
				elif action.props["extraAction"] == "storePlugin": 
					self.store_to_plugin (action.props["name"], response)
			except:
				pass
		
		return response
		
	###
	def get_stored_value (self, action):
		"""
		Hidden action return a stored value, must specify 'variable' in props.
		"""
		
		if not 'variable' in props:
			self.logger.error (u"Script attempted to retrieve a stored value but didn't pass a 'variable' property")
			return None
			
		if not u"saved_{}".format(props["variable"]) in self.pluginPrefs:
			self.logger.error (u"Script attempted to retrieve a stored value '{}' that value was never saved")
			return None		
			
		return self.pluginPrefs[u"saved_{}".format(props["variable"])]
		
	###
	def list_stored_variables (self):
		"""
		Read the pluginPrefs and output a list of all saved_* values.
		"""
		
		output = ""
		for key, value in self.pluginPrefs.iteritems():
			if key.startswith("saved_"): output += u"{}\n".format(key).replace("saved_", "")
			
		if output == "":
			self.logger.info("No variables have been saved to the plugin")
			return
			
		output = u"Values being saved in {}:\n{}".format(self.pluginDisplayName, output)
			
		self.logger.info(output)
		
	###
	def store_to_variable (self, variable, value):
		"""
		Store the value into a variable, creating it if needed.
		
		Arguments:
			variable:		name of the variable
			value:			value to unicode to the variable value
		"""
		
		if not variable in indigo.variables:
			try:
				indigo.variable.create(variable, u"{}".format(value))
			except:
				self.logger.error (u"Unable to create variable '{}', please check that it is a valid name, your AppleScript return value was not stored".format(variable))
		else:
			v = indigo.variables["MyVarName"]
			v.value = u"{}".format(value)
			v.replaceOnServer()
			self.logger.info(u"Variable '{}' has been updated from AppleScript".format(variable))
			
	###
	def store_to_plugin (self, variable, value):
		"""
		Store the actual value to the pluginPrefs with a prefix of 'saved_'.
		
		Arguments:
			variable:		name of the variable
			value:			value to unicode to the variable value
		"""
		
		try:
			self.pluginPrefs[u"saved_{}".format(variable)] = value
			self.logger.info(u"Plugin value '{}' has been updated from AppleScript".format(variable))
		except:
			self.logger.error (u"Unable to create variable '{}', please check that it is a valid name, your AppleScript return value was not stored".format(variable))
	
	###
	def get_folder_scripts (self, filter="", valuesDict=None, typeId="", targetId=0):
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
			
	###
	def validateActionConfigUi(self, valuesDict, typeId, deviceId):
		"""
		Validate action form.
		"""
		
		errorsDict = indigo.Dict()
		
		if re.match('^[\w-]+$', valuesDict["name"]) is None:
			errorsDict["showAlertText"] = "Variable names must contain only alphanumeric letters or underscores."
			errorsDict["name"] = "Invalid character(s)"
			return (False, valuesDict, errorsDict)
			
		return (True, valuesDict, errorsDict)






















 