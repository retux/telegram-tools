# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import re

class MinionLauncher:
	def __init__(self):
		self.MasterGru = 'Matías_Retux'
		self.DownloadDir = '/tmp'
		self.Command = ""

	
# Example of parent class, returns server's uptime
class MinionUptime(MinionLauncher):
	def __init__(self):
		self.Command = "getUptime"

	def GetUptime(self):
		try:
			p = Popen(["uptime"], stdout=PIPE)
			return p.communicate()[0]
		except:
			return "Error: no uptime available."


# parent class, returns fortune cookie
class MinionGetFortune(MinionLauncher):
	def __init__(self):
		self.Command = "getFortune"

	def GetFortune(self):
		try:
			p = Popen(["fortune"], stdout=PIPE)
			FortuneNoLF = re.sub(r'\n', " ", p.communicate()[0])
			return ' ' + FortuneNoLF
			#return ' ' + p.communicate()[0]
		except:
			return " Error: no fortune now. Is fortune package installed?"



