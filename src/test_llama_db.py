import unittest
from src.llama_db import LlamaDb 


class LlamaDbTest(unittest.TestCase):
    def test_connect(self):
		db = LlamaDb("test")
    def test_login(self):
		self.assertEqual("","")
		
if __name__ == '__main__':
    unittest.main()
