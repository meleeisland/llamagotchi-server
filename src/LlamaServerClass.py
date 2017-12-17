import os
import sys
import socket

from src.LlamaClass import Llama

from src.utils import unpack_dict,pack_dict,userid_in_users,get_llama_id,add_to_users,remove_from_users,get_llamas_ids,savefile_name

from src.LlamaDB import get_llama,edit_llama,usersdb
	
	
class LlamaServer :
	
	def __init__(self, address,port):
		self.address = address
		self.port = port
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind((address, port))
		serversocket.listen(5) # become a server socket, maximum 5 connections
		self.socket = serversocket
		
		self.commands=["pet","logout","sname","gname","ghappy","save","new"]
	
	
	
	
	
	
	def is_clean_request(self,data):
		if len(data) == 0 : return False
		return True
	def is_logged_request(self,data):
		type,userdata,userid = unpack_dict(data)
		return userid_in_users(userid)
	
	
	
	
	
	
		
	def login_request(self,data):
		print >>sys.stderr, 'received "%s"' % data		
		errormsg,errorl=pack_dict("fail","suca",0)
		
		
		
		type,userdata,u = unpack_dict(data)
		if (type != "login") : return False
		userdata = userdata.split(":")
		username = userdata[0]
		password = userdata[1]
		user_id = False
		i = 1
		for u in usersdb:
			if u["user"] == username and u["pass"] == password:
				user_id = i
			i = i+1
		if user_id == False : 
			return False,error
		else :
			uid = add_to_users(user_id)
			savefile = "save-" + str(user_id - 1)+".json"
			llama = usersdb[user_id-1]["llama"]
			if llama == None:
				llama = Llama("Calogero")	
				if (  os.path.isfile(savefile) == False ) :
					llama.save(savefile)
					m = llama.getName()
					msg,l=pack_dict("new",m,uid+1)
				else :
					llama.load(savefile)
					m = llama.getName()
					msg,l=pack_dict("load",m,uid+1)
				usersdb[user_id-1]["llama"] = llama
			return True,msg
				
				
				
				
				
				
				
				
				
					
	def newCMD(self,t,v,u):
	
		print "new llama for users["+str(u-1)+"] -> " + v
		edit_llama(u,Llama(""))
		llama = get_llama(u)
		if (llama != None):
			data,l = pack_dict("text",llama.getName(),u)
			self.connection.sendall(data)
		else :
			data,l = pack_dict("error","",u)
			self.connection.sendall(data)
	def snameCMD(self,t,v,u):
	
		print "setting name for users["+str(u-1)+"] -> " + v
		llama = get_llama(u)
		llama.setName(v)
		if (llama != None):
			data,l = pack_dict("text",llama.getName(),u)
			self.connection.sendall(data)
		else :
			data,l = pack_dict("error","",u)
			self.connection.sendall(data)
	def saveCMD(self,t,v,u):
		print "saving users["+str(u-1)+"]"
		llama = get_llama(u)
		llama.save(savefile_name(u))
		if (llama != None):
			data,l = pack_dict("text","saved",u)
			self.connection.sendall(data)
	def gnameCMD(self,t,v,u):
		print "getting name from users["+str(u-1)+"]"
		llama = get_llama(u)
		if (llama != None):
			data,l = pack_dict("text",llama.getName(),u)
			self.connection.sendall(data)
	def logoutCMD(self,t,v,u):
		print "removing users["+str(u-1)+"]"
		edit_llama(u,None)
		remove_from_users(u)
	def ghappyCMD(self,t,v,u):
		print "getting happiness for users["+str(u-1)+"]"
		llama = get_llama(u)
		if (llama != None):
			data,l = pack_dict("text",llama.llamagotchi.getHappiness(),u)
			self.connection.sendall(data)
	def petCMD(self,t,v,u):
		print "executing pet for users["+str(u-1)+"]"
		llama = get_llama(u)
		llama.llamagotchi.pet()
		if (llama != None):
			data,l = pack_dict("text","baaah!",u)
			self.connection.sendall(data)
			
			
			
			
			
			
	def handle_data(self,data):
		t,v,u = unpack_dict(data)
		
		if (t in self.commands) :
			getattr(self, t+"CMD")(t,v,u)
		else :
			print >>sys.stderr, 'sending data back to the client'
			self.connection.sendall(data)
			
		
		
		
	def wait_connect(self):
		print >>sys.stderr, 'waiting for a connection'
		self.connection, self.client_address = self.socket.accept()
		print >>sys.stderr, 'connection from', self.client_address
		
		
	def get_package(self):
		while True:
			data = self.connection.recv(128)
			if self.is_clean_request(data):
				if self.is_logged_request(data) : 
					print >>sys.stderr, 'received "%s"' % data
					if data:						
						self.handle_data(data)
						break
				else:
					login_ok,msg = self.login_request(data)
					self.connection.sendall(msg)
					break
			
			else:
				print >>sys.stderr, 'no more data from', self.client_address
				break
		
	def close(self):
		# Clean up the connectionna
		self.connection.close()			
				
	def start(self) :
		while True:
			self.wait_connect()
			try:
				self.get_package()
			finally:
				self.close()
