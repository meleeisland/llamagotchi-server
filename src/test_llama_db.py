"""Test for llama_db"""
import unittest
from src.llama_db import LlamaDb


class LlamaDbTest(unittest.TestCase):
    """Unit test class for LlamaDb"""

    def connect(self):
        """Test connect"""
        _db = LlamaDb("test")
        print str(_db)
        self.assertEqual("", "")

    def login(self):
        """Test login"""
        self.assertEqual("", "")


if __name__ == '__main__':
    unittest.main()
