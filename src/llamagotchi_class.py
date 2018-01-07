"""Module for llamagotchi component"""
import json


class Llamagotchi(object):
    """Class for llamagotchi component"""

    def __init__(self):
        self.happiness = 100

    def to_json(self):
        """Return JSON representation of Llamagotchi"""
        data = {
            'happiness': self.get_happiness()
        }
        return json.dumps(data)

    def load_json(self, jsonstring):
        """Load a JSON representation of Llamagotchi"""
        data = json.loads(jsonstring)
        self.happiness = data['happiness']

    def to_string(self):
        """Return string representation of Llamagotchi"""
        llama_string = "Data\n"
        llama_string = llama_string + "Happiness : " + self.get_happiness() + "\n"
        return llama_string

    def pet(self):
        """Action pet : happiness + 10"""
        self.happiness = int(self.happiness) + 10
        if self.happiness > 100:
            self.happiness = 100

    def get_happiness(self):
        """Return current happiness"""
        return str(self.happiness)

    def tick(self, time):
        """Execute tick for time second"""
        print "llamagotchi ticked" + str(time)
        if time % 100 == 0:
            self.happiness = int(self.happiness) - 1
