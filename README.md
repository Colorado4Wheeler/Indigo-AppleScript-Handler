# AppleScript Handler for Indigo

This plugin allows you to save your AppleScripts into a folder and then select an AppleScript to run as an Indigo action.

## Script Folder

Simply save your AppleScripts as native *.scpt files to the plugin preference folder found under:

	/Library/Application Support/Perceptive Automation/Indigo 7/Preferences/Plugins/com.eps.indigoplugin.applescript-handler

## Running an Action in Indigo

In Indigo create a new action, select AppleScript Handler -> Run AppleScript and select the script you want to run.  You can also store any returned value in an existing variable, new variable or directly in the plugin.  When storing to a variable it will be converted to a string representation, while storing directly to the plugin will always store the native data type that was returned.

## Running an Action Remotely or Via A Script

You can also run AppleScripts from a Python script and any results retured by the script will be returned to the caller.  For example:

	plugin = indigo.server.getPlugin('com.eps.indigoplugin.applescript-handler')
	if plugin.isEnabled:
		props = {'script': 'Play iTunes'}
		result = plugin.executeAction('runScript', deviceId=0, waitUntilDone=True, props=props)
		
## Retrieving a Stored Value From The Plugin

You can connect to the plugin to get a stored value in its native type as long as you pass the 'variable' key in props.  For example:

	plugin = indigo.server.getPlugin('com.eps.indigoplugin.applescript-handler')
	if plugin.isEnabled:
		props = {'variable': 'ScriptResult'}
		result = plugin.executeAction('getStoredValue', deviceId=0, waitUntilDone=True, props=props)
		
## Retrieving a List of Stored Variables

From the menu you can select the option to "List All Saved Variable Names" to see what the plugin is storing.		