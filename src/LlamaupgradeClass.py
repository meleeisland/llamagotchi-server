import json


class Llamaupgrade:

    def __init__(self):
        self.gold = 0

    def toJSON(self):
        data = {
            'gold': self.getGold()
        }
        return json.dumps(data)

    def loadJSON(self, jsonstring):
        d = json.loads(jsonstring)
        self.gold = d['gold']

    def toString(self):
        llamaString = "Data\n"
        llamaString = llamaString + "Gold : " + self.getGold() + "\n"
        return llamaString

    def getGold(self):
        return str(self.gold)

    def tick(self, time):
        print "llamaupgrade ticked"
