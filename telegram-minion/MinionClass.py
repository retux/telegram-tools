# -*- coding: utf-8 -*-

import subprocess	
import re
import sqlite3

SQLITE_WEATHER = 'weather-data.sql'

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
			p = subprocess.Popen(["uptime"], stdout=subprocess.PIPE)
			return p.communicate()[0]
		except:
			return "Error: minion says no uptime available."


# child class, returns fortune cookie
class MinionGetFortune(MinionLauncher):
	def __init__(self):
		self.Command = "getFortune"

	def GetFortune(self):
		try:
			# Adapt to fit your needs: /usr/games/fortune is where fortune is installed in Debian.
			p = subprocess.Popen(["/usr/games/fortune"], stdout=subprocess.PIPE)
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


class MinionGetBAWeather(MinionLauncher):
	def __init__(self):
		self.Command = "getBAweather"
		
	def GetConditions(self):
		try:	
			str2send = ""
			db = sqlite3.connect(SQLITE_WEATHER)
			cursor = db.cursor()
			cursor.execute('SELECT * FROM current_condition')
			row = cursor.fetchone()
			while row != None:
				str2send =  ' ' + str(row[0]) + ': ' + str(row[1]) + ' C, hum.: ' + str(row[2]) + '% PA: ' + str(row[3]) + ', visibilidad: ' + str(row[5]) + '. Hora obs.: ' + str(row[6]) + ' GMT. Datos de World Weather API.'
				# Don't forget fetching at last, cos' not using while (True):
				row = cursor.fetchone()
			return str2send
		except Exception as Error:
			return "SQLite Error: " + str(Error)
		finally:
			db.close()



class MinionGetTalk(MinionLauncher):
	def __init__(self, Contact=None, text2Speech=None):

		self.Command = 'sendSpeech'
		self.Contact = Contact
		self.Text2Speech = text2Speech
		self.State = False
		self.FileReady = False
		# To enable minion speak, these dependencies must be met: festival (General multi-lingual speech synthesis system)
		# Aditional language package for your own national language can be installed too. For spanish I'm using
		# festvox-palpc16k (Male Spanish voice Voz for Festival).
		# For mp3 encoding: lame (Open source MP3 encoder).
		# Audio tools (optionals) in order to minion to speak

		self.FestivalUtil = 'text2wave'
		self.MP3Enc = 'lame'
		self.AudioFile = '/tmp/salida.mp3'
		self.DepMsg = None
		self.CheckDependencies()
		if self.State:
			self.GetSpeech()



	def CheckDependencies(self):
		# Remember, this version is for *nix, windows version should be different
		if subprocess.call([ 'which', self.FestivalUtil ], stdout=subprocess.PIPE) == 0:
			if subprocess.call([ 'which', self.MP3Enc ], stdout=subprocess.PIPE) == 0:
				self.State = True
			else:
				self.DepMsg = self.MP3Enc + ' not found, install it using pakage manager.'
				self.State = False
		else:
			self.DepMsg = self.FestivalUtil + ' not found, install it using pakage manager.'
			self.State = False

	def GetSpeech(self):
		if len(self.Contact) == 0 and len(self.Text2Speech) == 0:
			self.DepMsg = "No message or contact provided!"
			self.State = False
			return False

		try:
			p = subprocess.Popen(["echo '" + self.Text2Speech + "'" + " | " + self.FestivalUtil + " | " + self.MP3Enc + " --quiet -V9 -b 32 --vbr-new - > " + self.AudioFile ], shell=True)
			res = p.wait()
			if res == 0:
				self.State = True
				self.FileReady = True
				return True
			else:
				return False
		except:
			self.DepMsg = "Error trying to create audio file. Dep missing?"
			self.State = False
			self.FileReady = False
			return False


