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
			return "Error: minion says no uptime available."


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
			return " Error: no fortune now for minion. Is fortune package installed?"

# // Gets photo by msg_id, specially suited for @esturniolo's needs
# // this class don't do very much, just sanitize a little msg_id

class MinionGetPic(MinionLauncher):
	def __init__(self, message_id):
		self.msg_id = message_id

	def GetPic(self):
		try:
			if int(self.msg_id) >= 0:
				return "load_photo " + str(self.msg_id)
			else:
				return "Error, minion got a suspicious message id."
		except:
			return "Error, minion got an incorrect message id."


# // Gets file by msg_id, specially suited for @esturniolo's needs
# // this class don't do very much, just sanitize a little msg_id

class MinionGetFile(MinionLauncher):
	def __init__(self, message_id):
		self.msg_id = message_id

	def GetFile(self):
		try:
			if int(self.msg_id) >= 0:
				return "load_document " + str(self.msg_id)
			else:
				return "Error, minion got a suspicious message id."
		except:
			return "Error, minion got an incorrect message id."

