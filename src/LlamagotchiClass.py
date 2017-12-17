import json

class Llamagotchi:
	
	def __init__(self):
		self.happiness = 100
		
	def toJSON(self):
		data = {
			'happiness' : self.getHappiness()
		}
		return	json.dumps(data)	

	def loadJSON(self,jsonstring):
		d = json.loads(jsonstring)
		self.happiness = d['happiness']
		
	def toString(self):
		llamaString =  "Data\n"
		llamaString =  llamaString + "Happiness : " + self.getHappiness() +"\n"
		return llamaString
	def pet(self):
		print "petting"
		self.happiness = self.happiness + 10
		if self.happiness > 100 : self.happiness = 100
	def getHappiness(self):
		return str(self.happiness)
	def tick(self,time):
		print "llamagotchi ticked"
		if time % 100 == 0 :
			self.happiness = self.happiness - 1
	
