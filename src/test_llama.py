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
        self.assertEqual("", "")

    def testSave(self):
        self.assertEqual("", "")

    def testToString(self):
        calogero = Llama('Calogero')
        self.assertEqual(calogero.toString(), "Llama\nNome : Calogero\n")
        calogero = Llama('Cal\!2ogero')
        self.assertEqual(calogero.toString(), "Llama\nNome : Cal\!2ogero\n")
        calogero = Llama('')
        self.assertEqual(calogero.toString(), "Llama\nNome : \n")


if __name__ == '__main__':
    unittest.main()
