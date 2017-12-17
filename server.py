import os
import thread
import time

from src.utils import get_llamas_ids,get_llama_id
from src.LlamaServerClass import LlamaServer
from src.LlamaDB import get_llama,edit_llama





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



	
	
	


server = LlamaServer('localhost', int(os.environ["PORT"]))

server.start()
