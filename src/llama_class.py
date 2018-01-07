import os
from llamagotchi_class import Llamagotchi
from llamaupgrade_class import Llamaupgrade
from llama_db import LlamaDb


def get_llama(_db, user_id):
    """Get a llama from user_id.
    If llama is new, create Calogero,
    if llama is saved load it,
    if llama is already logged use it.
    Return llama and type string ("new","load")"""
    llama = _db.get_llama(user_id)
    if llama is False:
        return False, False
    if llama == "new":
        llama = Llama("Calogero")
        llama.save(user_id)
        _db.set_llama(user_id, llama)
        _t = "new"
    elif llama == "load":
        llama = Llama("Calogero")
        llama.load(user_id)
        _db.set_llama(user_id, llama)
        _t = "load"
    else:
        _t = "load"
    return llama, _t


def set_llama( _db, user_id, llama):
    """Set a llama for user with user_id"""
    return _db.set_llama(user_id, llama)


class Llama:

    def __init__(self, name, dbname="test"):
        self.db = LlamaDb(dbname)
        self.set_name(name)
        self.llamagotchi = Llamagotchi()
        self.llamaupgrade = Llamaupgrade()
        self.time = 0
        self.keepalivemax = 20
        try:
            self.keepalivemax = int(os.environ["KEEPALIVEMAX"])
        except KeyError:
            pass
        self.keepalive = self.keepalivemax

    def to_string(self):
        llamaString = "Llama\n"
        llamaString = llamaString + "Nome : " + self.get_name() + "\n"
        return llamaString

    def to_json(self):
        data = {
            'name': self.get_name()
        }
        data["llamagotchi"] = self.llamagotchi.to_json()
        data["llamaupgrade"] = self.llamaupgrade.toJSON()
        return data

    def keep_alive(self):
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

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def save(self, user_id):
        self.db.save_llama(self, user_id)

    def load(self, user_id):
        toUpdate = False
        d = self.db.load_llama(user_id)
        try:
            self.set_name(d['name'])
        except KeyError:
            toUpdate = True
        try:
            l = d["llamagotchi"]
            self.llamagotchi.load_json(l)
        except KeyError:
            toUpdate = True
        try:
            l = d["llamaupgrade"]
            self.llamaupgrade.load_json(l)
        except KeyError:
            toUpdate = True
        if toUpdate:
            self.save(user_id)
