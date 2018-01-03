import os
from LlamagotchiClass import Llamagotchi
from LlamaupgradeClass import Llamaupgrade
from llama_db import LlamaDb


class Llama:

    def __init__(self, name, dbname="test"):
        self.db = LlamaDb(dbname)
        self.setName(name)
        self.llamagotchi = Llamagotchi()
        self.llamaupgrade = Llamaupgrade()
        self.time = 0
        self.keepalivemax = 20
        try:
            self.keepalivemax = int(os.environ["KEEPALIVEMAX"])
        except KeyError:
            pass
        self.keepalive = self.keepalivemax

    def toString(self):
        llamaString = "Llama\n"
        llamaString = llamaString + "Nome : " + self.getName() + "\n"
        return llamaString

    def toJSON(self):
        data = {
            'name': self.getName()
        }
        data["llamagotchi"] = self.llamagotchi.toJSON()
        data["llamaupgrade"] = self.llamaupgrade.toJSON()
        return data

    def keepAlive(self):
        self.keepalive = self.keepalivemax
        return self.keepalive

    def tick(self):
        self.time = self.time + 1
        self.llamagotchi.tick(self.time)
        self.llamaupgrade.tick(self.time)
        self.keepalive = self.keepalive - 1
        if self.keepalive == 0:
            return False
        else:
            return True

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def save(self, user_id):
        self.db.save_llama(self, user_id)

    def load(self, user_id):
        toUpdate = False
        d = self.db.load_llama(user_id)
        try:
            self.setName(d['name'])
        except KeyError:
            toUpdate = True
        try:
            l = d["llamagotchi"]
            self.llamagotchi.loadJSON(l)
        except KeyError:
            toUpdate = True
        try:
            l = d["llamaupgrade"]
            self.llamaupgrade.loadJSON(l)
        except KeyError:
            toUpdate = True
        if toUpdate:
            self.save(user_id)
