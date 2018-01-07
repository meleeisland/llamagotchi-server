"""Module for llamaupgrade component"""
import json


class Llamaupgrade(object):
    """Class for llamagotchi component"""

    def __init__(self):
        self.gold = 0

    def to_json(self):
        """Return JSON representation of Llamaupgrade"""
        data = {
            'gold': self.get_gold()
        }
        return json.dumps(data)

    def load_json(self, jsonstring):
        """Load a JSON representation of Llamaupgrade"""
        _d = json.loads(jsonstring)
        self.gold = _d['gold']

    def to_string(self):
        """Return string representation of Llamaupgrade"""
        s_llama = "Data\n"
        s_llama = s_llama + "Gold : " + self.get_gold() + "\n"
        return s_llama

    def get_gold(self):
        """Return current gold"""
        return str(self.gold)

    def tick(self, time):
        """Execute tick for time second"""
        print "llamaupgrade ticked " + str(time)
