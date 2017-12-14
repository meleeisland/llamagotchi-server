import json

class Llama:
	
	def __init__(self, name):
		self.setName(name)
		
	def toString(self):
		llamaString =  "Llama\n"
		llamaString =  llamaString + "Nome : " + self.getName() +"\n"
		return llamaString
		
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
	def load(self,filename):
		with open(filename) as json_data:
			d = json.load(json_data)
			self.setName(d['name'])
		
