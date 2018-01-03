import unittest
from LlamaDB import LlamaDB 


class LlamaDBTest(unittest.TestCase):
    def testConnect(self):
		db = LlamaDB("test")
    def testLogin(self):
		db = LlamaDB("test")
		db.login_user()
		
if __name__ == '__main__':
    unittest.main()
