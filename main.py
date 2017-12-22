import os
import sys
from src.LlamaClientClass import LlamaClient
STARTMSG="Hello! Llamagotchi client 0.0.1"

		






def exitcli(client) :
	d = client.send("GET","logout",{"uid":client.user_id()})
	exit(0)
	
def setname(client) :
	name = raw_input("LlamaGotchi - Scegli il nome $> ")
	return  client.send("POST","sname",{"name":name[:32],"uid":client.user_id()})


address = "localhost"
port = int( os.environ['PORT'])


print STARTMSG
username = raw_input("Username: ")	
password = raw_input("Password: ")	

client = LlamaClient(address,port,username,password)

if client.user_id() != False :
	client.addCMD("GET","getname","gname")
	client.addCMD("POST","newllama","new")
	client.addCMD("POST","pet","pet")
	client.addCMD("GET","happy","ghappy")
	client.addCMD("GET","save","save")
	client.addFun("setname",setname)
	client.addFun("exit",exitcli)
	client.start()
	
	
