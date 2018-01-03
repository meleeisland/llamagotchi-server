import os
import thread
import time

from src.LlamaServerClass import LlamaServer
from src.llama_db import LlamaDb

db = LlamaDb("test")


def tick( threadName, delay , max):
	global db
	count = 0
	while True :
		time.sleep(delay)
		print "tick"
		count += 1
		llama_ids = db.get_logged_llama_session_ids()
		for sessionID in llama_ids :
			print sessionID
			u = db.get_logged_user_id(sessionID)
			print u
			llama = db.get_llama(u)
			for i in range(0,max) :
				if llama.tick() == False :
					llama.save(u)
					db.logout_user(sessionID)


try:
   delay = 1
   ticks = 1
   try :
	   delay = int(os.environ["DELAY"])
   except KeyError :
	   pass
   try :
	   ticks = int(os.environ["TICKS"])
   except KeyError :
	   pass
   thread.start_new_thread( tick, ("tick-thread", delay , ticks, ) )
except:
   print "Error: unable to start thread"



	
	
	

server = LlamaServer('0.0.0.0', int(os.environ["PORT"]),db)

server.start()
