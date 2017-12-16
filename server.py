import os
import sys
import json
import socket

address = "localhost"
port = int( os.environ['PORT'])
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((address, port))
serversocket.listen(5) # become a server socket, maximum 5 connections



usersdb = [{"user":"pippo","pass":"pippo"}]
users = {}


def pack_dict(t,v) :
	d=[t,v]
	a = json.dumps(d)	
	return a,len(a)
def unpack_dict(data):
	data = json.loads(data)
	type = data[0]
	values = data[1]
	return type,values
	
def clean_request(data):
	if len(data) == 0 : return False
	return True
def logged_request(data):
	print data
	type,userdata = unpack_dict(data)
	if "log-" in type :
		userid = int(type.replace("log-",""))
		if userid - 1 in users.keys() :
			return True
	else: return False
	
def check_login(data):
	global usersdb
	
	print >>sys.stderr, 'received "%s"' % data
	type,userdata = unpack_dict(data)
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
			
			
			
			# riceve 3 pacchetti con login username password
			# controlla
			# se non ok : rispondi login non ok e esci
		    # ew : rispondi login ok           
            
            
			data = connection.recv(128)
			if clean_request(data):
				if logged_request(data) : 
						
					print >>sys.stderr, 'received "%s"' % data
					
					
					if data:
						print >>sys.stderr, 'sending data back to the client'
						connection.sendall(data)
				else:
					is_ok = check_login(data)
					if is_ok == False : 
						msg,l=pack_dict("fail","suca")
						connection.sendall(msg)
						break
					else :
						uid = len(users)
						users[uid] = is_ok 
						msg,l=pack_dict("ok",uid+1)
						connection.sendall(msg)
						break
			
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
    finally:
        # Clean up the connection
        connection.close()
