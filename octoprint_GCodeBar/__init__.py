# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import sys
import re
import shlex 
import subprocess

class GcodebarPlugin(
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.TemplatePlugin
	):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)
	
    ##~~ AssetPlugin API
	def get_assets(self):
		return {
			"js": ["js/GCodeBar.js"],
			"css": ["css/GCodeBar.css"],
			"less": ["less/GCodeBar.less"]
		} 		
		
		
	def get_template_configs(self):
		return [dict(type="sidebar", name="EXO Extras", icon="print")]

	##~~ Softwareupdate hook
	def get_template_vars(self):
		with open('/proc/cpuinfo', 'r') as infile:
			cpuinfo = infile.read()
		match2 = re.search('^Serial\s+:\s+(\w+)$', cpuinfo, flags=re.MULTILINE | re.IGNORECASE)
		RPiSerial = match2.group(1)
		p2 = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE).stdout.read()
		RPiIPAdr = p2
		NetInfo = subprocess.Popen('iw wlan0 info', shell=True, stdout=subprocess.PIPE).stdout.read()
		match2=re.search('type\s+(\w+)$', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwMode = "Desconocido"
		else:
			if match2.group(1)=="managed":
				NetwMode = "Conectado a Red WiFi."
			elif match2.group(1)=="AP":
				NetwMode = "Modo Punto de Acceso."
			else:
				NetwMode = "WiFi desconectado Starting"

		match2=re.search('ssid\s+(\w+)$', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwSSid = "Desconocido"
		else:
			NetwSSid = match2.group(1)

		match2=re.search('channel\s+(\w+)\s', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwChann = "Desconocido"
		else:
			NetwChann = match2.group(1)

		match2=re.search('addr\s+(.*)$', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwMAC = "Desconocido"
		else:
			NetwMAC = match2.group(1)

		return dict(serial=RPiSerial,ipadr=RPiIPAdr,wifiname=NetwSSid,channel=NetwChann,netmode=NetwMode,mac=NetwMAC)
		

	def on_after_startup(self):
		self.startTimer(25.0)

	def startTimer(self, interval):
		self._checkTempTimer = RepeatedTimer(interval, self.checkRaspiNet, None, None, True)
		self._checkTempTimer.start()

	def checkRaspiNet(self):
		with open('/proc/cpuinfo', 'r') as infile:
			cpuinfo = infile.read()
		match2 = re.search('^Serial\s+:\s+(\w+)$', cpuinfo, flags=re.MULTILINE | re.IGNORECASE)
		RPiSerial = match2.group(1)
		p2 = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE).stdout.read()
		RPiIPAdr = p2
		NetInfo = subprocess.Popen('iw wlan0 info', shell=True, stdout=subprocess.PIPE).stdout.read()
		match2=re.search('type\s+(\w+)$', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwMode = "Desconocido"
		else:
			if match2.group(1)=="managed":
				NetwMode = "Conectado a Red WiFi"
			elif match2.group(1)=="AP":
				NetwMode = "Modo Punto de Acceso"
			else:
				NetwMode = "WiFi desconectado"

		match2=re.search('ssid\s+(\w+)$', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwSSid = "Desconocido"
		else:
			NetwSSid = match2.group(1)

		match2=re.search('channel\s+(\w+)\s', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwChann = "Desconocido"
		else:
			NetwChann = match2.group(1)

		match2=re.search('addr\s+(.*)$', NetInfo, flags=re.MULTILINE | re.IGNORECASE)
		if match2 is None:
			NetwMAC = "Desconocido"
		else:
			NetwMAC = match2.group(1)
		self._plugin_manager.send_plugin_message(self._identifier, dict(serial=RPiSerial,ipadr=RPiIPAdr,wifiname=NetwSSid,channel=NetwChann,netmode=NetwMode,mac=NetwMAC))
		
	def find_between( s, first, last ):
		try:
			start = s.index( first ) + len( first )
			end = s.index( last, start )
			return s[start:end]
		except ValueError:
			return ""		
			
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			gcodebar=dict(
				displayName="Gcodebar Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="mtowara",
				repo="OctoPrint-Gcodebar",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/therasoft/octoprint-GCodeBar/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Gcodebar Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = GcodebarPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

