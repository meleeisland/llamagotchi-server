"""Llama operation module"""
import os
from src.llamagotchi_class import Llamagotchi
from src.llamaupgrade_class import Llamaupgrade
from src.llama_db import LlamaDb


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


def set_llama(_db, user_id, llama):
    """Set a llama for user with user_id"""
    return _db.set_llama(user_id, llama)


class Llama(object):
    """Llama base class"""

    def __init__(self, name, dbname="test"):
        self._db = LlamaDb(dbname)
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
        """Return string representation of Llama"""
        s_llama = "Llama\n"
        s_llama = s_llama + "Nome : " + self.get_name() + "\n"
        return s_llama

    def to_json(self):
        """Return json representation of Llama"""
        data = {
            'name': self.get_name()
        }
        data["llamagotchi"] = self.llamagotchi.to_json()
        data["llamaupgrade"] = self.llamaupgrade.to_json()
        return data

    def keep_alive(self):
        """Reset keepalive of Llama"""
        self.keepalive = self.keepalivemax
        return self.keepalive

    def tick(self):
        """Tick Llama and subcomponents"""
        self.time = self.time + 1
        self.llamagotchi.tick(self.time)
        self.llamaupgrade.tick(self.time)
        self.keepalive = self.keepalive - 1
        if self.keepalive == 0:
            return False
        return True

    def set_name(self, name):
        """Set llama name"""
        self.name = name

    def get_name(self):
        """Get llama name"""
        return self.name

    def save(self, user_id):
        """Save llama with user_id on linked db"""
        self._db.save_llama(self, user_id)

    def load(self, user_id):
        """Load llama with user_id from linked db"""
        to_update = False
        _d = self._db.load_llama(user_id)
        try:
            self.set_name(_d['name'])
        except KeyError:
            to_update = True
        try:
            _l = _d["llamagotchi"]
            self.llamagotchi.load_json(_l)
        except KeyError:
            to_update = True
        try:
            _l = _d["llamaupgrade"]
            self.llamaupgrade.load_json(_l)
        except KeyError:
            to_update = True
        if to_update:
            self.save(user_id)
