"""HTTPserver for communication and TickThread for time"""
import os

from src.llamaserver_class import LlamaServer, default_llamaserver_config
from src.llama_db import LlamaDb
from src.llama_class import get_llama

DB = LlamaDb("test")


DELAY = 1
TICKS = 1
PORT = 8080
try:
    DELAY = int(os.environ["DELAY"])
except KeyError:
    pass
try:
    PORT = int(os.environ["PORT"])
except KeyError:
    pass
try:
    TICKS = int(os.environ["TICKS"])
except KeyError:
    pass


CONFIG = default_llamaserver_config()
CONFIG["delay"] = DELAY
CONFIG["ticks"] = TICKS

SERVER = LlamaServer('0.0.0.0', PORT, DB, CONFIG)

SERVER.start()
