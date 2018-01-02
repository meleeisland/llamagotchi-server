import os
import sys
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import SocketServer
import urlparse

from src.LlamaClass import Llama
from src.BaseHTTPcustomServer import BaseHTTPcustomServer

from src.utils import unpack_dict,pack_dict,userid_in_users,get_llama_id,add_to_users,remove_from_users,get_llamas_ids,savefile_name

from src.LlamaDB import get_llama,edit_llama,usersdb,get_userid_from_credentials

class S(BaseHTTPcustomServer):
    def check_login(self,data):
		ok = False
		try:
			t = self.extract_json(data["type"])
			if t == "login" :
				username = self.extract_json(data["username"])
				password = self.extract_json(data["password"])
				ok = get_userid_from_credentials(username,password)
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
		except KeyError : 
			return { "type" : "keepalive", "data" : "false" }
			
    def getHappiness(self,llama) :
		happy = -1
		try:
			if (llama != None):
				happy = llama.llamagotchi.getHappiness() 
		except KeyError:
			pass
		if happy != -1 :
			return { "type" : "happiness", "data" : happy }
		return { "type" : "error", "data" : "suca" }
    def getSave(self,llama,u) :
		data = ""
		llama.save(savefile_name(u))
		if (llama != None):
			data = llama.getName() + " saved" 
		if data != "" :
			return { "type" : "name", "data" : data }
		return { "type" : "error", "data" : "suca" }
    def getLogout(self,llama,u) :
		data = ""
		if u != False :
			llama.save()
			edit_llama(u,None)
			remove_from_users(u)
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
		edit_llama(u,Llama(""))
		llama = get_llama(u)
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
			sessionID = add_to_users(login)
			llama = get_llama(login)
			if llama == None :
				llama = Llama("Calogero")
				if (  os.path.isfile(savefile_name(login)) == False ) :
					t = "new"
					llama.save(savefile_name(login))
				else :
					t = "load" 
					llama.load(savefile_name(login))
				edit_llama(login,llama)
				return {"type" : t ,"data" : llama.getName() ,"uid" : sessionID + 1}
				
			return {"type" : "load" ,"data" : llama.getName() ,"uid" : sessionID + 1}
		return { "type" : "error", "data" : "suca" }
class LlamaServer :		
	def __init__(self, address = "0.0.0.0",port =8080):
		self.address = address
		self.port = port
		self.httpd = HTTPServer((self.address,self.port), S )		
	def start(self) :
		print 'Starting httpd...'
		self.httpd.serve_forever()
