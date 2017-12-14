import os
import json
import unittest
from LlamaClass import Llama 



class LlamaClassTest(unittest.TestCase):
    def testGetName(self):
		calogero = Llama('Calogero')
		self.assertEqual(calogero.getName(), "Calogero")

    def testSetName(self):
		calogero = Llama('Calogero')
		calogero.setName('Pippino')
		self.assertEqual(calogero.getName(), "Pippino")

    def testLoad(self):
		with open("testload.json", 'w') as fp:
			data = { 'name' : 'Pippino' }
			json.dump(data, fp)
		calogero = Llama('Calogero')
		calogero.load('testload.json')
		self.assertEqual(calogero.getName(),'Pippino' )
		
    def testSave(self):
		calogero = Llama('Calogero')
		calogero.setName('Pippino')
		self.assertEqual(calogero.getName(), "Pippino")
		calogero.save('testsave.json')
		data = { 'name' : 'Pippino' }
		with open('testsave.json') as json_data:
			self.assertEqual(json_data.read(),json.dumps(data) )
		os.unlink('testsave.json')
    def testToString(self):
		calogero = Llama('Calogero')
		self.assertEqual(calogero.toString(), "Llama\nNome : Calogero\n")
		calogero = Llama('Cal\!2ogero')
		self.assertEqual(calogero.toString(), "Llama\nNome : Cal\!2ogero\n")
		calogero = Llama('')
		self.assertEqual(calogero.toString(), "Llama\nNome : \n")

if __name__ == '__main__':
    unittest.main()
