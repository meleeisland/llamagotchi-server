import os
import sys
from src.LlamaClientClass import LlamaClient
STARTMSG="Hello! Llamagotchi client 0.0.1"

		






def exitcli(client) :
	d,l = client.send("logout","")
	exit(0)
	
def setname(client) :
	name = raw_input("LlamaGotchi - Scegli il nome $> ")
	return  client.send("sname",name[:32])


address = "localhost"
port = int( os.environ['PORT'])


print STARTMSG
username = raw_input("Username: ")	
password = raw_input("Password: ")	

client = LlamaClient(address,port,username,password)

if client.user_id() != False :
	client.addCMD("getname","gname")
	client.addCMD("newllama","new")
	client.addCMD("pet","pet")
	client.addCMD("happy","ghappy")
	client.addCMD("save","save")
	client.addFun("setname",setname)
	client.addFun("exit",exitcli)
	client.start()
	
	
