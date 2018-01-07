"""HTTPserver for communication and TickThread for time"""
import os
import thread
import time

from src.llamaserver_class import LlamaServer
from src.llama_db import LlamaDb
from src.llama_class import get_llama

DB = LlamaDb("test")


def tick(thread_name, _delay, _max, _db , _server):
    """TickThread for time"""
    count = 0
    while True:
        time.sleep(_delay)
        print "[" + thread_name + "]" + "tick"
        count += 1
        llama_ids = _db.get_logged_llama_session_ids()
        for session_id in llama_ids:
            user_id = _db.get_logged_user_id(session_id)
            llama , _ = get_llama( _db ,user_id)
            for _ in range(0, _max):
                if llama.tick() is False:
                    llama.save(user_id)
                    _db.logout_user(session_id)




SERVER = LlamaServer('0.0.0.0', int(os.environ["PORT"]), DB)

try:
    DELAY = 1
    TICKS = 1
    try:
        DELAY = int(os.environ["DELAY"])
    except KeyError:
        pass
    try:
        TICKS = int(os.environ["TICKS"])
    except KeyError:
        pass
    thread.start_new_thread(tick, ("tick_thread", DELAY, TICKS, DB, SERVER, ))
except thread.error:
    print "Error: unable to start thread"

SERVER.start()
