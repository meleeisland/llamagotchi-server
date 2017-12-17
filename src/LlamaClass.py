import json

class Llama:
	
	def __init__(self, name):
		self.setName(name)
		self.time = 0
		self.happiness = 100
		
	def toString(self):
		llamaString =  "Llama\n"
		llamaString =  llamaString + "Nome : " + self.getName() +"\n"
		return llamaString
	def pet(self):
		print "petting"
		self.happiness = self.happiness + 10
		if self.happiness > 100 : self.happiness = 100
	def getHappiness(self):
		return str(self.happiness)
	def tick(self):
		self.time = self.time + 1
		
		if self.time % 100 == 0 :
			self.happiness = self.happiness - 1
		
	def setName(self,name):
		self.name = name
	def getName(self):
		return self.name
	def save(self,filename):
		with open(filename, 'w') as fp:
			data = {
				'name' : self.getName()
			}
			json.dump(data, fp)
			fp.close()
	def load(self,filename):
		with open(filename) as json_data:
			d = json.load(json_data)
			self.setName(d['name'])
			json_data.close()
		
