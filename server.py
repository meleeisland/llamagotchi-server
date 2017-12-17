import os
import sys
import json
import socket
import thread
import time

from src.utils import unpack_dict,pack_dict,clean_request,logged_request,get_llama_id,add_to_users,remove_from_users,get_llamas_ids,savefile_name
from src.LlamaClass import Llama





def tick( threadName, delay):
   count = 0
   while True :
      time.sleep(delay)
      print "tick"
      count += 1
      llamas_ids = get_llamas_ids()
      for u in llamas_ids:
		  llama = get_llama(u)
		  llama.tick()

try:
   thread.start_new_thread( tick, ("tick-thread", 1, ) )
except:
   print "Error: unable to start thread"




usersdb = [{"user":"pippo","pass":"pippo","llama" : None}]
	

def get_llama(u):
	user_id = get_llama_id(u)		
	userdata = usersdb[user_id]
	llama = userdata["llama"]
	return llama
def edit_llama(u,llama):	
	user_id = get_llama_id(u)	
	userdata = usersdb[user_id]
	userdata["llama"] = llama
		
	
	
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
	
	
def handle_data(connection,data):
	t,v,u = unpack_dict(data)

	if t == "logout":
		print "removing users["+str(u-1)+"]"
		edit_llama(u,None)
		remove_from_users(u)
	elif t == "pet":
		print "executing pet for users["+str(u-1)+"]"
		llama = get_llama(u)
		llama.llamagotchi.pet()
		if (llama != None):
			data,l = pack_dict("text","baaah!",u)
			connection.sendall(data)
	elif t == "ghappy":
		print "getting happiness for users["+str(u-1)+"]"
		llama = get_llama(u)
		if (llama != None):
			data,l = pack_dict("text",llama.llamagotchi.getHappiness(),u)
			connection.sendall(data)
	elif t == "gname":
		print "getting name from users["+str(u-1)+"]"
		llama = get_llama(u)
		if (llama != None):
			data,l = pack_dict("text",llama.getName(),u)
			connection.sendall(data)
	elif t == "save":
		print "saving users["+str(u-1)+"]"
		llama = get_llama(u)
		llama.save(savefile_name(u))
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
		
	
	
	
	
	
	
	
	
address = "localhost"
port = int( os.environ['PORT'])
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((address, port))
serversocket.listen(5) # become a server socket, maximum 5 connections

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
						handle_data(connection,data)
						break
				else:
					user_id = check_login(data)
					if user_id == False : 
						msg,l=pack_dict("fail","suca",0)
						connection.sendall(msg)
						break
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
								
						connection.sendall(msg)
						break
			
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
    finally:
        # Clean up the connectionna
        connection.close()
