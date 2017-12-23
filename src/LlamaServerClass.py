import os
import sys
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse

from src.LlamaClass import Llama

from src.utils import unpack_dict,pack_dict,userid_in_users,get_llama_id,add_to_users,remove_from_users,get_llamas_ids,savefile_name

from src.LlamaDB import get_llama,edit_llama,usersdb

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
	  
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")     
        self.send_header("Access-Control-Allow-Headers", "Content-Type")     
    def check_login(self,data):
		print data
		ok = False
		try:
			self.log(str(type(data["type"])))
			if type(data["type"]) is unicode : t = data["type"]
			elif type(data["type"]) is list : t = data["type"][0]
			if t == "login" :
				if type(data["username"]) is unicode : username = data["username"]
				elif type(data["username"]) is list : username = data["username"][0]
				if type(data["password"]) is unicode : password = data["password"]
				elif type(data["password"]) is list : password = data["password"][0]
				i = 1
				user_id = 0
				for u in usersdb:
					if u["user"] == username and u["pass"] == password:
						user_id = i
					i = i+1
				if user_id != 0 :
					ok = user_id
		except KeyError:
			pass
		return ok	
		
    def get_logged_user(self,post_data,type=""):
		print post_data
		data = post_data
		try:
			ok = False
			if type == "" :	ok = True
			if str(data["type"][0]) == type :	ok = True
			
			if ok :
				return int(data["uid"][0])
		except KeyError:
			pass
		return False	
		
		
    def loginRequest(self,post_data):
		self.log(str(post_data))
		is_ok = self.check_login(post_data)
		if is_ok != False :
			user_id = is_ok
			loggedUID = add_to_users(user_id)
			savefile = "save-" + str(user_id - 1)+".json"
			llama = usersdb[user_id-1]["llama"]
			if llama == None:
				llama = Llama("Calogero")	
				if (  os.path.isfile(savefile) == False ) :
					llama.save(savefile)
					data = {"type" : "new","data" : llama.getName() ,"uid" : loggedUID + 1}
					msg = json.dumps(data)
				else :
					llama.load(savefile)
					data = {"type" : "load","data" : llama.getName(),"uid" : loggedUID + 1}
					msg = json.dumps(data)
				usersdb[user_id-1]["llama"] = llama
			else : 
				data = {"type" : "load","data" : llama.getName(),"uid" : loggedUID + 1}
				msg = json.dumps(data)
			self.wfile.write(msg)
		else :
			data = {
				"type" : "error",
				"data" : "suca"
			}
			msg = json.dumps(data)
			self.wfile.write(msg)
			
    def petRequest(self,post_data):
		u = self.get_logged_user(post_data,"pet")
		ok = False
		data = ""
		try :
			if u != False :
				llama = get_llama(u)
				if (llama != None):
					llama.llamagotchi.pet()
					ok = True
					data = "baah!"
		except KeyError :
			pass
		if ok :
			data = {
				"type" : "ok",
				"data" : data
			}
			msg = json.dumps(data)
			self.wfile.write(msg)
		else :
			data = {
				"type" : "error",
				"data" : "suca"
			}
			msg = json.dumps(data)
			self.wfile.write(msg)
			
    def snameRequest(self,post_data):
		u = self.get_logged_user(post_data,"sname")
		ok = False
		data = ""
		try :
			if u != False :
				llama = get_llama(u)
				data = post_data
				if (llama != None):
					llama.setName(data["name"][0])
					ok = True
					data = llama.getName()
		except KeyError :
			pass
		if ok :
			data = {
				"type" : "ok",
				"data" : data
			}
			msg = json.dumps(data)
			self.wfile.write(msg)
		else :
			data = {
				"type" : "error",
				"data" : "suca"
			}
			msg = json.dumps(data)
			self.wfile.write(msg)			
    def newRequest(self,post_data):
		u = self.get_logged_user(post_data,"new")
		ok = False
		data = ""
		try :
			if u != False :
				edit_llama(u,Llama(""))
				llama = get_llama(u)
				if (llama != None):
					ok = True
					data = "new llama : name <" + llama.getName() + ">"
		except KeyError :
			pass
		if ok :
			data = {
				"type" : "ok",
				"data" : data
			}
			msg = json.dumps(data)
			self.wfile.write(msg)
		else :
			data = {
				"type" : "error",
				"data" : "suca"
			}
			msg = json.dumps(data)
			self.wfile.write(msg)
			
			
			
    def happyRequest(self,path) :
		q =  urlparse.parse_qs(path.query)
		ok = False
		happy = -1
		try :
			u = int( q["uid"][0])
			llama = get_llama(u)
			print llama
			if (llama != None):
				happy = llama.llamagotchi.getHappiness() 
		except KeyError :
			pass
		if happy > 0 :
			data = { "type" : "happiness", "data" : happy }
		else :				
			data ={ "type" : "error", "data" : "suca" }
		msg = json.dumps(data)
		self.wfile.write(msg)
		
    def gnameRequest(self,path) :
		q =  urlparse.parse_qs(path.query)
		ok = False
		name = ""
		try :
			u = int( q["uid"][0])
			llama = get_llama(u)
			print llama
			if (llama != None):
				name = llama.getName() 
		except KeyError :
			pass
		if name != "" :
			data = { "type" : "name", "data" : name }
		else :				
			data ={ "type" : "error", "data" : "suca" }
		msg = json.dumps(data)
		self.wfile.write(msg)
    def saveRequest(self,path) :
		q =  urlparse.parse_qs(path.query)
		ok = False
		data = ""
		try :
			u = int( q["uid"][0])
			llama = get_llama(u)
			llama.save(savefile_name(u))
			if (llama != None):
				data = llama.getName() + " saved" 
		except KeyError :
			pass
		if data != "" :
			data = { "type" : "name", "data" : data }
		else :				
			data ={ "type" : "error", "data" : "suca" }
		msg = json.dumps(data)
		self.wfile.write(msg)
    def logoutRequest(self,path) :
		q =  urlparse.parse_qs(path.query)
		ok = False
		data = ""
		try :
			u = int( q["uid"][0])
			print u
			if u != False :
				edit_llama(u,None)
				remove_from_users(u)
				print "removing users["+str(u-1)+"]"
				data = "bye!"
		except KeyError :
			pass
		if data != "" :
			data = { "type" : "ok", "data" : data }
		else :				
			data ={ "type" : "error", "data" : "suca" }
		msg = json.dumps(data)
		self.wfile.write(msg)
    def do_GET(self):

        self._set_headers()
        p = urlparse.urlparse(self.path)
        
        if p.path == "/ghappy/" :
			self.happyRequest(p)
				
        elif p.path == "/gname/" :
			self.gnameRequest(p)
        elif p.path == "/save/" :
			self.saveRequest(p)
        elif p.path == "/logout/" :
			self.logoutRequest(p)
				
        else :
			data = { "type" : "error", "data" : "suca:nopath" }
			msg = json.dumps(data)
			self.wfile.write(msg)
			
    def log(self,msg):
		BaseHTTPRequestHandler.log_message(self,msg)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
		content_length=int(self.headers['Content-Length']) 
		content_type=(self.headers['Content-Type']) 
		post_data = self.rfile.read(content_length) 
		content_type = content_type.split(";")
		if "application/json" in content_type :
			post_data = json.loads(post_data)
		else : post_data = urlparse.parse_qs(post_data)
		
		self._set_headers()
		
		
		
		if (self.path == "/login/") :
			self.loginRequest(post_data)
			
		elif (self.path == "/pet/") :
			self.petRequest(post_data)
		elif (self.path == "/sname/") :
			self.snameRequest(post_data)
		elif (self.path == "/new/") :
			self.newRequest(post_data)
		else :
			data = { "type" : "error", "data" : "suca:nopath" }
			msg = json.dumps(data)
			self.wfile.write(msg)
        
class LlamaServer :		
	def __init__(self, address = "0.0.0.0",port =8080):
		self.address = address
		self.port = port
		self.httpd = HTTPServer((self.address,self.port), S )		
	def start(self) :
		print 'Starting httpd...'
		self.httpd.serve_forever()
