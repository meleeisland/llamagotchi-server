import os
import sys
import json
import socket

from src.LlamaClass import Llama

address = "localhost"
port = int( os.environ['PORT'])
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((address, port))
serversocket.listen(5) # become a server socket, maximum 5 connections



usersdb = [{"user":"pippo","pass":"pippo","llama" : None}]
users = {}

def unpack_dict(data):
	data = json.loads(data)
	type = data[0]
	values = data[1]
	user = data[2]
	return type,values,user
def pack_dict(t,m,u) :
	d = [t,m,u]
	a = json.dumps(d)	
	return a,len(a)

def get_llama(u):		
	user_id = users[u-1] - 1
	userdata = usersdb[user_id]
	llama = userdata["llama"]
	return llama
def edit_llama(u,llama):		
	user_id = users[u-1] - 1
	userdata = usersdb[user_id]
	userdata["llama"] = llama
def clean_request(data):
	if len(data) == 0 : return False
	return True
def logged_request(data):
	print data
	type,userdata,userid = unpack_dict(data)
	if userid - 1 in users.keys() :
		return True
	else: return False
	
def check_login(data):
	global usersdb
	
	print >>sys.stderr, 'received "%s"' % data
	type,userdata,u = unpack_dict(data)
	if (type != "login") : return False
	userdata = userdata.split(":")
	username = userdata[0]
	password = userdata[1]
	login = False
	i = 1
	for u in usersdb:
		if u["user"] == username and u["pass"] == password:
			login = i
		i = i+1
	print username + " " + password
	print login
	return login
	
login = False
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = serversocket.accept()
    try:
        print >>sys.stderr, 'connection from', client_address
        # Receive the data in small packet and retransmit it
        while True:
            
            
			data = connection.recv(128)
			if clean_request(data):
				if logged_request(data) : 
						
					print >>sys.stderr, 'received "%s"' % data
					
					if data:
						t,v,u = unpack_dict(data)
						
						if t == "logout":
							print "removing users["+str(u-1)+"]"
							edit_llama(u,None)
							users.pop(u-1, None)
						elif t == "gname":
							print "getting name from users["+str(u-1)+"]"
							llama = get_llama(u)
							if (llama != None):
								data,l = pack_dict("text",llama.getName(),u)
								connection.sendall(data)
						elif t == "save":
							print "saving users["+str(u-1)+"]"
							llama = get_llama(u)
							llama.save("save-" + str(users[u-1] -1) +".json")
							if (llama != None):
								data,l = pack_dict("text","saved",u)
								connection.sendall(data)
						elif t == "sname":
							print "setting name for users["+str(u-1)+"] -> " + v
							llama = get_llama(u)
							llama.setName(v)
							if (llama != None):
								data,l = pack_dict("text",llama.getName(),u)
								connection.sendall(data)
							else :
								data,l = pack_dict("error","",u)
								connection.sendall(data)
						elif t == "new":
							print "new llama for users["+str(u-1)+"] -> " + v
							edit_llama(u,Llama(""))
							llama = get_llama(u)
							if (llama != None):
								data,l = pack_dict("text",llama.getName(),u)
								connection.sendall(data)
							else :
								data,l = pack_dict("error","",u)
								connection.sendall(data)
						else :
							print >>sys.stderr, 'sending data back to the client'
							connection.sendall(data)
							
						break
				else:
					user_id = check_login(data)
					if user_id == False : 
						msg,l=pack_dict("fail","suca",0)
						connection.sendall(msg)
						break
					else :
						uid = len(users)
						users[uid] = user_id 
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
								
						connection.sendall(msg)
						break
			
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
    finally:
        # Clean up the connectionna
        connection.close()
