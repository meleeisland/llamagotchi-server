import sys
import json
import requests
import json
from src.utils import unpack_dict,pack_dict
from urllib import urlencode

class LlamaClient :
	
	def __init__(self, address,port,u,p):
		self.address = address
		self.port = port
		self.username = u
		self.password = p
		self.uid = 0
		self.uid = self.send_login(u,p)
		
		self.commands = {}
		self.commandsfun = {}	
	def user_id(self) :
		return self.uid
	

	def new_game_message(self):
		return 'New Game';
	
	
	def send_login(self,username,password) :
		print >>sys.stderr, 'sending login message "%s":"%s"' % (username, password)
		data = self.send("POST","login",{"type":"login","username":username , "password" : password })
		data = json.loads(data.content)
		try :
			if (data["type"] == "new") : 
				print self.new_game_message()
				print 'baaah'
				return data["uid"]
			if (data["type"] == "load") : return data["uid"]
		except KeyError :
			pass
		return False
		
		
	

	def send(self,meth,type,message) :
		r = False
		if meth == "GET" :
			url = "http://"+self.address+":"+str(self.port )+"/"+type+"/"
			if message == "" :
				message = {}
			message["uid"] = self.user_id()
			message["type"] = type
			if message != "" :
				url = url + "?" + urlencode(message)
			r = requests.get(url)
		elif  meth == "POST":
			url = "http://"+self.address+":"+str(self.port )+"/"+type+"/"
			if message == "" :
				message = {}
			message["uid"] = self.user_id()
			message["type"] = type
			r = requests.post(url,data=message)
		else :
			print "Unknown method " + meth
			
		return r
	
	
	
	def exit(self,v):
		print "bye"
		sys.exit(v)
	def execute_cmd(self,cmd):
		cmdData = None
		try:
			cmdData = self.commands["GET"][cmd]
			print cmdData
			print cmd
			d = self.send("GET",cmdData["msg"],cmdData["data"])
			print d.text
			return True
		except KeyError:
			pass
		try:
			cmdData = self.commands["POST"][cmd]
			d = self.send("POST",cmdData["msg"],cmdData["data"])
			print d.text
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
	def addCMD(self,meth,cmd,msg,data="") :
		try :
			x = self.commands[meth]
			self.commands[meth][cmd] = {"msg":msg,"data":data}
		except KeyError:
			self.commands[meth] = {}
			self.commands[meth][cmd] = {"msg":msg,"data":data}
	def start(self) :
			
		while True :
		
			cmd = raw_input("Llamagotchi $> ")	
			print cmd
			if not self.execute_cmd(cmd) :
				uid = self.user_id()
				self.send("GET","log-"+str(uid),"")


