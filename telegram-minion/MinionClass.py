# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import re
import sqlite3

SQLITE_WEATHER='weather-data.sql'

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


# child class, returns fortune cookie
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
				str2send =  ' ' + str(row[0]) + ': ' + str(row[1]) + ' C, hum.: ' + str(row[2]) + ' PA: ' + str(row[3]) + ', visibilidad: ' + str(row[5]) + '. Hora obs.: ' + str(row[6]) + ' GMT (por ahora). Datos de World Weather API.'
				# Don't forget fetching at last, cos' not using while (True):
				row = cursor.fetchone()
			return str2send
		except Exception as Error:
			return "SQLite Error: " + str(Error)
		finally:
			db.close()




