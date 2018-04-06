# AppleScript Handler for Indigo

This plugin allows you to save your AppleScripts into a folder and then select an AppleScript to run as an Indigo action.

## Script Folder

Simply save your AppleScripts as native *.scpt files to the plugin preference folder found under /Library/Application Support/Perceptive Automation/Indigo 7/Preferences/Plugins/com.eps.indigoplugin.applescript-handler. 

## Running an Action in Indigo

In Indigo create a new action, select AppleScript Handler -> Run AppleScript and select the script you want to run.

## Running an Action Remotely or Via A Script

You can also run AppleScripts from a Python script and any results retured by the script will be returned to the caller.  For example:

	plugin = indigo.server.getPlugin('com.eps.indigoplugin.applescript-handler')
	if plugin.isEnabled:
		props = {'script': 'Play iTunes'}
		result = plugin.executeAction('scriptRun', deviceId=0, waitUntilDone=True, props=props)
		