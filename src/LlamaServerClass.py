from BaseHTTPServer import HTTPServer

import urlparse

from src.LlamaClass import Llama
from src.BaseHTTPcustomServer import BaseHTTPcustomServer


from src.llama_db import LlamaDb

def MakeLlamaServerFromArgs(init_args):
	class LlamaCustomHTTP(BaseHTTPcustomServer,object):
		def __init__(self, *args, **kwargs):
			 self.initCustomServer(init_args)
			 super(LlamaCustomHTTP, self).__init__(*args, **kwargs)
		def check_login(self,data):
			ok = False
			try:
				t = self.extract_json(data["type"])
				if t == "login" :
					username = self.extract_json(data["username"])
					password = self.extract_json(data["password"])
					ok = self.db.get_user_id_from_credentials(username,password)
			except KeyError:
				pass
			return ok	
				
			
				
		def do_GET(self):

			p = urlparse.urlparse(self.path)
			if p.path == "/ghappy/" :
				self.customGET(self.getHappiness)
			elif p.path == "/gname/" :
				self.customGET(self.getName)
			elif (p.path == "/keepalive/") :
				self.customGET(self.getKeepalive)
			elif p.path == "/save/" :
				self.customGET(self.getSave)
			elif p.path == "/logout/" :
				self.customGET(self.getLogout)
			else :
				self.customGET(self.getError)
		
		def getError(self):
			return { "type" : "error", "data" : "suca:nopath" }
		def getName(self,llama) :
			name = ""
			try:
				if (llama != None):
					name = llama.getName() 
			except KeyError:
				pass
			if name != "" :
				return { "type" : "name", "data" : name }
			return { "type" : "error", "data" : "suca" }
		def getKeepalive(self,llama) :
			try :
				val = llama.keepAlive() 
				return  { "type" : "keepalive", "data" : val }
			except (KeyError , AttributeError) as error :
				return { "type" : "keepalive", "data" : "false" }
				
		def getHappiness(self,llama) :
			happy = -1
			try:
				if (llama != False):
					happy = llama.llamagotchi.getHappiness() 
			except (KeyError , AttributeError) as error :
				pass
			if happy != -1 :
				return { "type" : "happiness", "data" : happy }
			return { "type" : "error", "data" : "suca" }
		def getSave(self,llama,u) :
			data = ""
			llama.save(u)
			if (llama != False):
				data = llama.getName() + " saved" 
			if data != "" :
				return { "type" : "name", "data" : data }
			return { "type" : "error", "data" : "suca" }
		def getLogout(self,llama,u,s) :
			data = ""
			if u != False :
				llama.save()
				self.db.set_llama(u,None)
				self.db.logout_user(s)
				return { "type" : "ok", "data" : "bye!" }
			return { "type" : "error", "data" : "suca" }		
		   
		   
		   
		   
		   
		   
		   
		   
		   
		   
		   
		   
		 
		   
		
		   
			
		def do_POST(self):
			
			if (self.path == "/login/") :
				self.customPOST(self.postLogin)	
			elif (self.path == "/pet/") :
				self.customPOST(self.postPet)
			elif (self.path == "/sname/") :
				self.customPOST(self.postSetName)
			elif (self.path == "/new/") :
				self.customPOST(self.postNew)
			else :
				self.customPOST(self.getError)
			
		def postNew(self,llama,u):
			self.set_llama(u,Llama(""))
			llama = self.get_llama(u)
			if (llama != None):
				return { "type" : "ok",	"data" :  "new llama : name <" + llama.getName() + ">" }
			return { "type" : "error", "data" : "suca" }
			
		def postSetName(self,llama,data):
			name = self.extract_json(data["name"])
			llama.setName(name)
			if (llama != None):
				return { "type" : "ok",	"data" :  "new name : name <" + llama.getName() + ">" }
			return { "type" : "error", "data" : "suca" }
			
		def postPet(self,llama,data):
			llama.llamagotchi.pet()
			return { "type" : "ok",	"data" :   "baah!" }
			
		def postLogin(self,data):
			login = self.check_login(data)
			if login != False :
				sessionID = self.db.login_user(login)
				llama,t = self.get_llama(login)
				return {"type" : t ,"data" : llama.getName() ,"uid" : sessionID }
			return { "type" : "error", "data" : "suca" }

	return LlamaCustomHTTP
class LlamaServer :		
	def __init__(self, address = "0.0.0.0",port =8080 , mongodb = None ):
		self.address = address
		self.port = port
		if mongodb == None : mongodb = LlamaDb("test")
		S = MakeLlamaServerFromArgs({"database" : mongodb })
		self.httpd = HTTPServer((self.address,self.port), S )		
	def start(self) :
		print 'Starting httpd...'
		self.httpd.serve_forever()
