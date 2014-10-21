#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configurations: MASTER_GRU is the only peer from who the commands will be accepted.
"""

MASTER_GRU = 'Matías_Retux'


import time
import re
from ClientSocket import ClientSocket
from MinionClass import *
def main():

	while True:
		myMinion = ClientSocket()
		myMinion.host = 'localhost'
		myMinion.port = 2391

		myMinion.Create()

		if myMinion.socket and myMinion.alive:
			myMinion.Resolve()
	
		if myMinion.socket and myMinion.alive:
			myMinion.Connect()
		
		if myMinion.socket and myMinion.alive:
			myMinion.SendData('main_session\r\n')
	

		#if myMinion.socket and myMinion.alive:
		#	myMinion.SendData('contact_list\r\n')
	
				
		if myMinion.socket and myMinion.alive:
			while True and myMinion.alive:
				data = myMinion.ReceiveData()
				# // print "Debug data rx: " + str(data)
				result = parseCommand(data)
				if result != -1 and result != None:
					myMinion.SendData(str(result))
			
		# if gets out of this while, then it means socket is broken, so wait 30 seconds and try to 
		# reconnect.
		if myMinion.socket: myMinion.Close()
		time.sleep(10)

	

def parseCommand(reply):
	command = ""

	try:
		# Agregar validacion de Gru
		data = re.sub(r'^ANSWER.*', "", reply)
		if re.search( r'«««', data):		
			header, message = data.split('«««', 1)
		if re.search( r' >>>', data):		
			header, message = data.split('>>>', 1)

		#reply = None
		hour, peer = header.split(']', 1)
		messageID, msgTime = hour.split('[', 1)
		messageID = messageID.strip()
		peer = peer.strip()
		peer = re.sub(r' ', "_", peer)
		# // BOF Just for some debugging
		#print "msgID: " + messageID
		#print "hour: " + hour
		#print "peer: " + peer
		#print "message: " + message
		# // EOF for dubbugging
		# // Check for commands
		if re.search( r'miniondo=', message):
			minion, command = message.split('=', 1)
			command = command.strip()
			if command == 'getUptime':
				myMinionDo = MinionUptime()
				# This is my master, from him I'll accept commands
				myMinionDo.MasterGru = MASTER_GRU
				str2Send = 'msg ' + peer + myMinionDo.GetUptime() + "\r\n"				
				#// print 'Debug str2Send=' + str2Send
				myMinionDo = None		# // delete the object
				return str(str2Send)
			# get fortune cookie
			if command == 'getFortune':
				myMinionDo = MinionGetFortune()
				myMinionDo.MasterGru = MASTER_GRU
				Fortune = myMinionDo.GetFortune()
				Fortune = re.sub(r'\t', "   ", Fortune)
				str2Send = 'msg ' + peer + Fortune + "\r\n"				
				myMinionDo = None		# // delete the object
				return str2Send
			else:
				return -1
		# // Check for other actions, like receiving pics or files. Asked by @esturniolo
		if message.strip() == "[photo]":
			# /// print "Debug foto recibida! MessageID=" + str(messageID)
			myMinionDo = MinionGetPic(messageID) # // provide messageID to object
			myMinionDo.MasterGru = MASTER_GRU
			str2Send = myMinionDo.GetPic() + "\r\n"
			myMinionDo = None	# // delete the object
			if re.search( r'^Error', str2Send):
				return 'msg ' + peer + str2Send + '\r\n'
			return str2Send
		# // file reception, asked by @esturniolo
		# // we filter txt file
		if re.search( r'^\[document.*\.txt.*', message.strip() ):
			# // print "Debug file recibida! MessageID=" + str(messageID)
			myMinionDo = MinionGetFile(messageID) # // provide messageID to object
			myMinionDo.MasterGru = MASTER_GRU
			str2Send = myMinionDo.GetFile() + "\r\n"
			myMinionDo = None	# // delete the object
			if re.search( r'^Error', str2Send):
				return 'msg ' + peer + str2Send + '\r\n'
			return str2Send


		

	except:
		pass


if __name__ == "__main__":
	main()


