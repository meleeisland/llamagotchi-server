import os
import sys
import json
import socket
STARTMSG="Hello! Llamagotchi client 0.0.1"


def new_game_message():
	return 'New Game';

def send_msg((address, port),message) :
	try:
			
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientsocket.connect((address, port))
		# Send data
		print >>sys.stderr, 'sending "%s"' % message
		clientsocket.sendall(message)

		# Look for the response
		amount_received = 0
		amount_expected = len(message)
		
		while amount_received < amount_expected:
			data = clientsocket.recv(16)
			amount_received += len(data)
			print >>sys.stderr, 'received "%s"' % data

	finally:
		print >>sys.stderr, 'closing socket'
		#~ clientsocket.close()
		
def is_login_data_ok(data):
	t,v,u = unpack_dict(data)
	if (t == "new") : 
		print new_game_message()
		print 'baaah'
		return u
	if (t == "load") : return u
	return False
	

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
	
def send(clientsocket,type,message,uid=0,EXPECTED_LEN=128) :
	MAXLEN=120
	data = ""
	try:
		# Send data
		print >>sys.stderr, 'sending  message "%s":"%s"' % (type, message)
		msg,l = pack_dict(type,message[:MAXLEN],uid)
		clientsocket.send(msg)
		# Look for the response
		amount_received = 0
		#~ amount_expected = EXPECTED_LEN
		data = clientsocket.recv(EXPECTED_LEN)
		amount_received += len(data)
		#~ if  amount_received < amount_expected:
		#~ somethings wrong
		print >>sys.stderr, 'received "%s"' % data
	finally:
		print >>sys.stderr, 'closing socket'
		clientsocket.close()
	return data,amount_received
	
def send_login(clientsocket,username,password) :
	
	print >>sys.stderr, 'sending login message "%s":"%s"' % (username, password)
	data,len = send(clientsocket,"login",username + ":" + password)
	return is_login_data_ok(data)


address = "localhost"
port = int( os.environ['PORT'])


print STARTMSG
username = raw_input("Username: ")	
password = raw_input("Password: ")	

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((address, port))
uid = send_login(clientsocket,username,password)

print uid
if  uid == False : exit (0)



while True :
	
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect((address, port))
	cmd = raw_input("Llamagotchi $> ")	
	print cmd
	if (cmd == 'setname'):
		name = raw_input("LlamaGotchi - Scegli il nome $> ")
		send(clientsocket,"sname",name[:32],uid)
	elif (cmd == 'newllama'): 
		d,l = send(clientsocket,"new","",uid)
		print d
	elif (cmd == 'getname'):
		d,l = send(clientsocket,"gname","",uid)
		print d
	elif (cmd == 'pet'):
		d,l = send(clientsocket,"pet","",uid)
		print d
	elif (cmd == 'happy'):
		d,l = send(clientsocket,"ghappy","",uid)
		print d
	elif (cmd == 'save'):
		d,l = send(clientsocket,"save","",uid)
		print d
	elif (cmd == 'exit'):
		d,l = send(clientsocket,"logout","",uid)
		print d
		exit(0)
	else :
		send(clientsocket,"log-"+str(uid),str(uid) + " " +cmd,uid)
