import json
from LlamagotchiClass import Llamagotchi
from LlamaupgradeClass import Llamaupgrade

class Llama:
	
	def __init__(self, name):
		self.setName(name)
		self.llamagotchi = Llamagotchi()
		self.llamaupgrade = Llamaupgrade()
		self.time = 0
		self.keepalivemax = 1000
		self.keepalive = self.keepalivemax
		
	def toString(self):
		llamaString =  "Llama\n"
		llamaString =  llamaString + "Nome : " + self.getName() +"\n"
		return llamaString
	def keepAlive(self):
		self.keepalive = self.keepalivemax
		return self.keepalive
	def tick(self):
		self.time = self.time + 1
		self.llamagotchi.tick(self.time)
		self.llamaupgrade.tick(self.time)
		self.keepalive = self.keepalive - 1
		if self.keepalive == 0 :
			return False
		else : 
			return True
		
	def setName(self,name):
		self.name = name
	def getName(self):
		return self.name
	def save(self,filename):
		with open(filename, 'w') as fp:
			data = {
				'name' : self.getName()
			}
			data["llamagotchi"] = self.llamagotchi.toJSON()
			data["llamaupgrade"] = self.llamaupgrade.toJSON()
			json.dump(data, fp)
			fp.close()
	def load(self,filename):
		toUpdate = False
		with open(filename) as json_data:
			d = json.load(json_data)
			
			try : self.setName(d['name'])
			except KeyError : toUpdate = True
			try :
				l = d["llamagotchi"]
				self.llamagotchi.loadJSON(l)
			except KeyError : toUpdate = True
			try :
				l = d["llamaupgrade"]
				self.llamaupgrade.loadJSON(l)
			except KeyError : toUpdate = True
			if toUpdate :
				self.save(filename)
			json_data.close()
		
