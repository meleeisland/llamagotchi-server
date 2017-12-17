import sys
import json
import socket
from src.utils import unpack_dict,pack_dict
	
class LlamaClient :
	
	def __init__(self, address,port,u,p):
		self.address = address
		self.port = port
		self.username = u
		self.password = p
		self.uid = 0
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((address, port))
		self.uid = self.send_login(u,p)
		
		self.commands = {}
		self.commandsfun = {}	
	def user_id(self) :
		return self.uid
	

	def new_game_message(self):
		return 'New Game';
	
	
	def send_login(self,username,password) :
		print >>sys.stderr, 'sending login message "%s":"%s"' % (username, password)
		data,len = self.send("login",username + ":" + password)
		t,v,u = unpack_dict(data)
		if (t == "new") : 
			print self.new_game_message()
			print 'baaah'
			return u
		if (t == "load") : return u
		return False
		
		
	

	def send(self,type,message,EXPECTED_LEN=128) :
		MAXLEN=120
		data = ""
		try:
			# Send data
			print >>sys.stderr, 'sending  message "%s":"%s"' % (type, message)
			msg,l = pack_dict(type,message[:MAXLEN],self.user_id())
			self.socket.send(msg)
			# Look for the response
			amount_received = 0
			#~ amount_expected = EXPECTED_LEN
			data = self.socket.recv(EXPECTED_LEN)
			amount_received += len(data)
			#~ if  amount_received < amount_expected:
			#~ somethings wrong
			print >>sys.stderr, 'received "%s"' % data
		finally:
			print >>sys.stderr, 'closing socket'
			self.socket.close()
		return data,amount_received
	
	
	
	def exit(self,v):
		print "bye"
		sys.exit(v)
	def execute_cmd(self,cmd):
		cmdData = None
		try:
			cmdData = self.commands[cmd]
			d,l = self.send(cmdData["msg"],cmdData["data"])
			print d
			return True
		except KeyError:
			pass
		try:
			cmdFun = self.commandsfun[cmd]
			d = cmdFun(self)
			return d
			return True
		except KeyError:
			return False
	def addFun(self,cmd,fun) :
		self.commandsfun[cmd] = fun
	def addCMD(self,cmd,msg,data="") :
		self.commands[cmd] = {"msg":msg,"data":data}
	def start(self) :
			
		while True :
		
			cmd = raw_input("Llamagotchi $> ")	
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.address, self.port))
			print cmd
			if not self.execute_cmd(cmd) :
				uid = self.user_id()
				self.send("log-"+str(uid),str(uid) + " " +cmd)


