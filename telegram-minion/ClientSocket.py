# -*- coding: utf-8 -*-

'''
This class just wraps a simple single-threaded socket client to talk with
Telegram-cli client/server.
'''
import socket
from datetime import datetime

class ClientSocket:
	def __init__(self):
		self.port = 2391
		self.host = 'localhost'
		self.logging = True
		self.alive = False
		self.data = ''		# string received
		self.message = ''	# string to be sent
		self.logDir = '/tmp'
		self.logFile = 'miniontalk.log'
		self.errorCode = ''
		self.errorMessage = ''
		self.socket = None
		self.remoteIP = None
		self.timestamp = None

		if self.logging:
			try:
				self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%s')
				self.fd = open (self.logDir + '/' + self.logFile, 'a')
				
			except IOError as e:
				print "I/O error({0}): {1}".format(e.errno, e.strerror)	
				self.Logging = False
			if (self.logging): self.fd.write( self.timestamp + ' Opening connection with telegram-cli\n')	
		
	
	def __del__(self):
		self.UpdateTimestamp()
		if (self.logging): self.fd.close()	
		if (self.socket): self.socket.close()

	def UpdateTimestamp(self):
		self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%s')

	def Create(self):
		try:
			self.UpdateTimestamp()
			#create an AF_INET, STREAM socket (TCP)
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.alive = True
			if self.logging:
				self.fd.write( self.timestamp + ' Socket created\n')
		except socket.error, msg:
			if self.logging:
				self.fd.write( self.timestamp +  ' Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1] )
			self.alive = False
		


	def Resolve(self):
		self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%s')
		try:
			self.remoteIP = socket.gethostbyname( self.host )
			self.alive = True
		except socket.gaierror:
			#could not resolve hostname, man!
			self.alive = False
			if (self.logging): self.fd.write( self.timestamp + ' Hostname could not be resolved. Exiting\n')


	def Connect(self):
		self.UpdateTimestamp()
		try:
			self.socket.connect((self.remoteIP , self.port))
			self.alive = True
			if self.logging:
				self.fd.write( self.timestamp + ' Socket connected to ' + self.host + ' on ip ' + self.remoteIP + '\n')

		except socket.error, msg:
			self.alive = False
			if self.logging:
				self.fd.write( self.timestamp + ' Failed to connect to socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1] )


	def SendData(self, message):
		self.UpdateTimestamp()
		try :
			if message:
				self.socket.sendall(message)
			self.alive = True
			if self.logging:
				self.fd.write( self.timestamp + ' Sent data: ' + message)

		except socket.error:
			#Send failed
			self.alive = False
			if self.logging:
				self.fd.write( self.timestamp + ' Failed to send data remote socket \n')

	def ReceiveData(self):
		self.UpdateTimestamp()
		try:
			reply = self.socket.recv(4096)
			if (reply):
				self.data = reply
				self.alive = True
				self.data = reply
				# logs the received data
				if self.logging:
					self.fd.write(self.timestamp + ' Data received: ' + reply)
				return reply
			else:
				self.alive = False
				if self.logging:
					self.fd.write( self.timestamp + ' Disconnected by remote server\n')
		except socket.error:
			if self.logging:
				self.fd.write( self.timestamp +' Failed trying to read socket \n')


	def Close(self):
		if self.socket: self.socket.close()

	def add2Log(self, msg):
		if (self.logging): 
			UpdateTimestamp()
			self.fd.write( self.timestamp + msg)	
