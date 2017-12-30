import os
import thread
import time

from src.utils import get_llamas_ids,get_llama_id,remove_from_users,savefile_name
from src.LlamaServerClass import LlamaServer
from src.LlamaDB import get_llama,edit_llama





def tick( threadName, delay , max):
   count = 0
   while True :
      time.sleep(delay)
      print "tick"
      count += 1
      llamas_ids = get_llamas_ids()
      print str(llamas_ids)
      for u in llamas_ids:
		  llama = get_llama(u)
		  if llama == None :
			  remove_from_users(u)
		  else :
			for i in range(0,max) :
				if llama.tick() == False :
				  llama.save(savefile_name(u))
				  remove_from_users(u)
				

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



	
	
	


server = LlamaServer('0.0.0.0', int(os.environ["PORT"]))

server.start()
